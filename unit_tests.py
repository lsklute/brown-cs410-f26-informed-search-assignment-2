from importlib.resources import path
import unittest
from typing import Optional, Any
from maze import Maze
from search_algorithm import SearchAlgorithm
from search import BFS, DFS
from directed_graph import DirectedGraph
from undirected_graph import UndirectedGraph

class IOTest(unittest.TestCase):
    """
    Tests IO for bfs and dfs implementations. Contains basic/trivial test cases.

    Each test instatiates a Maze object and tests the bfs and dfs algorithms on it.
    Note: The tests currently are only testing if the algorithms start and end at the
    correct locations and if the path returned is the correct length (optional).

    You may wish to add path validity checks. How do you know if a path is valid nor not?
    Your path should not teleport you, move through a wall, or go through a cell more than once.
    Maybe you should test for this... We certainly will during grading!

    These tests are not exhaustive and do not check if your implementation follows the
    algorithm correctly. We encourage you to create your own tests as necessary.
    """

    #Note: I am adding my tests for validiity here, so anytime I run check_maze it checks if it is valid 
    def _check_maze(self, algorithm: SearchAlgorithm[Any], maze: Maze, length: Optional[int] = None) -> None:
        """
        Test algorithm on a Maze
        algorithm: SearchAlgorithm instance to test
        maze: Maze to test algorithm on
        length: length that the path returned from algorithm should be.
                Think about why this argument is optional, and when you should provide it. 
                A: When there are multiple paths to the goal and when I know the shortest one (which is only for BFS)
        """
        solution = algorithm.search(maze)
        self.assertIsNotNone(solution.path, "Algorithm should find a path")

        path = solution.path
        self.assertEqual(path[0], maze.get_start_state(),
                         "Path should start with the start state")
        self.assertTrue(maze.is_goal_state(path[-1]),
                        "Path should end with the goal state")
        if length:
            self.assertEqual(solution.path_length(), length,
                             f"Path length should be {length}")

        # Check that the path only contains valid moves
        for i in range(len(path)-1):
                    self.assertIn(path[i+1], maze.get_successors(path[i]), "Path should only contain valid moves")

        # Check that the path does not contain duplicate states
        self.assertTrue(len(set(path))==len(path), "Path should not contain duplicate states")

         

    def test_bfs(self) -> None:
        """
        Test BFS on a variety of mazes."""
        single_cell_maze = Maze(1, 1)
        self._check_maze(BFS(), single_cell_maze, 1)

        two_by_two_maze = Maze(2, 2)
        self._check_maze(BFS(), two_by_two_maze, 3)

        large_maze = Maze(10, 10)
        self._check_maze(BFS(), large_maze)

        rectangular_maze = Maze(5, 10)
        self._check_maze(BFS(), rectangular_maze)

        giant_maze = Maze(30, 30)
        self._check_maze(BFS(), giant_maze)

    def test_dfs(self) -> None:
        """
        Test DFS on a variety of mazes.
        """
        single_cell_maze = Maze(1, 1)
        self._check_maze(DFS(), single_cell_maze, 1)

        two_by_two_maze = Maze(2, 2)
        self._check_maze(DFS(), two_by_two_maze, 3)

        large_maze = Maze(10, 10)
        self._check_maze(DFS(), large_maze)

        rectangular_maze = Maze(5, 10)
        self._check_maze(DFS(), rectangular_maze)

        giant_maze = Maze(30, 30)
        self._check_maze(DFS(), giant_maze)
        


    

