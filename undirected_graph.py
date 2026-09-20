from typing import List, Optional, Set

from search_problem import SearchProblem

class UndirectedGraph(SearchProblem[int]):
    """
    DGraph holds a reciprocated djacency matrix, which represents an undirected graph. See the handout for more
    information on adjacency matrices.

    DGraph implements the SearchProblem Abstract Base Class. A state in DGraph is just an integer
    representing a node in the graph.
    """

    def __init__(
        self,
        matrix,
        goal_indices,
        start_state=0,
    ):
        self.matrix = matrix
        self.goal_indices = goal_indices
        self.start_state = start_state

    def get_start_state(self):
        return self.start_state

    def is_goal_state(self, state):
        if self.goal_indices is None:
            raise ValueError("No goal states defined for this problem")
        return state in self.goal_indices

    def get_successors(self, state):
        row = self.matrix[state]
        successors = set()

        for index, cost in enumerate(row):
            if cost is not None:
                successors.add(index)

        return successors