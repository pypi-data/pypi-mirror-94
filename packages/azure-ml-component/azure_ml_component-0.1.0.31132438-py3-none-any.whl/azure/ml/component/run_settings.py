# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Defines classes for run settings."""

import json
import logging
from typing import Sequence

from azureml._base_sdk_common.field_info import _FieldInfo
from azureml.core.runconfig import RunConfiguration
from ._core._run_settings_definition import RunSettingsDefinition, K8sRunSettingsDefinition, \
    RunSettingParam, K8sSectionDefinition
from ._dynamic import KwParameter, create_kw_method_from_parameters
from ._restclients.service_caller_factory import _DesignerServiceCallerFactory
from ._util._loggerfactory import _LoggerFactory, _PUBLIC_API, track
from ._util._exceptions import InvalidTargetSpecifiedError
from ._util._telemetry import WorkspaceTelemetryMixin

_logger = None


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger(__name__)
    return _logger


class RunSettings(WorkspaceTelemetryMixin):
    """A RunSettings aggregates the run settings of a component."""

    def __init__(self, definition: RunSettingsDefinition, component_name, workspace, owner):
        """
        Initialize RunSettings.

        :param definition: The definition of RunSettings.
        :type definition: RunSettingsDefinition
        :param component_name: The name of the component.
        :type component_name: str
        :param workspace: The workspace of the component.
        :type workspace: azureml.core.Workspace
        :param owner: The component which the RunSettings belongs to.
        :type owner: azure.ml.component.Component
        """
        self._target = None
        # Note: calling runsetting.target will reach the property behind, not here.
        self.target = None if definition.target is None else definition.target.default
        for argument_name, param in definition.params.items():
            if not param.is_compute_target:
                setattr(self, argument_name, param.default)
        self._params_spec = definition.params
        self._workspace = workspace
        self._owner = owner
        self._sections = {}
        self._section_params = {k: v for k, v in definition.params.items() if v.section_name is not None}
        self._generate_configure_func(component_name)
        self._generate_sections(self._section_params)
        WorkspaceTelemetryMixin.__init__(self, workspace=workspace)

    def _generate_sections(self, params):
        sections = {p.section_argument_name for p in params.values()}
        self._sections = sections
        for section in sections:
            setattr(self, section, _RunSettingsSection(
                [p for p in params.values() if p.section_argument_name == section], self._workspace, self._owner))

    def _copy(self, source_setting):
        """
        Copy settings from source_setting to current.

        :param source_setting:
        :type source_setting: RunSettings
        """
        if source_setting is None:
            return

        for k, v in source_setting._params_spec.items():
            # Special case about target
            if v.is_compute_target:
                continue

            if v.section_argument_name is not None:
                value = getattr(getattr(source_setting, v.section_argument_name), k)
                setattr(getattr(self, v.section_argument_name), k, value)
            else:
                value = getattr(source_setting, k)
                setattr(self, k, value)
        self._workspace = source_setting._workspace
        self._target = source_setting._target

    def _generate_configure_func(self, component_name):
        func_docstring_lines = []
        func_docstring_lines.append("Run setting configuration for component [{}]".format(component_name))
        if len(self._params_spec) > 0:
            func_docstring_lines.append("\n")
        params, _doc_string = _format_params(list(self._params_spec.values()), show_deprecated=True)
        func_docstring_lines.extend(_doc_string)
        func_docstring = '\n'.join(func_docstring_lines)
        self.__doc__ = func_docstring

        self.configure = create_kw_method_from_parameters(
            self.configure,
            parameters=params,
            documentation=func_docstring,
        )

    @track(_get_logger, activity_type=_PUBLIC_API)
    def configure(self, *args, **kwargs):
        """
        Configure the runsettings.

        Note that this method will be replaced by a dynamic generated one at runtime with parameters
        that corresponds to the runsettings of the component.
        """
        # Note that the argument list must be "*args, **kwargs" to make sure
        # vscode intelligence works when the signature is updated.
        # https://github.com/microsoft/vscode-python/blob/master/src/client/datascience/interactive-common/intellisense/intellisenseProvider.ts#L79
        self._configure(*args, **kwargs)

    def _configure(self, *args, **kwargs):
        # @track on public will increase call stack depth,
        # and log unnecessary telemetry which not triggered by user, which we should avoid.
        for k, v in kwargs.items():
            # Ignore None value since it's the default value
            if v is None:
                continue
            setattr(self, k, v)

    def __repr__(self):
        """Return the representation of the RunSettings."""
        params_str = ''
        param_names = self._params_spec.keys()
        for name in param_names:
            params_str += '{}: {}\n'.format(name, getattr(self, name))
        return params_str

    def __setattr__(self, key, value):
        """Manage attribute validation."""
        # Track if user configure runsettings via configure or direct assign.
        # _specify_runsettings will be used for telemetry and create pipeline instance by pipeline definition.
        from ._component_validator import RunSettingParameterType, ComponentValidator
        if hasattr(self, '_params_spec') and (key in self._params_spec.keys() or 'target' == key):
            self._owner._specify_runsettings = True
            if key != "target":  # Bypass target validation since we have done it in property setter
                ComponentValidator.validate_single_runsettings_parameter(
                    key, value, self, RunSettings._process_error)
                if self._params_spec[key].parameter_type == RunSettingParameterType.json_string and \
                        not isinstance(value, str) and value is not None:
                    value = json.dumps(value)

        # Always save the attr
        # Even for deprecated params, we need this to generate the old interfaces
        super().__setattr__(key, value)

        # For deprecated params, print warning and save the value by new interface,
        # since we get the value from new interface in __getattr__
        if hasattr(self, '_section_params') and key in self._section_params.keys():
            section_name = self._section_params[key].section_argument_name
            logging.warning("{} is deprecated, please use runsettings.{}.{}.".format(
                key, section_name, key))
            setattr(getattr(self, section_name), key, value)

        # Check unexpected runsettings.
        # Add "target" in reserved_param_names, because _params_spec of hdi-component has no "target".
        reserved_param_names = {'target', '_target', 'configure', '_workspace', '_params_spec', '__doc__', '_owner',
                                '_workspace_for_telemetry', '_sections', '_section_params'}
        if hasattr(self, '_params_spec') and key not in reserved_param_names.union(
                set(self._params_spec.keys())).union(self._sections if hasattr(self, '_sections') else {}):
            logging.warning("{} is not expected runsettings, will be ignored.".format(key))

    def __getattribute__(self, key):
        """Override this to make a hint for deprecated parameters."""
        # For deprecated params, get value from the new interfaces
        reserved_names = {
            'target', '_target', 'configure', '_workspace', '_params_spec', '__doc__', '_owner',
            '_workspace_for_telemetry', '_sections', '_section_params'}
        if key not in reserved_names and hasattr(self, '_section_params') and key in self._section_params.keys():
            section_name = self._section_params[key].section_argument_name
            return getattr(getattr(self, section_name), key)

        return object.__getattribute__(self, key)

    @property
    def _use_default_compute(self):
        return self._target is None

    @property
    def target(self):
        """
        Use name "target" to provide a common access for compute parameter.

        Because the name of compute parameter in HDInsight component is "Compute Name", while other components'
        are "Target".
        :return: The compute target name and type tuple like ('aml-compute', 'AmlCompute').
        :rtype: tuple(str, str)
        """
        return self._target

    @target.setter
    def target(self, compute):
        if compute is not None:
            if isinstance(compute, str):
                # Get compute type
                service_caller = _DesignerServiceCallerFactory.get_instance(self._workspace)
                target_compute = service_caller.get_compute_by_name(compute)
                if target_compute is None:
                    raise InvalidTargetSpecifiedError(target_name="RunSettings.target",
                                                      message="Cannot find compute '{}' in workspace".format(compute))
                else:
                    compute = (compute, target_compute.compute_type)
            elif not (isinstance(compute, tuple) and len(compute) == 2 and
                      isinstance(compute[0], str) and isinstance(compute[1], str)):
                raise InvalidTargetSpecifiedError(target_name="RunSettings.target",
                                                  message="Bad value for target, expect a string value")
        self._target = compute

    @staticmethod
    def _process_error(e: Exception, error_type):
        # Raise exception when hit INVALID_RUNSETTING_PARAMETER
        # Since missing some parameters is allowed when calling runsettings.configure(), for example:
        # runsettings.configure(node_count=2)
        # runsettings.target = 'amlcompute'
        from ._component_validator import ComponentValidationError
        if error_type == ComponentValidationError.INVALID_RUNSETTING_PARAMETER:
            ve = ComponentValidationError(str(e), e, error_type)
            raise ve


