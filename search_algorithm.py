from abc import ABC, abstractmethod
from typing import Dict, Generic, List

from search_problem import SearchProblem, State
from search_solution import SearchSolution


class SearchAlgorithm(ABC, Generic[State]):
    """
    A SearchAlgorithm searches a SearchProblem and returns a SearchSolution
    describing the path to a goal (or None, if no such path exists) and
    statistics about the search.
    """

    name: str = ""

    @abstractmethod
    def search(self, problem: SearchProblem[State]) -> SearchSolution[State]:
        pass


def reconstruct_path(parents: Dict[State, State], end: State, problem: SearchProblem[State]) -> List[State]:
    """
    Reconstructs the path from the start state to the given end state.

    This function traces back through the parent mapping to build the complete path
    from start to goal. The path is initially built in reverse order (goal to start)
    and then reversed to give the correct order.

    Args:
        parents (Dict[State, State]): A dictionary mapping each state to its predecessor in the search.
        end (State): The goal state to trace back from.
        problem (SearchProblem[State]): The search problem to solve.

    Returns:
        List[State]: The reconstructed path from the start state to the goal state.
    """
    reverse_path = []
    while end != problem.get_start_state():
        reverse_path.append(end)
        end = parents[end]
    reverse_path.append(problem.get_start_state())
    reverse_path.reverse()
    return reverse_path
