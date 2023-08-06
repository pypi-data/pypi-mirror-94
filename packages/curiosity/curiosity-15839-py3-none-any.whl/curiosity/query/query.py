from typing import Union, List

from .. import Node


class Query:
    """
    The ``Query`` interface provides methods to fetch data from the graph database.
    This can either be done directly by providing a keys to nodes or by traversing the graph.

    A Query has a state that is changed by operations performed on the query:

    * A current collection of nodes on which operations can be perfumed on.
    * A result object that is emitted once the query is run.

    See Also:
        (Knowledge Graph)[http://docs.curiosity.ai/en/articles/4452643-knowledge-graph]

    Examples:
        >>> graph.query(
        >>>         # Empty query object to run queries on
        >>>         Query()
        >>>         # Sets the current collection of nodes to all nodes of the node type "MyEntity"
        >>>         .start_at("MyEntity")
        >>>         # Follow all outgoing edges to nodes of type "_FilesEntry" and replace current collection of nodes with these "_FilesEntry" nodes.
        >>>         .out("_FileEntry")
        >>>         # Add the current collection of nodes to the result object under the key "FilesWithMyEntity". Also fetches the field "OriginalName" of the nodes in the collection.
        >>>         .emit("FilesWithMyEntity", ["OriginalName"]))
    """

    def __init__(self):
        self.query = []

    def start_at(self, n: Union[str, Node, List[Node]]) -> 'Query':
        """
        Sets the current collection of nodes to a node, a list of nodes or all nodes of a given node type.

        Args:
            n: node(s) or a node type
        """

        if isinstance(n, str):
            self.query.append({"op": "StartAt", "args": {"nodeType": n}})
        elif isinstance(n, Node):
            self.query.append({"op": "StartAt", "args": {"node": n}})
        elif isinstance(n, list):
            self.query.append({"op": "StartAt", "args": {"nodes": n}})
        else:
            raise ValueError(f"Can't StartAt for type {type(n)}")
        return self

    def out(self, node_type: Union[str, Node, List[Node]] = None, edge_type: Union[str, List[str]] = None) -> 'Query':
        """
        Follows outgoing edges from the current collection of nodes and replaces the current collection of nodes with the target nodes.

        Examples:

            Fetch all Authors(Person) for a given file.

            This assumes the following relationship:

            File -HasAuthor-> Person

            1. *Query*: Create a new query.

            2. *StartAt*: Starts the query at the given file with the given id.

            3. *Out*: Follows all outgoing edges of type "HasAuthor" from this file to "Person" nodes.

            4. *Emit*: Adds this collection of authors to the emitted output under the key "Authors"

            5. *graph.Query*: Run the query.

            >>>    my_file = "SsdKH2jhdf345S0M3UID"
            >>>    teams_result = graph.query(Query().start_at(my_file).out("Person", "HasAuthor").emit("Authors"))

            The response will include Persons and Teams related to the given file.

            >>> {
            >>>   "R": {
            >>>     "Authors": [
            >>>       {
            >>>         "U": "BW6iEUWesnKY4VrjrhVzKw",
            >>>         "T": "_AccessGroup",
            >>>         "C": {}
            >>>       },
            >>>       {
            >>>         "U": "BVyHzAPixAYJqZoH9FBwM6",
            >>>         "T": "_AccessGroup",
            >>>         "C": {}
            >>>       }
            >>>     ]
            >>>   },
            >>>   "MS": 4.0285
            >>> }

        Args:
            node_type: Restricts the targets of the edges to follow to the given node types.
            edge_type: Restricts the edges to follow to only edges of the given edge types.

        """
        current_out = {}

        if node_type is not None:
            if isinstance(node_type, str):
                current_out = {"nodeType": node_type}
            elif isinstance(node_type, Node):
                current_out = {"node": node_type}
            elif isinstance(node_type, list):
                current_out = {"nodes": node_type}
            else:
                raise ValueError(f"Can't out for type {type(node_type)}")

        if edge_type is not None:
            if isinstance(edge_type, str):
                current_out.update({"edgeType": edge_type})
            elif isinstance(edge_type, list):
                current_out.update({"edgeTypes": edge_type})
            else:
                raise ValueError(f"Can't out for type {type(node_type)}")
        self.query.append({"op": "Out", "args": current_out})
        return self

    def out_many(self, levels: int, node_types: List[str], edge_types: List[str], distinct: bool = True) -> 'Query':
        """
        Similar to *Out* but following edges for multiple levels while keeping the intermediate nodes.
        Follows outgoing edges from the current collection of nodes for multiple levels and replaces the current collection of nodes with the target and intermediate nodes.

        See Also:
            See *Out*, how to emit only the last layer, by calling *Out* multiple times.

        Example:

            Fetch all Authors(Person) and the Teams they are in for a given file.

            This assumes the following relationships:

            File -HasAuthor-> Person

            Person -InTeam-> Team

            >>>    my_file = "SsdKH2jhdf345S0M3UID"
            >>>    teams_result = graph.query(Query().start_at(my_file).out_many(2, ["Person", "Team"], ["HasAuthor" ,"InTeam"]).emit("Teams"))

            The response will include Persons and Teams related to the given file.

            >>> {
            >>>  "R": {
            >>>    "Teams": [
            >>>      {
            >>>        "U": "BW6iEUWesnKY4VrjrhVzKw",
            >>>        "T": "Person",
            >>>        "C": {}
            >>>      },
            >>>      {
            >>>        "U": "BVyHzAPixAYJqZoH9FBwM6",
            >>>        "T": "Person",
            >>>        "C": {}
            >>>      },
            >>>      {
            >>>        "U": "MzmYCqZrjeddaquFAq4wwf",
            >>>        "T": "Team",
            >>>        "C": {}
            >>>      }
            >>>    ]
            >>>  }
            >>> }

        Args:

            levels : maximum number of levels to follow
            node_types : restricts the edges to follow to only targets of the given node types
            edge_types : restricts the edges to follow to only edges of the given edge types
            distinct : make resulting current collection of nodes distinct
        """
        self.query.append({"op": "OutMany", "args": {"levels": levels, "nodeTypes": node_types, "edgeTypes": edge_types,
                                                     "distinct": distinct}})
        return self

    def similar(self, index: str, count: int, tolerance: float) -> 'Query':
        """
        Replaces the current collection of nodes with similar nodes based on the given similarity index.

        See Also:
            [Models & Text pocessing](https://docs.curiosity.ai/en/collections/2550055-models-text-processing)
            TODO pius: add docs page how to get similarity index

        Args:
            index:
            count:
            tolerance:

        """
        self.query.append({"op": "Similar", "args": {"index": index, "count": count, "tolerance": tolerance}})
        return self

    def skip(self, count: int) -> 'Query':
        """
        Removes the given count from the beginning of the current collection of nodes.

        See Also:
            *Take*

        Args:
            count: number of nodes to skip
        """
        self.query.append({"op": "Skip", "args": {"count": count}})
        return self

    def take(self, count: int) -> 'Query':
        """
        Limits the number of nodes in the current collection of nodes. Removes all other nodes from the current collection of nodes.

        See Also:
            *Skip*

        Args:
            count:  number of nodes to take

        """
        self.query.append({"op": "Take", "args": {"count": count}})
        return self

    def emit(self, emit_key: str, fields: List[str] = None) -> 'Query':
        """

        Adds the current collection to the final output under the given emit_key.

        Examples:

            1. *Query*: Create a new query.

            2. *StartAt*: Sets the current collection of nodes to the given files.

            4. *Emit*: Adds these files to the emitted output under the key "Files" and fetches the field "Metadata" form the current nodes ("Files").

            5. *graph.Query*: Run the query.

            >>>    my_file1 = "SsdKH2jhdf345S0M3UID"
            >>>    my_file2 = "K34Ssd5H2jhdfS0M3UID"
            >>>    files_result = graph.query(Query().start_at([my_file1, my_file1]).emit("Files", ["Metadata"]))

            The response will look similar to this:

            >>> {
            >>>   "R": {
            >>>     "Files": [
            >>>       {
            >>>         "U": "M1wR2dhMTkiBzAxUzJPYBS",
            >>>         "T": "_FileEntry",
            >>>         "C": {
            >>>           "Metadata": {
            >>>             "LastSavedBy": "Word 2016",
            >>>             "Author": "Jon Doe",
            >>>           }
            >>>         }
            >>>       },
            >>>       {
            >>>         "U": "dcBDxXDebzMP9rXBmguJvj",
            >>>         "T": "_FileEntry",
            >>>         "C": {
            >>>           "Metadata": {
            >>>             "LastSavedBy": "Word 2016",
            >>>             "Author": "Jon Doe",
            >>>           }
            >>>         }
            >>>       }
            >>>     ]
            >>>   },
            >>>   "MS": 0.1937
            >>> }

        See Also:
            *EmitWithEdges*

        Args:
            emit_key: Key, under which the results are written to the output. Calling *Emit* with a different *emit_key* adds another collection of nodes to the output under that key.
            fields: Fields to fetch from the emitted nodes in this collection.

        """
        current_emit = {"emitKey": emit_key}
        if fields is not None:
            {"emitKey": emit_key}.update({"fields": fields})
        self.query.append({"op": "Emit", "args": current_emit})
        return self

    def emit_count(self, emit_key: str) -> 'Query':
        """
        Adds the count of the current collection of nodes to the output under the given key.


        Examples:

            1. *Query*: Create a new query.

            2. *StartAt*: Sets the current collection of nodes to the given files.

            4. *EmitCount*: Adds the count of the the current collection of nodes to the output under the given key.

            5. *graph.Query*: Run the query.

            >>>    my_file1 = "SsdKH2jhdf345S0M3UID"
            >>>    my_file2 = "K34Ssd5H2jhdfS0M3UID"
            >>>    files_result = graph.query(Query().start_at([my_file1, my_file1]).emit_count("FilesCount"))

            The response will look similar to this:

            >>> {
            >>>   "R": {},
            >>>   "C": {
            >>>     "FilesCount": 2
            >>>   },
            >>>   "MS": 0.4819
            >>> }

        See Also:
            *QueryResult*

        Args:
            emit_key: The key to add the count of the current collection of nodes to the output.

        """
        self.query.append({"op": "EmitCount", "args": {"emitKey": emit_key}})
        return self

    def emit_with_edges(self, emit_key: str, fields: List[str] = None) -> 'Query':
        """

        Adds the current collection to the final output under the given emit_key. Adds all **outgoing** edges of the emitted node to the emitted output.

        Examples:

            1. *Query*: Create a new query.

            2. *StartAt*: Sets the current collection of nodes to the given files.

            4. *EmitWithEdges*: Adds these files to the emitted output under the key "Files" and fetches the field "Metadata" form the current nodes ("Files").

            5. *graph.Query*: Run the query.

            >>>    my_file1 = "SsdKH2jhdf345S0M3UID"
            >>>    my_file2 = "K34Ssd5H2jhdfS0M3UID"
            >>>    files_result = graph.query(Query().start_at([my_file1, my_file1]).emit_with_edges("Files"))

            The response will look similar to this:

            >>> {
            >>>   "R": {
            >>>     "Files": [
            >>>       {
            >>>         "U": "dcBDxXDebzMP9rXBmguJvj",
            >>>         "T": "_FileEntry",
            >>>         "E": [
            >>>           {
            >>>             "N": "_Folder",
            >>>             "U": "RootFoLder111111111111",
            >>>             "T": "_ParentFolder"
            >>>           }
            >>>         ]
            >>>       },
            >>>       {
            >>>         "U": "M1wR2dhMTkiBzAxUzJPYBS",
            >>>         "T": "_FileEntry",
            >>>         "E": [
            >>>           {
            >>>             "N": "_Folder",
            >>>             "U": "RootFoLder111111111111",
            >>>             "T": "_ParentFolder"
            >>>           }
            >>>         ]
            >>>       }
            >>>     ]
            >>>   },
            >>>   "MS": 0.1749
            >>> }


        Args:
            emit_key: Key, under which the results are written to the output. Calling *Emit* with a different *emit_key* adds another collection of nodes to the output under that key.
            fields: Fields to fetch from the emitted nodes in this collection.

        """
        current_emit_with_edges = {"emitKey": emit_key}
        if fields is not None:
            current_emit_with_edges.update({"fields", fields})
        self.query.append({"op": "EmitWithEdges", "args": current_emit_with_edges})
        return self

    def of_type(self, node_type: str) -> 'Query':
        """
        Filters the current collection of nodes by removing nodes that are **not** of the given node type.

        Args:
            node_type:
        """
        self.query.append({"op": "OfType", "args": {"nodeType": node_type}})
        return self

    def of_types(self, node_types: str) -> 'Query':
        """
        Filters the current collection of nodes by removing nodes that are **not** of any of the given node types.

        Args:
            node_types:
        """
        self.query.append({"op": "OfTypes", "args": {"nodeTypes": node_types}})
        return self

    def except_type(self, node_type: str) -> 'Query':
        """
        Filters the current collection of nodes by removing nodes that are of the given node type.

        Args:
            node_type:
        """
        self.query.append({"op": "ExceptType", "args": {"nodeType": node_type}})
        return self

    def except_types(self, node_types: List[str]) -> 'Query':
        """
        Filters the current collection of nodes by removing nodes that are of any of the given node types.

        Args:
            node_types:
        """
        self.query.append({"op": "ExceptTypes", "args": {"nodeTypes": node_types}})
        return self

    def is_related_to_type(self, n: Union[str, List[str]]) -> 'Query':
        """
        Filters the current collection of nodes by removing nodes that do **not** have any outgoing edge to the given node type(s).

        Args:
            n: node type(s)

        """
        if isinstance(n, str):
            self.query.append({"op": "IsRelatedTo", "args": {"nodeType": n}})
        elif isinstance(n, list) and isinstance(n[0], str):
            self.query.append({"op": "IsRelatedTo", "args": {"nodeTypes": n}})
        else:
            raise ValueError
        return self

    def is_related_to(self, n: Union[Node, List[Node]], assume_bidirectional_edges: bool = True) -> 'Query':
        """
        Filters the current collection of nodes by removing nodes that do **not** have any outgoing edge to the given node(s).
        If *assumeBidirectionalEdges* is set to True, also removes nodes, that do have an outgoing edge, but the target node does not have an edge back.

        Args:
            n: node(s)
            assume_bidirectional_edges:

        """
        if isinstance(n, Node):
            self.query.append(
                {"op": "IsRelatedTo", "args": {"node": n, "assumeBidirectionalEdges": assume_bidirectional_edges}})
        elif isinstance(n, list) and isinstance(n[0], Node):
            self.query.append(
                {"op": "IsRelatedTo", "args": {"nodes": n, "assumeBidirectionalEdges": assume_bidirectional_edges}})
        else:
            raise ValueError
        return self

    def is_not_related_to_type(self, n: Union[str, List[str]]) -> 'Query':
        """
        Filters the current collection of nodes by removing nodes that do have any outgoing edge to the given node type(s).

        Args:
            n: node type(s)
        """
        if isinstance(n, str):
            self.query.append({"op": "IsNotRelatedTo", "args": {"nodeType": n}})
        elif isinstance(n, list) and isinstance(n[0], str):
            self.query.append({"op": "IsNotRelatedTo", "args": {"nodeTypes": n}})
        else:
            raise ValueError
        return self

    def is_not_related_to(self, n: Union[Node, List[Node]], assume_bidirectional_edges: bool = True) -> 'Query':
        """
        Filters the current collection of nodes by removing nodes that do have any outgoing edge to the given node(s).
        If *assumeBidirectionalEdges* is set to True, only removes nodes, that have an outgoing edge to the given node(s) *and* the given node(s) have an edge back.

        Args:
            n: node(s)
            assume_bidirectional_edges:
        """
        if isinstance(n, Node):
            self.query.append(
                {"op": "IsNotRelatedTo", "args": {"node": n, "assumeBidirectionalEdges": assume_bidirectional_edges}})
        elif isinstance(n, list) and isinstance(n[0], Node):
            self.query.append(
                {"op": "IsNotRelatedTo", "args": {"nodes": n, "assumeBidirectionalEdges": assume_bidirectional_edges}})
        else:
            raise ValueError
        return self

    def sort_by_timestamp(self, oldest_first: bool = True) -> 'Query':
        """
        Sorts the current collection of nodes (and by extension the emitted results) by the timestamp.

        Notes:
        For files the timestamp is set to the last modified date, by default.
        For nodes, the timestamp is the created timestamp or a manually provided one.

        Args:
            oldest_first: Reverts the ordering.
        """
        self.query.append({"op": "SortByTimestamp", "args": {"oldestFirst": oldest_first}})
        return self

    def sort_by_connectivity(self, most_connected_first: bool = True) -> 'Query':
        """
        Sorts the current collection of nodes (and by extension the emitted results) by the number of outgoing edges.

        Args:
            most_connected_first:
        """
        self.query.append({"op": "SortByConnectivity", "args": {"mostConnectedFirst": most_connected_first}})
        return self
