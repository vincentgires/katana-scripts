from NodegraphAPI.NodegraphGlobals import GetCurrentTime
from NodegraphAPI import Parameter
from typing import Union


def set_parameter(
        obj: object,
        name: str,
        value: Union[str, int, float, bool]) -> Parameter:
    param = obj.getParameter(name)
    param.setValue(value, GetCurrentTime())


def append_child(
        parameter: Parameter,
        name: str,
        value: Union[str, int, float]) -> Parameter:
    if name in [c.getName() for c in parameter.getChildren()]:
        return
    if isinstance(value, str):
        create_child_item = parameter.createChildString
    elif isinstance(value, (float, int)):
        create_child_item = parameter.createChildNumber
    else:
        return
    child = create_child_item(name, value)
    return child
