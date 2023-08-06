from __future__ import annotations

from typing import Optional, Any, Dict, List


class Node:
    """
        Unique reference to a node in the graph. Either a Node Type + Key pair or a Unique Identifier (UID) used in the system.
        Both can be usually used interchangeably.

        Create a new Node object:

        >>> nodeA = Node.uid("MyNodeUID")
        >>> nodeB = Node.key("MyNodeType", "MyNodeKey")

        Methods that create or change nodes will always return a Node object that you can use in subsequent calls
        (such as adding edges or aliases, restricting access or deleting it).
    """

    def __init__(self, U: Optional[str] = None, K: Optional[str] = None, T: str = None):
        """

        Args:
            U: UID
            K: Key
            T: Node type
        """
        self.U = U
        self.K = K
        self.T = T

    @classmethod
    def uid(cls, uid: str, node_type: str) -> 'Node':
        """
        Creates a local reference to a node with the given UID.  The UID uniquely identifies the node in the Curiosity instance.

        :param uid: UID of the existing Node in the system.
        :param node_type: The node type of the existing node
        :return: Node for further use by the library
        """
        return Node(uid, None, node_type)

    @classmethod
    def key(cls, node_type: str, key: str) -> 'Node':
        """
        Creates a local reference to a node with the given node type and key. The combination of node type and key uniquely identifies the node in the Curiosity instance.

        :param node_type: The node type of the existing or new node
        :param key: The key of the existing or new node
        :return: Node for further use by the library
        """
        return Node(None, key, node_type)


class EmittedNode(Node):
    """
    Reference to a node returned by the Curiosity instance.
    """
    def __init__(self, U: Optional[str], K: Optional[str], T: str, C: Dict[str, Any], E: List['Edge']):
        super().__init__(U, K, T)
        self.C: Dict[str, Any] = C
        self.E: List['Edge'] = E

    def get_field(self, field: str) -> Any:
        """
        Args:
            field: Name of the field in the node schema.

        Returns: The value of the given field for this node.

        """
        if self.C is dict:
            if field in self.C:
                return self.C[field]
            else:
                raise Exception(f"Field '{field}' not found in the node content - either you forgot to emit it, or the name is incorrect.")

    def edges(self) -> List['Edge']:
        """

        Returns: The outgoing edges of this node.

        """
        return self.E
