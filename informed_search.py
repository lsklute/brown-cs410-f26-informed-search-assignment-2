from itertools import count
from queue import PriorityQueue
from typing import Dict

from search_problem import State
from search_solution import SearchSolution
from search_algorithm import SearchAlgorithm, reconstruct_path
from heuristic_search_problem import HeuristicSearchProblem
from tile_game import HeuristicTileGame, TileGame
from heuristics import admissible_heuristic, inadmissible_heuristic


class AStar(SearchAlgorithm[State]):
    """
    A* search algorithm implementation.

    Searches a HeuristicSearchProblem (a SearchProblem with costs and a
    heuristic) and returns a SearchSolution.
    """

    name = "A*"

    def search(self, problem: HeuristicSearchProblem[State]) -> SearchSolution[State]:
        solution = SearchSolution()

        #TODO: Implement the A* search algorithm to find a solution to the given problem.
        # Review the class notes and the assignment handout for guidance on how to implement A*.
        # You may use the provided reconstruct_path function to help build the solution path once a goal state is found.
        # Update `solution.stats` (e.g. num_nodes_generated, num_nodes_expanded, max_frontier_size) as you search.
        # Once you find a goal state, set `solution.path` and `solution.cost`, then return `solution`.
        # If the frontier empties out without finding a goal, `solution.path` stays None -- just return `solution`.

        return solution

def main() -> None:
    dim = 3
    tg = TileGame(dim)
    # admissible_tile_game = HeuristicTileGame(
    #     dim, start_state=tg.get_start_state(), heuristic=admissible_heuristic)
    inadmissible_tile_game = HeuristicTileGame(
        dim, start_state=tg.get_start_state(), heuristic=inadmissible_heuristic)

    solution = AStar().search(inadmissible_tile_game)
    print("path (inadmissible):")
    tg.print_pretty_path(solution.path)
    print("stats (inadmissible):", solution)
    print('-'*110)


if __name__ == "__main__":
    main()
