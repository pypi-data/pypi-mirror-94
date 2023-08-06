# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging
from enum import Enum
from typing import List
from pathlib import Path

from azureml.data.datapath import DataPath
from azureml.data.data_reference import DataReference
from azureml.data.dataset_consumption_config import DatasetConsumptionConfig
from azureml.data import TabularDataset, FileDataset

from ._pipeline_data import PipelineData
from ._core._run_settings_definition import RunSettingParam
from .run_settings import RunSettings
from ._restclients.designer.models import StructuredInterfaceParameter, RunSettingParameterType, \
    StructuredInterfaceOutput
from ._module_dto import _type_code_to_python_type_name, IGNORE_PARAMS
from ._pipeline_parameters import PipelineParameter
from ._parameter_assignment import _ParameterAssignment
from ._util._attr_dict import _AttrDict
from ._util._exceptions import ComponentValidationError
from ._util._utils import _get_or_sanitize_python_name, is_float_convertible, is_bool_string, is_int_convertible, \
    _is_json_string_convertible, _is_valid_raw_json, _dumps_raw_json


class JsonSchemaType(str, Enum):

    object = "object"
    array = "array"


class ComponentValidator(object):

    @staticmethod
    def validate_component_inputs(provided_inputs,
                                  interface_inputs, param_python_name_dict, process_error, is_local=False):
        """
        It will verify required input is provided and whether input type is valid.
        Current support input types are DataReference, Dataset, DataPath, DatasetConsumptionConfig and PipelineData.
        If is_local is True, tabular dataset is not support and it will support str and Path as input type and
        verify input path exists.

        :param provided_inputs: Inputs to be verified
        :type provided_inputs: dict[str, Input]
        :param interface_inputs: Input interface info
        :type interface_inputs: List[StructuredInterfaceInput]
        :param param_python_name_dict: Map of input name and python name
        :type param_python_name_dict: dict[str, str]
        :param process_error: Function to handle invalid situation
        :type process_error: Callable
        :param is_local: Whether the validation is for local run in the host, false if it is for remote run in AzureML.
        :type is_local: bool
        """
        for _input in interface_inputs:
            formatted_input_name = \
                _get_or_sanitize_python_name(_input.name, param_python_name_dict)
            provided_input_value = provided_inputs.get(formatted_input_name, None)
            if provided_input_value is not None:
                provided_input_value = provided_input_value._build()
            if isinstance(provided_input_value, PipelineParameter):
                provided_input_value = provided_input_value.default_value
            if not _input.is_optional:
                if provided_input_value is None:
                    process_error(ValueError("Required input %s not provided." % formatted_input_name),
                                  ComponentValidationError.MISSING_INPUT)
            if provided_input_value is not None:
                ComponentValidator._validate_input_port_type(
                    _input.name, provided_input_value, process_error, is_local)
            continue

    @staticmethod
    def _validate_input_port_type(input_name, dset, process_error, is_local=False):
        """
        Validate input port type, if is_local=True, TabularDatset is not support and support str and Path as input.

        :param input_name: Input name
        :type input_name: str
        :param dset: Validate input dataset
        :type dset: object
        :param process_error: Function to handle invalid situation
        :type process_error: Callable
        :param is_local: Whether the validation is for local run, false if it is for remote run.
        :type is_local: bool
        """
        if isinstance(dset, DatasetConsumptionConfig):
            dset = dset.dataset
        # DataReference, PipelineData, DataPath, FileDataset both work in local and in remote
        if isinstance(dset, (DataReference, PipelineData, DataPath, FileDataset)):
            return
        if is_local:
            # Except for types both supported, local also support local path
            is_local_dataset = isinstance(dset, str) or isinstance(dset, Path)
            if is_local_dataset and not Path(dset).exists():
                process_error(ValueError("Not found input %s path %s in local." % (input_name, dset)),
                              ComponentValidationError.INVALID_INPUT)
            if not is_local_dataset:
                process_error(ValueError("Input '%s' is invalid type %s for local." % (input_name, type(dset))),
                              ComponentValidationError.INVALID_INPUT)
        else:
            # Except for types both supported, remote also support tabular dataset
            if not isinstance(dset, TabularDataset):
                process_error(ValueError("Input '%s' is invalid type %s." % (input_name, type(dset))),
                              ComponentValidationError.INVALID_INPUT)

    @staticmethod
    def validate_component_parameters(provided_parameters,
                                      interface_parameters, param_python_name_dict, process_error):

        def type_mismatch(parameter_name, _type, param_value):
            process_error(ValueError("Parameter %s type mismatch. " % parameter_name +
                                     "Required %s, got %s." % (_type, type(param_value))),
                          ComponentValidationError.PARAMETER_TYPE_MISMATCH)

        def validate_numeric_parameter(parameter_name, _type, param_value):
            # Try to convert string parameter to int/float
            if isinstance(param_value, str) and parameter_type == '0' \
                    and is_int_convertible(param_value):
                param_value = int(param_value)
            if isinstance(param_value, str) and parameter_type == '1' \
                    and is_float_convertible(param_value):
                param_value = float(param_value)
            if isinstance(param_value, bool):
                type_mismatch(parameter_name, _type, param_value)
                return
            # Don't allow other types when int is required
            if parameter_type == '0' and not isinstance(param_value, int):
                type_mismatch(parameter_name, _type, param_value)
                return
            # Allow int and float when float is required
            if parameter_type == '1' and \
                    not (isinstance(param_value, int) or isinstance(param_value, float)):
                type_mismatch(parameter_name, _type, param_value)
                return

            lower_bound = parameter.lower_bound
            if lower_bound is not None and param_value < float(lower_bound):
                process_error(ValueError("Parameter %s range is invalid. " % parameter_name +
                                         "Lower bound is %s, got %s." % (lower_bound, param_value)),
                              ComponentValidationError.INVALID_PARAMETER)
            upper_bound = parameter.upper_bound
            if upper_bound is not None and param_value > float(upper_bound):
                process_error(ValueError("Parameter %s range is invalid. " % parameter_name +
                                         "Upper bound is %s, got %s." % (upper_bound, param_value)),
                              ComponentValidationError.INVALID_PARAMETER)

        def validate_enum_values_parameter(parameter_name, _type, param_value):
            enum_values = parameter.enum_values
            # Allow pass not str Enum parameter
            if enum_values is not None and not isinstance(param_value, str):
                param_value = str(param_value)
            if not isinstance(param_value, str):
                type_mismatch(parameter_name, _type, param_value)
                return
            if enum_values is not None and param_value not in enum_values:
                process_error(ValueError("Parameter %s is invalid. " % parameter_name +
                                         "Options are %s, got '%s'." % (str(enum_values), param_value)),
                              ComponentValidationError.INVALID_PARAMETER)

        def _is_conditional_optional(parameter, provided_parameters):
            # this is to support build-in components' conditional required parameter
            # e.g. 'Split Data' has parameter named 'Stratification Key Column' which is configured
            # to be enabled by parameter 'Stratified split' with value set ['True']
            # so if parameter 'Stratified split' is provided with value equals to 'True'
            # we should consider 'Stratification Key Column' as a required parameter, otherwise as optional
            if parameter.enabled_by_parameter_name is None or parameter.enabled_by_parameter_values is None:
                return parameter.is_optional

            enabled_by = parameter.enabled_by_parameter_name
            enabled_by_values = parameter.enabled_by_parameter_values
            provided_value = provided_parameters.get(
                _get_or_sanitize_python_name(enabled_by, param_python_name_dict), None)
            return provided_value not in enabled_by_values

        # Validate params
        for parameter in interface_parameters:
            if parameter.name in IGNORE_PARAMS:
                continue

            formatted_parameter_name = \
                _get_or_sanitize_python_name(parameter.name, param_python_name_dict)
            provided_param_value = provided_parameters.get(formatted_parameter_name, None)
            is_parameter_optional = _is_conditional_optional(parameter, provided_parameters)
            if provided_param_value is None:
                if not is_parameter_optional:
                    process_error(ValueError("Required parameter %s not provided." % formatted_parameter_name),
                                  ComponentValidationError.MISSING_PARAMETER)
                continue
            else:

                parameter_type = parameter.parameter_type
                if isinstance(provided_param_value, PipelineParameter):
                    provided_param_value = provided_param_value.default_value
                elif isinstance(provided_param_value, _ParameterAssignment):
                    provided_param_value = provided_param_value.value

                required_parameter_type = _type_code_to_python_type_name(parameter_type)

                # '0' means int type, '1' means float type:
                if parameter_type == '0' or parameter_type == '1':
                    validate_numeric_parameter(formatted_parameter_name, required_parameter_type, provided_param_value)
                # '2' means boolean
                elif parameter_type == '2':
                    if not (isinstance(provided_param_value, bool) or is_bool_string(provided_param_value)):
                        type_mismatch(formatted_parameter_name, required_parameter_type, provided_param_value)
                # '3' means str type
                elif parameter_type == '3':
                    validate_enum_values_parameter(formatted_parameter_name, required_parameter_type,
                                                   provided_param_value)

    @staticmethod
    def validate_compatibility(old_component, new_component):
        """
        provided for replace a component in pipeline
        compare ports and params
        """
        errors = []
        ComponentValidator._validate_ports(old_component, new_component, errors)
        ComponentValidator._validate_parameters(old_component._interface_parameters,
                                                new_component._interface_parameters,
                                                errors)
        return errors

    @staticmethod
    def _validate_ports(old_component, new_component, errors: List):
        """
        validate input and output ports defined in component
        both name and mode, allow additional
        """

        def _input_provided(component, port_name: str):
            provided_inputs = component._inputs
            formatted_input_name = _get_or_sanitize_python_name(port_name,
                                                                component._module_dto.module_python_interface
                                                                .inputs_name_mapping)
            provided_input_value = provided_inputs.get(formatted_input_name, None)
            return provided_input_value is not None

        def _check_missing(ptype: str, old_ports: dict, new_ports: dict, errors: List):
            missing_ports = list(old_ports.keys() - new_ports.keys())
            if len(missing_ports) != 0:
                errors.append("Missing {0} ports in new component function, expected {1}, but not found.".
                              format(ptype, missing_ports))
            # only check inputs now
            if ptype == 'Output':
                return
            mismatched_ports = [[k, v.data_type_ids_list, new_ports[k].data_type_ids_list]
                                for k, v in old_ports.items() if k in new_ports.keys() and
                                _input_provided(old_component, k) and
                                len(set(v.data_type_ids_list) - set(new_ports[k].data_type_ids_list)) > 0]
            # flatten mismatched ports
            mismatched_ports = [mismatched_ports[i][j] for i in range(len(mismatched_ports))
                                for j in range(len(mismatched_ports[i]))]
            if len(mismatched_ports) != 0:
                errors.append("{0} ports data type mismatched {1}, expected type: {2}, actually {3}.".
                              format(ptype, mismatched_ports[0::3], mismatched_ports[1::3],
                                     mismatched_ports[2::3]))
            # check if required port added
            required_ports = {p.name: p.data_type_ids_list for p in new_ports.values()
                              if p.name not in old_ports.keys() and not p.is_optional}
            if len(required_ports) != 0:
                errors.append("New required ports {0} added in new component function, type {1}".
                              format(required_ports.keys(), required_ports.values()))

        old_inputs = {i.name: i for i in old_component._interface_inputs}
        new_inputs = {i.name: i for i in new_component._interface_inputs}
        _check_missing("Input", old_inputs, new_inputs, errors)

        old_outputs = {i.name: i for i in old_component._interface_outputs}
        new_outputs = {i.name: i for i in new_component._interface_outputs}
        _check_missing("Output", old_outputs, new_outputs, errors)
        return errors

    @staticmethod
    def _validate_parameters(old_params, new_params: List[StructuredInterfaceParameter],
                             errors: List):
        """
        validate parameters defined in component with new component's params
        type of interface parameter definition:  List[StructuredInterfaceParameter]

        only compare name and type now, allow additional params
        """
        old_param_dict = {p.name: p.parameter_type for p in old_params}
        new_param_dict = {p.name: p.parameter_type for p in new_params}

        if old_param_dict == new_param_dict:
            return
        # missing params: new function does not contains parameters in the old one
        # check at first to show more clear error message
        missing_params = {p.name: _type_code_to_python_type_name(p.parameter_type)
                          for p in old_params if p.name not in new_param_dict.keys()}
        if len(missing_params) != 0:
            errors.append("Missing parameter in new component function, expected: {0}, but not found.".
                          format(missing_params))

        # mismatched params: new function has some parameters that type mismatched with the old one
        # looks like this: [['name', 'str', 'int'][..]..]
        # the 2nd is type expected and the 3rd is type real
        mismatched_params = [[k, _type_code_to_python_type_name(v),
                              _type_code_to_python_type_name(new_param_dict[k])]
                             for k, v in old_param_dict.items() if k in new_param_dict.keys() and
                             v != new_param_dict[k]]
        # flatten mismatched params
        mismatched_params = [mismatched_params[i][j] for i in range(len(mismatched_params))
                             for j in range(len(mismatched_params[i]))]
        if len(mismatched_params) != 0:
            errors.append("Parameter type mismatched {0}, expected type: {1}, actually {2}.".
                          format(mismatched_params[0::3], mismatched_params[1::3],
                                 mismatched_params[2::3]))
        # check if new component includes required params which not exists in old component
        required_params = {p.name: _type_code_to_python_type_name(p.parameter_type) for p in new_params
                           if p.name not in old_param_dict.keys() and not p.is_optional}
        if len(required_params) != 0:
            errors.append("No such required params {0} provided in old component, type: {1}.".
                          format(required_params.keys(), required_params.values()))

    @staticmethod
    def validate_runsettings(runsettings: RunSettings, process_error):
        for param_name, param_spec in runsettings._params_spec.items():
            if param_spec.is_compute_target:
                # Bypass target validation since we have done it in property setter
                continue
            param_value = getattr(runsettings, param_name, None)
            if param_spec.section_name is not None:
                param_name = "{}.{}".format(param_spec.section_argument_name, param_name)
            ComponentValidator._validate_runsetting_parameter("runsettings.%s" % param_name,
                                                              param_value,
                                                              param_spec,
                                                              process_error)
        # Note: vars(runsettings).keys() here is after src\azure-ml-component\azure\ml\component\pipeline.py::
        # update_component_extra_settings, which only copies runsettings._params_spec values, unexpected
        # runsettings are already filtered out. Therefore, this parameters-not-in-spec-check seems useless.
        # Raise warnings for parameters not in spec
        reserved_param_names = ['target', '_target', 'configure', '_workspace', '_params_spec', '__doc__', '_owner',
                                '_workspace_for_telemetry', '_sections', '_section_params']
        ComponentValidator._raise_warnings_for_params_not_in_spec(
            reserved_param_names,
            set(runsettings._params_spec.keys()).union(runsettings._sections),
            vars(runsettings).keys(), 'runsettings',
        )

    @staticmethod
    def validate_single_runsettings_parameter(param_name, param_value, runsettings, process_error):
        spec = runsettings._params_spec[param_name]
        ComponentValidator._validate_runsetting_parameter("runsettings.%s" % param_name,
                                                          param_value,
                                                          spec,
                                                          process_error)

    @staticmethod
    def validate_single_runsettings_section_parameter(
            section_name, param_name, param_value, runsettings, process_error):
        spec = runsettings._params_spec[param_name]
        ComponentValidator._validate_runsetting_parameter("runsettings.{}.{}".format(section_name, param_name),
                                                          param_value,
                                                          spec,
                                                          process_error)

    @staticmethod
    def validate_k8srunsettings(k8srunsettings, process_error):
        if k8srunsettings is None:
            return
        for section_name in k8srunsettings._params_spec:
            section_settings = getattr(k8srunsettings, section_name, None)
            if section_settings is None:
                continue  # k8srunsettings is all optional
            for param_name in section_settings._params_spec:
                param_spec = section_settings._params_spec[param_name]
                param_value = getattr(section_settings, param_name, None)
                ComponentValidator._validate_runsetting_parameter("k8srunsettings.%s.%s" %
                                                                  (section_settings._section_name, param_name),
                                                                  param_value,
                                                                  param_spec,
                                                                  process_error)
            # Raise warnings for parameters not in spec
            reserved_param_names = ['_params_spec', '_section_name', '__doc__', 'configure', '_owner']
            ComponentValidator._raise_warnings_for_params_not_in_spec(
                reserved_param_names, section_settings._params_spec.keys(), vars(section_settings).keys(),
                "k8srunsettings.%s" % section_name,
            )

        # Raise warnings for sections not in spec
        reserved_section_names = ['_params_spec', '__doc__', '_owner']
        ComponentValidator._raise_warnings_for_params_not_in_spec(
            reserved_section_names, k8srunsettings._params_spec.keys(), vars(k8srunsettings).keys(), 'k8srunsettings',
        )

    @staticmethod
    def validate_single_k8srunsettings_parameter(param_name, param_value, section_settings, process_error):
        spec = section_settings._params_spec[param_name]
        ComponentValidator._validate_runsetting_parameter(
            "k8srunsettings.%s.%s" % (section_settings._section_name, param_name), param_value, spec, process_error,
        )

    @staticmethod
    def _get_runsetting_advanced_validator_by_type(parameter_type):
        if parameter_type == RunSettingParameterType.int_enum or parameter_type == RunSettingParameterType.double:
            return ComponentValidator._validate_numeric_runsetting_parameter
        if parameter_type == RunSettingParameterType.json_string:
            return ComponentValidator._validate_json_string_runsetting_parameter
        return None

    @staticmethod
    def _validate_runsetting_parameter(param_hint_name, param_value, spec: RunSettingParam, process_error):
        if param_value is None:
            # Required parameter validation
            if spec.is_optional is False:
                process_error(ValueError("Required parameter '%s' not provided." % param_hint_name),
                              ComponentValidationError.MISSING_RUNSETTING_PARAMETER)
            return

        # Type validation
        # Handle parameter_type = RunSettingParameterType.json_string situation
        if spec.parameter_type == RunSettingParameterType.json_string and not isinstance(param_value, str):
            # dumps param_value to json string if it's not str
            dumped_json_string = _dumps_raw_json(param_value)
            # get json_schema type
            json_schema_type = spec.json_schema.get("type") if spec.json_schema else None

            if dumped_json_string:
                # param_value is json dump-able and json_schema_type is not None
                if json_schema_type is not None:
                    # Dictionary json type validation
                    if json_schema_type == JsonSchemaType.object:
                        if not isinstance(param_value, dict):
                            process_error(ValueError("Parameter type mismatched '%s', expected type: "
                                                     % param_hint_name +
                                                     "'dict', actually '%s'." % type(param_value).__name__),
                                          ComponentValidationError.INVALID_RUNSETTING_PARAMETER)
                    # List json type validation
                    elif json_schema_type == JsonSchemaType.array:
                        if not (isinstance(param_value, list) or isinstance(param_value, tuple)):
                            process_error(ValueError("Parameter type mismatched '%s', expected type: "
                                                     % param_hint_name +
                                                     "'list' or 'tuple', actually '%s'." % type(param_value).__name__),
                                          ComponentValidationError.INVALID_RUNSETTING_PARAMETER)
                    param_value = dumped_json_string
                else:
                    pass  # skip param_value type check if json_schema type is not given
            else:
                # param_value is not json dump-able
                if json_schema_type is not None:
                    # json_schema type is given
                    if json_schema_type == JsonSchemaType.object:
                        expected_type = "'dict'"
                    elif json_schema_type == JsonSchemaType.array:
                        expected_type = "'list' or 'tuple'"
                    else:
                        expected_type = "serializable JSON"
                    process_error(ValueError("Parameter '%s' with type '%s' "
                                             % (param_hint_name, type(param_value).__name__) +
                                             "is invalid, which is not JSON serializable, expected type: " +
                                             "%s object or JSON string" % expected_type),
                                  ComponentValidationError.INVALID_RUNSETTING_PARAMETER)
                else:
                    # json_schema type is not given
                    process_error(ValueError("Parameter '%s' with type '%s' "
                                             % (param_hint_name, type(param_value).__name__) +
                                             "is invalid, which is not JSON serializable, expected type: " +
                                             "serializable JSON object or JSON string"),
                                  ComponentValidationError.INVALID_RUNSETTING_PARAMETER)

        if not isinstance(param_value, spec.parameter_type_in_py):
            process_error(ValueError("Parameter type mismatched '%s', expected type: " % param_hint_name +
                                     "'%s', " % spec.parameter_type_in_py.__name__ +
                                     "actually '%s'." % type(param_value).__name__),
                          ComponentValidationError.INVALID_RUNSETTING_PARAMETER)

        # Value validation
        advanced_validator = ComponentValidator._get_runsetting_advanced_validator_by_type(spec.parameter_type)
        if advanced_validator is None:
            return  # Pass
        advanced_validator(param_hint_name, param_value, spec, process_error)

    @staticmethod
    def _validate_numeric_runsetting_parameter(param_hint_name, param_value, spec, process_error):
        upper_bound = spec.parameter_type_in_py(spec.upper_bound) if spec.upper_bound is not None else None
        lower_bound = spec.parameter_type_in_py(spec.lower_bound) if spec.lower_bound is not None else None
        if upper_bound is not None and param_value > upper_bound:
            process_error(ValueError("Parameter '%s' is invalid, which should '<= %s', "
                                     % (param_hint_name, upper_bound) +
                                     "got '%s'" % param_value),
                          ComponentValidationError.INVALID_RUNSETTING_PARAMETER)
        if lower_bound is not None and param_value < lower_bound:
            process_error(ValueError("Parameter '%s' is invalid, which should '>= %s', "
                                     % (param_hint_name, lower_bound) +
                                     "got '%s'" % param_value),
                          ComponentValidationError.INVALID_RUNSETTING_PARAMETER)

    @staticmethod
    def _validate_json_string_runsetting_parameter(param_hint_name, param_value, spec, process_error):
        if not _is_json_string_convertible(param_value):
            process_error(ValueError("Parameter '%s' is invalid, " % param_hint_name +
                                     "which should be a valid JSON string"),
                          ComponentValidationError.INVALID_RUNSETTING_PARAMETER)

        if not _is_valid_raw_json(param_value):
            process_error(ValueError("Parameter '%s' is invalid, " % param_hint_name +
                                     "which should be a valid RAW JSON object"),
                          ComponentValidationError.INVALID_RUNSETTING_PARAMETER)

    @staticmethod
    def _raise_warnings_for_params_not_in_spec(reserved_param_names,
                                               param_names_in_spec,
                                               provided_param_names,
                                               config_name):
        expected_param_names = set(reserved_param_names).union(set(param_names_in_spec))
        params_not_in_spec = list(set(provided_param_names) - expected_param_names)
        if len(params_not_in_spec) > 0:
            logging.warning("%s in %s will be ignored." % (params_not_in_spec, config_name))

    @staticmethod
    def _validate_datastore(component_type: str,
                            output_interfaces: List[StructuredInterfaceOutput],
                            output_ports: _AttrDict,
                            process_error):
        """
        Validate data store settings for specific component's output ports.
        Currently, only valid the CosmosStructureStream port for ScopeComponent.

        :param component_type: Component type of the component to be validated
        :type component_type: str
        :param output_interfaces: Output interface definition for the component
        :type output_interfaces: list of StructuredInterfaceOutput
        :param output_ports: Outputs for the component
        :type output_ports: _AttrDict
        :param process_error: Function to handle invalid situation
        :type process_error: Callable
        """
        from azure.ml.component._core._component_definition import ComponentType
        from azureml.data.azure_data_lake_datastore import AzureDataLakeDatastore

        if component_type == ComponentType.ScopeComponent.value:
            # For ScopeComponent, if the output type is CosmosStructureStream,
            # then it's datastore should be AzureDataLakeDatastore
            for output in output_interfaces:
                port = output_ports.get(output.label)
                datastore_name = port.datastore.name if port.datastore is not None else None
                if not isinstance(port.datastore, AzureDataLakeDatastore):
                    process_error(
                        TypeError(
                            'The datastore:{} of type:{} is not valid for output:{}.'
                            .format(datastore_name, type(port.datastore), output.label) +
                            'Because the ScopeComponent only supports AzureDataLakeDatastore.'),
                        ComponentValidationError.INVALID_DATASTORE_TYPE)