class _RunSettingsSection(WorkspaceTelemetryMixin):
    def __init__(self, params, workspace, owner):
        self._section_name = params[0].section_argument_name
        section_description = params[0].section_description
        if section_description is None:
            section_description = self._section_name
        for p in params:
            setattr(self, p.argument_name, p.default_value)
        self._params_spec = {p.argument_name: p for p in params}
        self._generate_configure_func(section_description, params)
        self._owner = owner
        WorkspaceTelemetryMixin.__init__(self, workspace=workspace)

    def _generate_configure_func(self, section_description, params):
        func_docstring_lines = [section_description]
        func_params, _doc_string = _format_params(params, is_compute_run_settings=True)
        func_docstring_lines.extend(_doc_string)
        func_docstring = '\n'.join(func_docstring_lines)
        self.__doc__ = func_docstring
        self.configure = create_kw_method_from_parameters(
            self.configure,
            parameters=func_params,
            documentation=func_docstring,
        )

    @track(_get_logger, activity_type=_PUBLIC_API)
    def configure(self, *args, **kwargs):
        """
        Configure the runsettings.

        Note that this method will be replaced by a dynamic generated one at runtime with parameters
        that corresponds to the runsettings of the component.
        """
        # Note that the argument list must be "*args, **kwargs" to make sure
        # vscode intelligence works when the signature is updated.
        # https://github.com/microsoft/vscode-python/blob/master/src/client/datascience/interactive-common/intellisense/intellisenseProvider.ts#L79
        from ._component_validator import ComponentValidator, RunSettingParameterType
        for k, v in kwargs.items():
            # Ignore None value since it's the default value
            if v is None:
                continue
            ComponentValidator.validate_single_runsettings_section_parameter(
                self._section_name, k, v, self, RunSettings._process_error)
            if self._params_spec[k].parameter_type == RunSettingParameterType.json_string and \
                    not isinstance(v, str):
                v = json.dumps(v)
            setattr(self, k, v)

    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)
        # Track if user configure runsettings via configure or direct assign.
        # _specify_runsettings will be used for telemetry and create pipeline instance by pipeline definition.
        if hasattr(self, '_params_spec') and key in self._params_spec.keys():
            self._owner._specify_runsettings = True


