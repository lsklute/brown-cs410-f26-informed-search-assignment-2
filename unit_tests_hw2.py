import unittest
from typing import Optional, Callable

from search import BFS, DFS
from tile_game import TileGame, TileGameState, HeuristicTileGame
from informed_search import AStar
from blind_search import IDS
from heuristics import admissible_heuristic, inadmissible_heuristic


class IOTest(unittest.TestCase):
    """
    Tests IO for search implementations. Contains basic/trivial test cases.

    Each test function instantiates a search problem (TileGame) and tests if the three test case
    contains the solution, the start state is in the solution, the end state is in the
    solution and, if applicable, if the length of the solutions are the same.

    These tests are not exhaustive and do not check if your implementation follows the
    algorithm correctly. We encourage you to create your own tests as necessary.
    """

    def _check_tilegame(self, start_state: TileGameState, goal_state: TileGameState, length: Optional[int] = None, heuristic: Optional[Callable[[TileGameState], float]] = None) -> None:
        """
        Test algorithm on a TileGame
        algorithm: algorithm to test
        start_state: start state of the TileGame
        goal_state: goal state of the TileGame
        length: length that the path returned from algorithm should be. 
                Think about why this argument is optional, and when you should provide it.
        heuristic: heuristic to use for the TileGame (admissible or inadmissible)
        """
        # Ensure start_state and goal_state dimensions are n x n
        self.assertEqual(len(start_state.board), len(start_state.board[0]), "Dimensions must be n x n")
        dim = len(start_state.board)
        
        # Initialize the TileGame with the provided start and goal states, and the given heuristic
        game = HeuristicTileGame(dim, start_state=start_state, goal_state=goal_state, heuristic=heuristic)

        # Run the algorithm (e.g., A* or any other search algorithm) on the game
        solution = AStar().search(game)
        self.assertIsNotNone(solution.path, "Algorithm should find a path")

        # Check that the path starts and ends with the correct states
        self.assertEqual(solution.path[0], start_state, "Path should start with the start state")
        self.assertEqual(solution.path[-1], goal_state, "Path should end with the goal state")
        # If a path length is provided, verify the length matches the expected value
        if length:
            self.assertEqual(solution.path_length(), length, f"Path length should be {length}")
        
    def test_astar(self) -> None:
        start_state = TileGameState(((4, 1, 3), (7, 2, 6), (9, 5, 8)))
        goal_state = TileGameState(((1, 2, 3), (4, 5, 6), (7, 8, 9)))
        self._check_tilegame(start_state, goal_state, length=7, heuristic=admissible_heuristic)

    # TODO: add tests here!


if __name__ == "__main__":
    unittest.main()