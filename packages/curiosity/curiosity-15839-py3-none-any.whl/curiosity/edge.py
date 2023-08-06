from .node import Node


class Edge:
    """
    Reference to a edge in the Curiosity instance. Should only be created using the ``edges`` method of nodes returned from the Curiosity instance.

    """
    def __init__(self, N: str, U: str, T: str):
        """

        Args:
            N: Node type of the target Node
            U: UID of the target node
            T: Edge type
        """
        self._N = N
        self._U = U
        self._T = T

    def to(self) -> Node:
        """

        Returns: Reference to the target node.

        """
        return Node.uid(self._U, self._N)

    def edge_type(self) -> str:
        """

        Returns: The type of the edge.

        """
        return self._T