class _K8sRunSettings(object):
    def __init__(self, params: K8sRunSettingsDefinition, owner):
        self._params_spec = params
        for section_name, section_params in params.items():
            setattr(self, section_name, _K8sRunSettingsSection(section_params, section_name, owner))
        sections = sorted([section for section in params])
        self.__doc__ = "The compute run settings for Component, only take effect " \
                       "when compute type is in {}.\n" \
                       "Configuration sections: {}.".format(params.available_computes, str(sections))

    def __repr__(self):
        params_str = ''
        for name, section in sorted(self._params_spec.items()):
            params_str += '{}:\n'.format(section.name)
            for p in section.params.values():
                params_str += '\t{}: {}\n'.format(
                    p.argument_name, getattr(getattr(self, name), p.argument_name),
                )
        return params_str

    def _copy(self, source_setting):
        """
        Copy settings from source_setting to current.

        :param source_setting:
        :type source_setting: _K8sRunSettings
        """
        if source_setting is None:
            return
        for name, section in source_setting._params_spec.items():
            if name not in self._params_spec:
                continue
            current_section = getattr(self, name)
            source_section = getattr(source_setting, name)
            params = {_p.argument_name: getattr(source_section, _p.argument_name) for _p in section.params.values()}
            current_section.configure(**params)


