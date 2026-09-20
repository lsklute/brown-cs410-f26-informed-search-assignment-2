import unittest
from typing import Optional, Callable

from search import BFS, DFS
from tile_game import TileGame, TileGameState, HeuristicTileGame
from informed_search import AStar
from blind_search import IDS
from heuristics import admissible_heuristic, inadmissible_heuristic

#Add test for when the nodes are all the same
class IOTest(unittest.TestCase):
    """
    Tests IO for search implementations. Contains basic/trivial test cases.

    Each test function instantiates a search problem (TileGame) and tests if the three test case
    contains the solution, the start state is in the solution, the end state is in the
    solution and, if applicable, if the length of the solutions are the same.

    These tests are not exhaustive and do not check if your implementation follows the
    algorithm correctly. We encourage you to create your own tests as necessary.
    """

    def _check_tilegame(self, start_state: TileGameState, goal_state: TileGameState, length: Optional[int] = None, heuristic: Optional[Callable[[TileGameState], float]] = None, alg : type = AStar) :
        """
        Test algorithm on a TileGame
        alg: algorithm to test 
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
        solution = alg().search(game)
        self.assertIsNotNone(solution.path, "Algorithm should find a path")

        # Check that the path starts and ends with the correct states
        self.assertEqual(solution.path[0], start_state, "Path should start with the start state")
        self.assertEqual(solution.path[-1], goal_state, "Path should end with the goal state")
        # If a path length is provided, verify the length matches the expected value
        if length:
            self.assertEqual(solution.path_length(), length, f"Path length should be {length}")
        return solution
        
    def test_astar(self) -> None:
        """
        Testing A* with an admissable heuristic on a solveable 3x3 board with a known optimal
        length. Verifies that A* returns this length (since it is the shortest one) not just any
        solution. 
        """
        start_state = TileGameState(((4, 1, 3), (7, 2, 6), (9, 5, 8)))
        goal_state = TileGameState(((1, 2, 3), (4, 5, 6), (7, 8, 9)))
        self._check_tilegame(start_state, goal_state, length=7, heuristic=admissible_heuristic)

    #This test does not run -> must be too big for A*
    # def test_astar_big_game_nonworking(self) -> None: 
    #     start_state = TileGameState(((4, 1, 3, 8), (7, 2, 6, 12), (9, 5, 11, 15), (10, 13, 14, 16)))
    #     goal_state = TileGameState(((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 16)))
    #     self._check_tilegame(start_state, goal_state, heuristic=admissible_heuristic) #can not calculate this length 

    def test_astar_big_game(self) -> None: 
        """
        Tests A* on a 4x4 board (different dimension), and it is only one move away from being goal state.
        This ensures that A* works for larger board sizes, and since it is just one move I know the 
        length will just be 2 (2 states are moved for 1 move). 
        """
        start_state = TileGameState(((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 16, 15)))
        goal_state = TileGameState(((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 16)))
        self._check_tilegame(start_state, goal_state, length=2, heuristic=admissible_heuristic) 
    
    def test_astart_already_solved(self) -> None:
        """
        Edge case: start state equals goal state. Verifies that A* recognizes the trivial case,
        knowing that it already got the goal. Therefor, the lenght should be 0. 
        """
        start_state = TileGameState(((1, 2, 3), (4, 5, 6), (7, 8, 9)))
        self._check_tilegame(start_state, start_state, length=0, heuristic=admissible_heuristic)

    def test_astar_and_bfs(self) -> None:
        """
        Testing that A* and BFS agree on a path length when the board is the same. Both must
        be optimal so then the length should be the same since optimality provides 1 distinct
        solution/path. This proves that A* is optimal and not suboptimal. 
        """
        start_state = TileGameState(((4, 1, 3), (7, 2, 6), (9, 5, 8)))
        goal_state = TileGameState(((1, 2, 3), (4, 5, 6), (7, 8, 9)))
        bfs_solution=self._check_tilegame(start_state, goal_state, length=7, alg=BFS)
        astar_solution= \
        self._check_tilegame(start_state, goal_state, length=7, heuristic=admissible_heuristic, alg=AStar)
        self.assertEqual(bfs_solution.path_length(), astar_solution.path_length())

    def test_dfs_finds_a_path(self) -> None:
        """
        Testing that DFS returns a valid path, but length is not checked since DFS goes not
        guarentee optimality. (This is what distinguishes DFS behavior from BFS/A*).
        """
        start_state = TileGameState(((4, 1, 3), (7, 2, 6), (9, 5, 8)))
        goal_state = TileGameState(((1, 2, 3), (4, 5, 6), (7, 8, 9)))
        self._check_tilegame(start_state, goal_state, alg=DFS)

    def test_ids_matches_bfs_length(self) -> None:
        """
        BFS and IDS are both optimal, so path lengths should be the same.
        """
        start_state = TileGameState(((4, 1, 3), (7, 2, 6), (9, 5, 8)))
        goal_state = TileGameState(((1, 2, 3), (4, 5, 6), (7, 8, 9)))
        bfs_solution = self._check_tilegame(start_state, goal_state, length=7, alg= BFS)
        ids_solution = self._check_tilegame(start_state, goal_state, length=7, alg= IDS)
        self.assertEqual(bfs_solution.path_length(), ids_solution.path_length())

    def test_astar_admissible_vs_inadmissible_cost(self) -> None:
        """
        Admissible A* should never cost more than inadmissible A*
        """
        start_state = TileGameState(((4, 1, 3), (7, 2, 6), (9, 5, 8)))
        goal_state = TileGameState(((1, 2, 3), (4, 5, 6), (7, 8, 9)))

        admissible_solution = \
            self._check_tilegame(start_state, goal_state, heuristic=admissible_heuristic)
        inadmissible_solution = \
            self._check_tilegame(start_state, goal_state, heuristic=inadmissible_heuristic)
        self.assertLessEqual(admissible_solution.cost, inadmissible_solution.cost)

    def test_astar_stats(self) -> None:
        """
        Testing that A* with an asmissible heuristic expands less than or equal to the 
        nodes on an uninformed search (BFS). 
        """
        start_state = TileGameState(((4, 1, 3), (7, 2, 6), (9, 5, 8)))
        goal_state = TileGameState(((1, 2, 3), (4, 5, 6), (7, 8, 9)))
        bfs_solution = self._check_tilegame(start_state, goal_state, length=7,alg=BFS )
        astar_solution= self._check_tilegame(start_state, goal_state, length=7, heuristic=admissible_heuristic)
        self.assertLessEqual(astar_solution.stats.num_nodes_expanded, bfs_solution.stats.num_nodes_expanded)




if __name__ == "__main__":
    unittest.main()