from dataclasses import dataclass
from typing import Generic, List, Optional

from search_problem import State


@dataclass
class SearchStats:
    """
    Runtime statistics collected while a SearchAlgorithm searches a
    SearchProblem.
    """

    num_nodes_generated: int = 0
    num_nodes_expanded: int = 0
    max_frontier_size: int = 0
    runtime_seconds: float = 0.0


class SearchSolution(Generic[State]):
    """
    The result of running a SearchAlgorithm on a SearchProblem.

    A SearchAlgorithm always returns one of these, even when no path to a
    goal exists -- in that case `path` is None. The algorithm's name lives
    on the SearchAlgorithm that produced this solution (see
    search_algorithm.py), not here. Every algorithm (BFS, DFS, IDS, A*)
    produces the same shape of result.
    """

    def __init__(self, path: Optional[List[State]] = None) -> None:
        self.path: Optional[List[State]] = path
        self.stats: SearchStats = SearchStats()

        # Total path cost. Left None by cost-agnostic algorithms (BFS/DFS);
        # populated by cost-aware algorithms (IDS, A*).
        self.cost: Optional[float] = None

    def path_length(self) -> Optional[int]:
        """
        Number of states in the path, or None if no path was found.
        """
        return len(self.path) if self.path is not None else None

    def __repr__(self) -> str:
        return (
            f"SearchSolution(path_length={self.path_length()}, cost={self.cost}, {self.stats})"
        )
