from typing import Optional

from pluggy import PluginManager

from preacher.compilation.request import create_request_compiler
from preacher.compilation.verification import create_description_compiler
from preacher.compilation.verification import create_predicate_compiler
from preacher.compilation.verification import create_response_description_compiler
from .case import CaseCompiler
from .scenario import ScenarioCompiler


def create_scenario_compiler(plugin_manager: Optional[PluginManager] = None) -> ScenarioCompiler:
    request = create_request_compiler()

    predicate = create_predicate_compiler(plugin_manager=plugin_manager)
    description = create_description_compiler(predicate=predicate)
    response = create_response_description_compiler(predicate=predicate, description=description)

    case = CaseCompiler(request=request, response=response, description=description)
    return ScenarioCompiler(description=description, case=case)