class _K8sRunSettingsSection(object):
    def __init__(self, section: K8sSectionDefinition, section_name, owner):
        self._section_name = section_name
        for p in section.params.values():
            setattr(self, p.argument_name, p.default_value)
        self._params_spec = section.params
        self._generate_configure_func(section)
        self._owner = owner

    def _generate_configure_func(self, section: K8sSectionDefinition):
        func_docstring_lines = [section.description]
        func_params, _doc_string = _format_params(section.params.values(), is_compute_run_settings=True, )
        func_docstring_lines.extend(_doc_string)
        func_docstring = '\n'.join(func_docstring_lines)
        self.__doc__ = func_docstring
        self.configure = create_kw_method_from_parameters(
            self.configure,
            parameters=func_params,
            documentation=func_docstring,
        )

    def configure(self, *args, **kwargs):
        """
        Configure the runsettings.

        Note that this method will be replaced by a dynamic generated one at runtime with parameters
        that corresponds to the runsettings of the component.
        """
        # Note that the argument list must be "*args, **kwargs" to make sure
        # vscode intelligence works when the signature is updated.
        # https://github.com/microsoft/vscode-python/blob/master/src/client/datascience/interactive-common/intellisense/intellisenseProvider.ts#L79
        for k, v in kwargs.items():
            # Ignore None value since it's the default value
            if v is None:
                continue
            from ._component_validator import ComponentValidator
            ComponentValidator.validate_single_k8srunsettings_parameter(k, v, self,
                                                                        RunSettings._process_error)
            setattr(self, k, v)

    def __repr__(self):
        params_str = ''
        param_names = self._params_spec.keys()
        for name in param_names:
            params_str += '{}: {}\n'.format(name, getattr(self, name))
        return params_str

    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)
        # Track if user configure runsettings via configure or direct assign.
        # _specify_runsettings will be used for telemetry and create pipeline instance by pipeline definition.
        if hasattr(self, '_params_spec') and key in self._params_spec.keys():
            self._owner._specify_k8srunsettings = True


def _set_compute_field(k8srunsettings, compute_type, run_config):
    compute_params_spec = k8srunsettings._params_spec
    if compute_params_spec is None:
        return
    compute_field_map = {'Cmk8s': 'cmk8scompute', 'CmAks': 'cmakscompute'}
    if compute_type in compute_field_map:
        field_name = compute_field_map[compute_type]
        aks_config = {'configuration': dict()}
        for section_name in compute_params_spec:
            for param in compute_params_spec[section_name]:
                value = getattr(getattr(k8srunsettings, section_name), param.argument_name)
                if value is not None:
                    aks_config['configuration'][param.argument_name] = value
        run_config._initialized = False
        setattr(run_config, field_name, aks_config)
        run_config._initialized = True
        RunConfiguration._field_to_info_dict[field_name] = _FieldInfo(dict,
                                                                      "{} specific details.".format(field_name))
        run_config.history.output_collection = True


def _format_params(source_params: Sequence[RunSettingParam], is_compute_run_settings=False, show_deprecated=False):
    target_params = []
    func_docstring_lines = []
    for param in source_params:
        param_name = param.argument_name
        param_name_in_doc = param_name
        # For Hdi component, the name of target parameter is "compute_name"
        # But in sdk, we use "target" to access the target parameter
        # So we add a hint here to indicate "target" is exactly "compute_name"
        if param.is_compute_target and param_name != 'target':
            param_name = 'target'
            param_name_in_doc = 'target ({})'.format(param_name_in_doc)
        # For the k8s compute run settings,
        # the default value in spec is not match the value in description,
        # so we remove "default value" part in doc string for this case.
        param_line = None
        if param.is_optional:
            param_line = ":param {}: {} (optional{})".format(
                param_name_in_doc, param.description,
                "" if is_compute_run_settings else ", default value is {}.".format(param.default_value))
        else:
            param_line = ":param {}: {}".format(param_name_in_doc, param.description)
        if param.section_name is not None and show_deprecated:
            param_line = "{} (deprecated, please use runsettings.{}.{})".format(
                param_line, param.section_argument_name, param.argument_name)
        func_docstring_lines.append(param_line)
        parameter_type = param.parameter_type
        func_docstring_lines.append(":type {}: {}".format(param_name_in_doc, parameter_type.value))
        target_params.append(KwParameter(
            param_name,
            annotation=param.description,
            # Here we set all default values as None to avoid overwriting the values by default values.
            default=None,
            _type=parameter_type.value))
    return target_params, func_docstring_lines