class GraphTest(unittest.TestCase):
    """
    Example tests for UndirectedGraph, meant to show the general workflow for
    testing bfs/dfs on a SearchProblem you build by hand (as opposed to a
    randomly-generated Maze):

      1. Build a small graph where you already know the right answer.
      2. Sanity-check the SearchProblem methods directly (get_start_state,
         is_goal_state, get_successors).
      3. Run the algorithm and check the path it returns.
    """

    def _check_problem(self, algorithm: SearchAlgorithm[Any],
                        problem: UndirectedGraph, length: Optional[int] = None) -> None:
        """
        Same idea as IOTest._check_maze, but generalized to any SearchProblem
        (here, an UndirectedGraph) instead of just a Maze.
        """
        
        solution = algorithm.search(problem)

        self.assertIsNotNone(solution.path, "Algorithm should find a path")

        path = solution.path
        self.assertEqual(path[0], problem.get_start_state(),
                         "Path should start with the start state")
        self.assertTrue(problem.is_goal_state(path[-1]),
                        "Path should end with the goal state")
        if length:
            self.assertEqual(solution.path_length(), length,
                             f"Path length should be {length}")

         # Check that the path only contains valid moves
        for i in range(len(path)-1):
                    self.assertIn(path[i+1], problem.get_successors(path[i]), "Path should only contain valid moves")

        # Check that the path does not contain duplicate states
        self.assertTrue(len(set(path))==len(path), "Path should not contain duplicate states")

    def _make_graph(self) -> UndirectedGraph:
        # A small graph shaped like:
        #
        #   0 --- 1 --- 2
        #         |
        #         3 --- 4 (goal)
        #
        # matrix[i][j] holds the edge cost between i and j, or None if there
        # is no edge. Because the graph is undirected, the matrix is
        # symmetric: matrix[i][j] is not None iff matrix[j][i] is not None.
        matrix = [
            [None, 1,    None, None, None],  # 0: connects to 1
            [1,    None, 1,    1,    None],  # 1: connects to 0, 2, 3
            [None, 1,    None, None, None],  # 2: connects to 1
            [None, 1,    None, None, 1],     # 3: connects to 1, 4
            [None, None, None, 1,    None],  # 4: connects to 3
        ]
        return UndirectedGraph(matrix, goal_indices={4}, start_state=0)

    
    def _make_graph_directed(self) -> DirectedGraph:
        """
        Directed graph, 5 nodes to check bigger graphs 
        """

        # A small graph shaped like:
        #
        #   0 --- 1 --- 2 --- 4 (goal)
        #         |
        #         3 
        #         |
        #         5
        matrix = [
            [None, 1,    None, None, None,None],  # 0: connects to 1
            [None,    None, 1,    1,    None,None],  # 1: connects to 2, 3
            [None, None,    None, None, 1,None],  # 2: connects to 4
            [None, None,    None, None, None,1],  # 3: connects to 5
            [None, None, None, None,    None,None],  # 4: connects to none
            [None,None,None,None,None,None] #5: connects to none
        ]
        return DirectedGraph(matrix, goal_indices={3}, start_state=0)


 
    def _make_graph_directed_start_is_goal(self) -> DirectedGraph:
        """
        Directed graph, start state is a goal state
        """
            # A small graph shaped like:
            #
            #   0 --- 1 --- 2 --- 4 (goal)
            #         |
            #         3 
            #
        matrix = [
            [None, 1,    None, None, None],  # 0: connects to 1
            [None,    None, 1,    1,    None],  # 1: connects to 2, 3
            [None, None,    None, None, None],  # 2: connects to 4
            [None, None,    None, None, None],  # 3: connects to none
            [None, None, None, None,    None],  # 4: connects to none
        ]
        return DirectedGraph(matrix, goal_indices={0}, start_state=0)

    def _make_graph_directed_no_goal(self) -> DirectedGraph:
        """ 
        Directed graph, NO goal state 
        """
            # A small graph shaped like:
            #
            #   0 --- 1 --- 2 --- 4 
            #         |
            #         3 
            #
        matrix = [
            [None, 1,    None, None, None],  # 0: connects to 1
            [None,    None, 1,    1,    None],  # 1: connects to 2, 3
            [None, None,    None, None, None],  # 2: connects to 4
            [None, None,    None, None, None],  # 3: connects to none
            [None, None, None, None,    None],  # 4: connects to none
        ]
        return DirectedGraph(matrix, goal_indices=None, start_state=0)

   
    def _make_graph_cycles(self) -> UndirectedGraph:
        """
        Undirected graph, with cycles 
        """
        # A small graph shaped like:
        #
        #   0 --- 1 
        #   |     |
        #      2  (goal)
        #
        # matrix[i][j] holds the edge cost between i and j, or None if there
        # is no edge. Because the graph is undirected, the matrix is
        # symmetric: matrix[i][j] is not None iff matrix[j][i] is not None.
        matrix = [
            [None, 1,    None, None, None],  # 0: connects to 1
            [1,    None, 1,    None,    None],  # 1: connects to 0, 2
            [1, 1,    None, None, None],  # 2: connects to 0,1
        ]
        return UndirectedGraph(matrix, goal_indices={2}, start_state=0)

    def _make_graph_multi_goals(self) -> UndirectedGraph:
        """
        Undirected graph, with multiple goal states
        """
        # A small graph shaped like:
        #
        #   0 --- 1 --- 2 (goal)
        #         |
        #         3 --- 4 (goal)
        #
        # matrix[i][j] holds the edge cost between i and j, or None if there
        # is no edge. Because the graph is undirected, the matrix is
        # symmetric: matrix[i][j] is not None iff matrix[j][i] is not None.
        matrix = [
            [None, 1,    None, None, None],  # 0: connects to 1
            [1,    None, 1,    1,    None],  # 1: connects to 0, 2, 3
            [None, 1,    None, None, None],  # 2: connects to 1
            [None, 1,    None, None, 1],     # 3: connects to 1, 4
            [None, None, None, 1,    None],  # 4: connects to 3
        ]
        return UndirectedGraph(matrix, goal_indices={2,4}, start_state=0)

    def _make_graph_multi_goals_directed(self) -> DirectedGraph:
            """
            Directed graph, with multiple goal states
            """
            # A small graph shaped like:
            #
            #   0 --- 1 --- 2 (goal)
            #         |
            #         3 --- 4 (goal)
            #
            matrix = [
                [None, 1,    None, None, None],  # 0: connects to 1
                [None,    None, 1,    1,    None],  # 1: connects to  2, 3
                [None, None,    None, None, None],  # 2: connects to None
                [None, None,    None, None, 1],     # 3: connects to 4
                [None, None, None, None,    None],  # 4: connects to None
            ]
            return DirectedGraph(matrix, goal_indices={2,4}, start_state=0)

    
    def _make_graph_disconnected(self) -> UndirectedGraph:
        """
        Undirected graph, disconnected nodes but goal node is reachable
        """
        # A small graph shaped like:
        #
        #   0 --- 1 --- 2 (goal)
        #         |
        #         3   4 
        #
        matrix = [
            [None, 1,    None, None, None],  # 0: connects to 1
            [1,    None, 1,    1,    None],  # 1: connects to 0, 2, 3
            [None, 1,    None, None, None],  # 2: connects to 1
            [None, 1,    None, None, None],    # 3: connects to 1
            [None, None, None, None,    None],  # 4: connects to none
        ]
        return UndirectedGraph(matrix, goal_indices={2}, start_state=0)


    def _make_graph_disconnected_is_goal(self) -> UndirectedGraph:
        """
        Undirected graph, disconnected node but the disconnected node is a goal state
        """
        # A small graph shaped like:
        #
        #   0 --- 1 --- 2 
        #         |
        #         3   4 (goal)
        #
    
        matrix = [
            [None, 1,    None, None, None],  # 0: connects to 1
            [1,    None, 1,    1,    None],  # 1: connects to 0, 2, 3
            [None, 1,    None, None, None],  # 2: connects to 1
            [None, 1,    None, None, None],    # 3: connects to 1
            [None, None, None, None,    None],  # 4: connects to none
        ]
        return UndirectedGraph(matrix, goal_indices={4}, start_state=0)

    def test_undirected_graph_methods(self) -> None:
        """Sanity-check the SearchProblem interface before trusting bfs/dfs on it."""
        graph = self._make_graph()

        self.assertEqual(graph.get_start_state(), 0)
        self.assertFalse(graph.is_goal_state(0))
        self.assertTrue(graph.is_goal_state(4))
        self.assertEqual(graph.get_successors(1), {0, 2, 3})
        self.assertEqual(graph.get_successors(4), {3})

    def test_undirected_graph_bfs(self) -> None:
        """Test BFS on an undirected graph."""
        graph = self._make_graph()
        # The only path from 0 to 4 is 0 -> 1 -> 3 -> 4, so bfs and dfs
        # should both find it; here we know bfs's path is also the shortest.
        self._check_problem(BFS(), graph, length=4)

    def test_undirected_graph_dfs(self) -> None:
        """Test DFS on an undirected graph."""
        graph = self._make_graph()
        # dfs isn't guaranteed to find the *shortest* path, just *a* valid
        # one, so we don't check length here -- just that it's a real path.
        self._check_problem(DFS(), graph)

    #TODO: Add more tests for DirectedGraph and UndirectedGraph, including edge cases like:
    # - Graphs with cycles
    # - Graphs with multiple goal states

    def test_undirected_graph_cycles_bfs(self) -> None:
        """Test BFS on an undirected graph with cycles."""
        graph = self._make_graph_cycles()
        # dfs isn't guaranteed to find the *shortest* path, just *a* valid
        # one, so we don't check length here -- just that it's a real path.
        self._check_problem(BFS(), graph)

    def test_undirected_graph_cycles_dfs(self) -> None:
        """Test DFS on an undirected graph with cycles."""
        graph = self._make_graph_cycles()
        self._check_problem(DFS(), graph)

    def test_undirected_graph_multi_goals_bfs(self) -> None:
        """Test BFS on an undirected graph with multiple goal states."""
        graph = self._make_graph_multi_goals()
        self._check_problem(BFS(), graph, 3 ) # should get index 2 and not index 4 since it is closer to the start state

    def test_undirected_graph_multi_goals_dfs(self) -> None:
        """Test DFS on an undirected graph with multiple goal states."""
        graph = self._make_graph_multi_goals()
        self._check_problem(DFS(), graph ) #length is iirelevant for DFS here

    def test_directed_graph_multi_goals_bfs(self) -> None:
        """Test BFS on a directed graph with multiple goal states."""
        graph = self._make_graph_multi_goals_directed()
        self._check_problem(BFS(), graph, 3 ) # should get index 2 and not index 4 since it is closer to the start state

    def test_directed_graph_multi_goals_dfs(self) -> None:
        """Test DFS on a directed graph with multiple goal states."""
        graph = self._make_graph_multi_goals_directed()
        self._check_problem(DFS(), graph ) #length is iirelevant for DFS here

    def test_directed_graph_start_is_goal(self) -> None:
        """Test DFS on a directed graph where the start node is the goal state."""
        graph = self._make_graph_directed_start_is_goal()
        self._check_problem(DFS(), graph , 1) 
    
    def test_undirected_graph_disconnected_is_goal_bfs(self) -> None:
        """Test BFS on an undirected graph with a disconnected node that is a goal state."""
        graph = self._make_graph_disconnected_is_goal()
        solution = BFS().search(graph)
        self.assertIsNone(solution.path, "No path should exist to an unreachable goal")

    def test_undirected_graph_disconnected_is_goal_dfs(self) -> None:
            """Test DFS on an undirected graph with a disconnected node that is a goal state."""
            graph = self._make_graph_disconnected_is_goal()
            solution = DFS().search(graph)
            self.assertIsNone(solution.path, "No path should exist to an unreachable goal")

    def test_undirected_graph_disconnected_dfs(self) -> None:
            """Test DFS on an undirected graph with a disconnected node BUT is not the goal state."""
            graph = self._make_graph_disconnected()
            self._check_problem(DFS(), graph)


    def test_directed_graph_no_goal_bfs(self) -> None:
        """Test BFS on a directed graph with no goal state."""
        graph = self._make_graph_directed_no_goal()
        with self.assertRaises(ValueError):
           BFS().search(graph)

if __name__ == "__main__":
    unittest.main()