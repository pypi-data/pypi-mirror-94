from dataclasses import dataclass
from datetime import timedelta
from typing import Dict, List

from .. import EmittedNode


@dataclass
class QueryResults:
    """
    Response of a query from the Curiosity instance.
    """
    R: Dict[str, List[EmittedNode]]
    C: Dict[str, int]

    MS: float

    @property
    def elapesd(self) -> timedelta:
        """Time it took to run the query in milliseconds."""
        return timedelta(milliseconds=self.MS)

    def get_emitted(self, emit_key: str) -> List[EmittedNode]:
        """
        Get a list of emitted nodes which were emitted qith with the given ``emit_key``.

        See Also:
            :py:meth:`~src.curiosity.query.query.Query.emit`

        Args:
            emit_key:

        Returns: List of emitted nodes

        """
        return self.R[emit_key]

    def get_emitted_count(self, emit_key: str) -> int:
        """


        Args:
            emit_key:

        Returns:

        """
        return self.C[emit_key]
