import json
from datetime import datetime
from typing import Any

from .graph_operation import GraphOperation, GraphOperationFlag
from .node import EmittedNode, Node


def del_none(d: Any) -> Any:
    """
    Delete keys with the value ``None`` in a dictionary, recursively.

    This alters the input so you may wish to ``copy`` the dict first.
    """
    if d is None:
        return d
    if isinstance(d, list):
        return [del_none(ditem) for ditem in d]

    if type(d) in dict_conversion:
        d = dict_conversion[type(d)](d)
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
    return d  # For convenience


dict_conversion = {
    EmittedNode:    lambda o: {"U": o.U, "K": o.K, "T": o.T, "C": o.C, "E": o.E},
    Node:           lambda o: {"U": o.U, "K": o.K, "T": o.T},
    GraphOperation: lambda o: {"S": o.S, "T": o.T, "E": o.E, "C": o.C, "F": o.F}
}


class CuriosityJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, GraphOperationFlag):
            return o.value

        if type(o) in dict_conversion:
            return dict_conversion[type(o)](o)

        ret = json.JSONEncoder.default(self, o)

        return ret
