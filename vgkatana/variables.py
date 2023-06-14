from typing import Union
from Katana import NodegraphAPI
from NodegraphAPI.NodegraphGlobals import GetCurrentTime
from NodegraphAPI import Parameter


def get_variables() -> Parameter:
    root_node = NodegraphAPI.GetRootNode()
    variables = root_node.getParameter('variables')
    return variables


def create_array_variable(name: str, elements: list) -> Parameter:
    variables = get_variables()
    group = variables.createChildGroup(name)
    group.createChildNumber('enable', 1)
    if all(isinstance(x, str) for x in elements):
        create_child_array = group.createChildStringArray
        create_child_item = group.createChildString
    elif all(isinstance(x, (float, int)) for x in elements):
        create_child_array = group.createChildNumberArray
        create_child_item = group.createChildNumber
    else:
        return
    options = create_child_array('options', len(elements))
    for option_param, option_value in zip(options.getChildren(), elements):
        option_param.setValue(option_value, GetCurrentTime())
    create_child_item('value', elements[0])
    return group


def get_array_variable_child(
        variable: Union[str, Parameter], name: str) -> Parameter:
    variables = get_variables()
    if isinstance(variable, str):
        variable = variables.getChild(variable)
    value = variable.getChild(name)
    return value


def get_array_variable_value(
        variable: Union[str, Parameter]) -> Union[str, float]:
    value = get_array_variable_child(variable, 'value')
    return value.getValue(GetCurrentTime())


def set_array_variable_value(
        variable: Union[str, Parameter], value: Union[str, float]) -> None:
    value_child = get_array_variable_child(variable, 'value')
    value_child.setValue(value, GetCurrentTime())


def append_array_variable(
        variable: Union[str, Parameter], value: Union[str, float]) -> None:
    options = get_array_variable_child(variable, 'options')
    if value in [o.getValue(GetCurrentTime()) for o in options.getChildren()]:
        return
    index = len(options.getChildren())
    element = options.insertArrayElement(index)
    element.setValue(value, GetCurrentTime())
