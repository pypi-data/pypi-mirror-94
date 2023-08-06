"""Scenario compilation."""

from functools import partial
from typing import Iterator, List, Optional, Mapping

from preacher.compilation.argument import Arguments, inject_arguments
from preacher.compilation.error import on_key
from preacher.compilation.parameter import Parameter, compile_parameter
from preacher.compilation.util.functional import (
    map_compile,
    compile_flattening,
)
from preacher.compilation.util.type import (
    ensure_bool,
    ensure_optional_str,
    ensure_list,
    ensure_mapping,
)
from preacher.compilation.verification import DescriptionCompiler
from preacher.core.scenario import Scenario, Case
from .case import CaseCompiler

_KEY_LABEL = 'label'
_KEY_WHEN = 'when'
_KEY_DEFAULT = 'default'
_KEY_ORDERED = 'ordered'
_KEY_CASES = 'cases'
_KEY_PARAMETERS = 'parameters'
_KEY_SUBSCENARIOS = 'subscenarios'


class ScenarioCompiler:

    def __init__(self, description: DescriptionCompiler, case: CaseCompiler):
        self._description = description
        self._case = case

    def compile(self, obj: object, arguments: Optional[Arguments] = None) -> Scenario:
        """
        Compile the given object into a scenario.

        Args:
            obj: A compiled object, which should be a mapping.
            arguments: Arguments to inject.
        Returns:
            The scenario as the result of compilation.
        Raises:
            CompilationError: when the compilation fails.
        """

        obj = ensure_mapping(obj)
        arguments = arguments or {}

        label_obj = inject_arguments(obj.get(_KEY_LABEL), arguments)
        with on_key(_KEY_LABEL):
            label = ensure_optional_str(label_obj)

        parameters_obj = obj.get(_KEY_PARAMETERS)
        if parameters_obj is not None:
            with on_key(_KEY_PARAMETERS):
                parameters_obj = ensure_list(parameters_obj)
                parameters = list(
                    map_compile(compile_parameter, parameters_obj)
                )
            subscenarios = [
                self._compile_parameterized(obj, arguments, parameter)
                for parameter in parameters
            ]
            return Scenario(label=label, subscenarios=subscenarios)

        ordered_obj = inject_arguments(obj.get(_KEY_ORDERED, True), arguments)
        with on_key(_KEY_ORDERED):
            ordered = ensure_bool(ordered_obj)

        default_obj = inject_arguments(obj.get(_KEY_DEFAULT, {}), arguments)
        with on_key(_KEY_DEFAULT):
            case_compiler = self._case.compile_default(default_obj)

        condition_obj = inject_arguments(obj.get(_KEY_WHEN, []), arguments)
        with on_key(_KEY_WHEN):
            conditions = self._compile_conditions(condition_obj)

        case_obj = inject_arguments(obj.get(_KEY_CASES, []), arguments)
        with on_key(_KEY_CASES):
            cases = self._compile_cases(case_compiler, case_obj)

        subscenario_obj = obj.get(_KEY_SUBSCENARIOS, [])
        with on_key(_KEY_SUBSCENARIOS):
            subscenarios = self._compile_subscenarios(
                case_compiler,
                subscenario_obj,
                arguments,
            )

        return Scenario(
            label=label,
            ordered=ordered,
            conditions=conditions,
            cases=cases,
            subscenarios=subscenarios,
        )

    def compile_flattening(
        self,
        obj: object,
        arguments: Optional[Arguments] = None,
    ) -> Iterator[Scenario]:
        """
        Compile the given object into a scenario with flattening:
        a nested object list results in a flattened scenario.

        Args:
            obj: A compiled object or a list.
            arguments: Arguments to inject.
        Returns:
            A scenario iterator as the result of compilation.
        Raises:
            CompilationError: when the compilation fails for each iteration.
        """

        compile = partial(self.compile, arguments=arguments)
        return compile_flattening(compile, obj)

    def _compile_conditions(self, obj: object):
        return list(map_compile(self._description.compile, ensure_list(obj)))

    @staticmethod
    def _compile_cases(case_compiler: CaseCompiler, obj: object) -> List[Case]:
        return list(
            map_compile(case_compiler.compile_fixed, ensure_list(obj))
        )

    def _compile_subscenarios(
        self,
        case: CaseCompiler,
        obj: object,
        arguments: Arguments,
    ) -> List[Scenario]:
        compiler = ScenarioCompiler(description=self._description, case=case)
        return list(map_compile(
            lambda sub_obj: compiler.compile(sub_obj, arguments=arguments),
            ensure_list(obj),
        ))

    def _compile_parameterized(
        self,
        obj: Mapping,
        arguments: Arguments,
        parameter: Parameter,
    ) -> Scenario:
        template = {
            k: v for (k, v) in obj.items()
            if k not in (_KEY_LABEL, _KEY_PARAMETERS)
        }
        template['label'] = parameter.label

        arguments = dict(arguments)
        arguments.update(parameter.arguments)
        return self.compile(template, arguments)
