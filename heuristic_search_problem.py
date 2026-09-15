from abc import abstractmethod
from search_problem import SearchProblem, State

class HeuristicSearchProblem(SearchProblem[State]):
    """
    Abstract base class for heuristic search problems.

    This class extends SearchProblem with edge costs and a heuristic
    function that estimates the cost to reach the goal state from a given
    state. get_successors(state) is unchanged (still Set[State]) so BFS/DFS
    keep working unmodified; get_cost supplies the edge weight and
    heuristic the goal-distance estimate that A* needs.

    Methods:
        get_cost(state: State, successor: State) -> float:
            Abstract method that must be implemented by subclasses to provide
            the cost of the edge from state to successor.

        heuristic(state: State) -> float:
            Abstract method that must be implemented by subclasses to provide
            a heuristic estimate for a given state.
    """
    @abstractmethod
    def get_cost(self, state: State, successor: State) -> float:
        """
        Cost of the edge from `state` to `successor` (successor must be one
        of the states in get_successors(state)).
        """
        pass

    @abstractmethod
    def heuristic(self, state: State) -> float:
        """
        Returns a heuristic estimate of the cost to reach the goal from the given state.

        Args:
            state (State): The current state of the problem.

        Returns:
            float: The estimated cost to reach the goal from the given state.
        """
        pass
