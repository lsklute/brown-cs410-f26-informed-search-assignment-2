import argparse
from queue import LifoQueue
from typing import List, Optional, Tuple
from search_problem import SearchProblem, State
from search_solution import SearchSolution
from search_algorithm import SearchAlgorithm, reconstruct_path
from tile_game import TileGame
from search import BFS, DFS
import tqdm


class IDS(SearchAlgorithm[State]):
    """
    Performs Iterative Deepening Search (IDS) on the given problem: repeatedly
    runs a depth-limited search with an increasing cutoff depth until a
    solution is found.
    """

    name = "IDS"

    def search(self, problem: SearchProblem[State]) -> SearchSolution[State]:
        solution = SearchSolution()

        cutoff_depth = 1
        while True:
            found, path, num_expanded, num_generated, frontier_size = \
                self._depth_limited_search(problem, cutoff_depth)

            solution.stats.num_nodes_expanded += num_expanded
            solution.stats.num_nodes_generated += num_generated
            solution.stats.max_frontier_size = max(solution.stats.max_frontier_size, frontier_size)

            if found:
                solution.path = path
                solution.cost = solution.path_length() - 1  # uniform move cost
                return solution

            cutoff_depth += 1

    def _depth_limited_search(self, problem: SearchProblem[State], depth: int) -> Tuple[bool, Optional[List[State]], int, int, int]:
        """
        Implement depth-limited search.

        Input:
            problem - the SearchProblem to solve
            depth - the maximum depth to which the search should explore

        Output:
            found - whether a goal state was reached within the depth limit
            path - the path to the goal, or None if not found
            num_states_expanded - the number of states expanded during the search
            num_states_generated - the number of states generated during the search
            max_frontier_size - the maximum size of the frontier during the search
        """
        frontier = LifoQueue()
        start_state = problem.get_start_state()
        frontier.put(start_state)
        parents_dict = {start_state: None}
        depth_of_state = {start_state: 0}
        num_states_expanded = 0
        num_states_generated = 1
        max_frontier_size = 1

        while not frontier.empty():
            # update size of frontier stat
            max_frontier_size = max(max_frontier_size, frontier.qsize())

            # get state from open set
            state = frontier.get()

            if problem.is_goal_state(state):
                # Backtracking: use parents dictionary to construct path
                # Path will be in reverse order at first (state is currently the goal state)
                path = [state]

                # Loop until a node with no parents is reached (the start state)
                while state and parents_dict[state] is not None:
                    parent = parents_dict[state]
                    state = parent
                    path.append(state)

                # Reverse path
                path.reverse()
                return True, path, num_states_expanded, num_states_generated, max_frontier_size
            else:
                # Expand state (get successors)
                successors = problem.get_successors(state)
                num_states_expanded += 1

                visited = parents_dict
                for child in successors:
                    if child in visited:
                        # If we've visited a node before, it may have been at a different depth
                        # Check if we need to lower the depth
                        temp_depth = depth_of_state[state] + 1
                        if temp_depth < depth_of_state[child]:
                            # If a node was reached at a different depth,
                            # update parent dictionary (to guarantee we use the faster path)
                            depth_of_state[child] = temp_depth
                            parents_dict[child] = state
                            if depth_of_state[child] <= depth:
                                frontier.put(child)
                    else:
                        # First time visiting a node
                        depth_of_state[child] = depth_of_state[state] + 1
                        parents_dict[child] = state
                        num_states_generated += 1
                        if depth_of_state[child] <= depth:
                            frontier.put(child)

        return False, None, num_states_expanded, num_states_generated, max_frontier_size


def compile_stats(size: int, n_trials: int, ids_only: bool) -> dict:
    """
    Collect stats for BFS, DFS, and IDS on TileGame problems.
    This method is intended to be used for comparing the performance of blind-search algorithms

    Args:
        size (int): The size of the TileGame problem.
        n_trials (int): The number of trials to run for each algorithm.
        ids_only (bool): Whether to run only IDS or all algorithms.

    Returns:
        Dict[str, List[float]]: A dictionary containing the average statistics for each algorithm.

    Note:
        The statistics are: the number of states expanded, the maximum frontier size, and the average path length.
    """
    # 0 = states expanded, 1 = max frontier size
    stats = {'bfs': [0., 0., 0.], 'dfs': [0., 0., 0.], 'ids': [0., 0., 0.]}
    if n_trials <= 0:
        return stats

    for _ in tqdm.tqdm(range(n_trials)):
        tile_game = TileGame(size)

        if not ids_only:  # run all algos
            # BFS
            bfs_solution = BFS().search(tile_game)
            stats['bfs'][0] += bfs_solution.stats.num_nodes_expanded
            stats['bfs'][1] += bfs_solution.stats.max_frontier_size
            if bfs_solution.path is not None:
                stats['bfs'][2] += bfs_solution.path_length()

            # DFS
            dfs_solution = DFS().search(tile_game)
            stats['dfs'][0] += dfs_solution.stats.num_nodes_expanded
            stats['dfs'][1] += dfs_solution.stats.max_frontier_size
            if dfs_solution.path is not None:
                stats['dfs'][2] += dfs_solution.path_length()
        print("starting ID")
        # IDS
        ids_solution = IDS().search(tile_game)
        stats['ids'][0] += ids_solution.stats.num_nodes_expanded
        stats['ids'][1] += ids_solution.stats.max_frontier_size
        if ids_solution.path is not None:
            stats['ids'][2] += ids_solution.path_length()

    avg_stats = {algo: [val[0] / n_trials, val[1] / n_trials, val[2] / n_trials]
                 for algo, val in stats.items()}
    return avg_stats


def main() -> None:
    """
    Run 3 different search algorithms (BFS, DFS, IDS) on TileGame problems.
    The results of each search are printed to the console.
    """
    parser = argparse.ArgumentParser(
        description='Run search algorithms on TileGame problems.')
    parser.add_argument('--size', type=int, default=2,
                        help='Size of the TileGame (default: 2)')
    parser.add_argument('--trials', type=int, default=10,
                        help='Number of trials to run (default: 10)')
    parser.add_argument('--ids', action='store_true', help='Run IDS only')

    args = parser.parse_args()
    SIZE = args.size
    N_TRIALS = args.trials
    if args.ids:
        print(f"Running IDS on {N_TRIALS} {SIZE}x{SIZE} TileGame problems...")
        avg_stats = compile_stats(SIZE, N_TRIALS, True)
        print("IDS Average States Expanded: ", avg_stats['ids'][0])
        print("IDS Average Max Frontier Size: ", avg_stats['ids'][1])
        print("IDS Average Path Length: ", avg_stats['ids'][2])
    else:
        print(f"Running BFS, DFS, IDS on {N_TRIALS} {SIZE}x{SIZE} TileGame problems...")
        avg_stats = compile_stats(SIZE, N_TRIALS, False)
        print("BFS Average States Expanded: ", avg_stats['bfs'][0])
        print("DFS Average States Expanded: ", avg_stats['dfs'][0])
        print("IDS Average States Expanded: ", avg_stats['ids'][0])
        print("BFS Average Max Frontier Size: ", avg_stats['bfs'][1])
        print("DFS Average Max Frontier Size: ", avg_stats['dfs'][1])
        print("IDS Average Max Frontier Size: ", avg_stats['ids'][1])
        print("BFS Average Path Length: ", avg_stats['bfs'][2])
        print("DFS Average Path Length: ", avg_stats['dfs'][2])
        print("IDS Average Path Length: ", avg_stats['ids'][2])


if __name__ == "__main__":
    main()
