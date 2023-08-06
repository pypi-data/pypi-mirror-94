from enum import Enum
from typing import Any, Optional, Dict, Union

from . import Node


class GraphOperationFlag(Enum):
    add_or_update_node = 0b000000000001
    try_add_node = 0b000000000010
    update_node = 0b000000000100
    delete_node = 0b000000001000
    add_edge = 0b000000010000
    add_unique_edge = 0b000000100000
    remove_all_edges_to = 0b000001000000
    remove_unique_edge = 0b000010000000
    add_alias = 0b000100000000
    clear_aliases = 0b001000000000


class GraphOperation:
    """
    Used internally to aggregate operations to be send in a batch commit to the Curiosity Instance.
    Encapsulates operation on the graph to be serialized and send to the Curiosity Instance.
    Should only be initiated either with the class methods 'Node' and 'Edge'.


    See Also:
        Node : Operations on a node
        Edge : Operations on a edge
    """

    def __init__(self, *, S: Optional[Node] = None, T: Optional[Node] = None, E: Optional[str] = None, C: Optional[Dict[str, Any]] = None, F: GraphOperationFlag = None):
        """

        Args:
            S: Source node
            T: Target node
            E: Edge type
            C: Node content which needs to follow the defined schema
            F: Operation flag on the operation to be performed
        """
        self.S = S
        self.T = T
        self.E = E
        self.C = C
        self.F = F

    @classmethod
    def node(cls, node: Node, content: Union[Dict[str, Any], None], flag: GraphOperationFlag) -> 'GraphOperation':
        """
        Creates a Graph operation on the given Node.

        Args:
            node: Node to perform operation on
            content: Node content which needs to follow the defined schema
            flag: Operation flag on the operation to be performed

        Returns: Created graph operation

        """
        return GraphOperation(S=node, C=content, F=flag)

    @classmethod
    def edge(cls, from_node: node, to_node: node, edge_type: str, flag: GraphOperationFlag) -> 'GraphOperation':
        """

        Args:
            from_node:
            to_node:
            edge_type:
            flag:

        Returns:

        """
        return GraphOperation(S=from_node, T=to_node, E=edge_type, F=flag)

    flag_costs = {
        GraphOperationFlag.add_or_update_node:  1000,
        GraphOperationFlag.try_add_node:        1000,
        GraphOperationFlag.update_node:         1000,
        GraphOperationFlag.delete_node:         1,
        GraphOperationFlag.add_edge:            1,
        GraphOperationFlag.add_unique_edge:     1,
        GraphOperationFlag.remove_all_edges_to: 1,
        GraphOperationFlag.remove_unique_edge:  1,
        GraphOperationFlag.add_alias:           5,
        GraphOperationFlag.clear_aliases:       1,
    }

    def cost(self) -> int:
        """

        Returns: Rough cost on how expensive this operation is to commit.

        """
        if self.F in GraphOperation.flag_costs:
            return GraphOperation.flag_costs[self.F]
        else:
            return 1000
