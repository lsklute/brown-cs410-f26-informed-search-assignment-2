import random
import signal
import matplotlib.pyplot as plt
from typing import Callable, Dict, List, Optional, Union
from informed_search import AStar
from search_solution import SearchSolution
from tile_game import TileGame, HeuristicTileGame, TileGameState
from heuristics import admissible_heuristic, inadmissible_heuristic, my_heuristic
import numpy as np
import tqdm
import multiprocessing


class _SearchTimeoutError(Exception):
    pass


def _raise_search_timeout(signum, frame) -> None:
    raise _SearchTimeoutError()


def _search_with_timeout(tile_game: HeuristicTileGame, cutoff_time: float = 10) -> Optional[SearchSolution]:
    """
    Runs AStar().search(tile_game), giving up (and returning None) if it
    hasn't finished within cutoff_time seconds. Some size/heuristic
    combinations are computationally intractable for a real A* search (e.g.
    a weak or near-admissible heuristic on a large board), so callers should
    treat None as "skip this data point" rather than guessing in advance
    which combinations are too slow.

    Uses a SIGALRM-based timeout (Unix only) in the same process, rather
    than a subprocess: spawning a fresh interpreter (re-importing
    matplotlib/numpy/tqdm) for every single search call is prohibitively
    slow across the hundreds of calls these comparisons make.
    """
    old_handler = signal.signal(signal.SIGALRM, _raise_search_timeout)
    signal.setitimer(signal.ITIMER_REAL, cutoff_time)
    try:
        return AStar().search(tile_game)
    except _SearchTimeoutError:
        return None
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old_handler)


class ScaledHeuristic:
    def __init__(self, base_heuristic: Callable[[TileGameState], float], scale: float) -> None:
        self.base_heuristic = base_heuristic
        self.scale = scale

    def __call__(self, state: TileGameState) -> float:
        return int(self.scale * self.base_heuristic(state))


def completion_rate(heuristic: Callable[[TileGameState], float], num_trials: int = 10, cutoff_time: int = 10) -> List[float]:
    """
    make completion rate graph
    """
    # set random seed so that games are consistent
    random.seed(2)
    # Define symbols for matplotlib scatter plot to use for each tile size
    solved = []
    size = 2
    while True:
        num_successful = 0
        num_failed = 0
        print(f'Running for size {size}...')
        for i in tqdm.tqdm(range(num_trials)):
            tg = TileGame(size)
            tile_game = HeuristicTileGame(
                size, heuristic, start_state=tg.get_start_state())
            # Make new thread to run astar, cutoff after cutoff_time
            p = multiprocessing.Process(target=AStar().search, args=(tile_game,))
            p.start()
            p.join(timeout=cutoff_time)
            if p.is_alive():
                # If thread has not ended, it has exceeded cutoff time and is a failure
                p.terminate()
                num_failed += 1
            else:
                num_successful += 1
        solved.append(num_successful / (num_successful + num_failed))
        size += 1
        if num_successful == 0:
            break
    return solved


def make_completion_rate_plot() -> None:
    lambdas = np.geomspace(1, 5, 8, endpoint=True)
    heuristics = [ScaledHeuristic(admissible_heuristic, l) for l in lambdas]
    for i, heuristic in enumerate(heuristics):
        print(f'Running for lambda={lambdas[i]:.2f}...')
        solved = completion_rate(heuristic)
        plt.plot(list(range(2, len(solved) + 2)), solved,
                 label=fr'$\lambda$={lambdas[i]:.2f}')
    plt.legend()
    plt.ylabel('Completion Rate')
    plt.xlabel('Board Size')
    plt.title('Completion Rate of A* Search with Varying Heuristics (Cutoff=10s)')
    plt.savefig('completion_rate.jpg')
    plt.clf()


def compare_problem_sizes(heuristics: Dict[str, Callable[[TileGameState], Union[int, float]]], sizes: range = range(2, 5), num_trials: int = 5, cutoff_time: float = 10) -> None:
    random.seed(2)
    markers = ['o', 's', 'D', 'v', '^', '<']
    colors = plt.get_cmap('tab10')

    plt.figure(figsize=(10, 6))

    for i, size in enumerate(sizes):
        results = {h: [] for h in heuristics}
        for _ in tqdm.tqdm(range(num_trials)):
            tg = TileGame(size)

            for heuristic in heuristics:
                print(f'Running for size {size} and heuristic {heuristic}...')
                heuristic_fn = heuristics[heuristic]
                if heuristic_fn(tg.get_start_state()) is None:
                    print(f"Heuristic {heuristic} not implemented (returns None)")
                    continue
                tile_game = HeuristicTileGame(
                    size, heuristic_fn, start_state=tg.get_start_state())
                solution = _search_with_timeout(tile_game, cutoff_time)
                if solution is None:
                    print(f"Skipping size {size}, heuristic {heuristic}: exceeded {cutoff_time}s cutoff")
                    continue
                if solution.path is not None:
                    results[heuristic].append((solution.path_length(), solution.stats.num_nodes_expanded))

        for j, heuristic in enumerate(heuristics):
            if len(results[heuristic]) == 0:
                continue
            heuristic_results = results[heuristic]
            average_length = np.mean([x[0] for x in heuristic_results])
            average_nodes = np.mean([x[1] for x in heuristic_results])

            plt.scatter(average_nodes, average_length,
                        marker=markers[i], color=colors(j/len(heuristics)), # type: ignore
                        label=f'λ={heuristic}, size {size}')

    plt.ylabel('Length of Solution')
    plt.xlabel('# States Expanded')
    plt.title('A* Search Performance with Varying Size')
    plt.yscale('log')
    plt.xscale('log')
    plt.xlim(1, 10e6)

    # Create a simplified legend
    handles, labels = plt.gca().get_legend_handles_labels()
    by_heuristic = {}
    by_size = {}
    for handle, label in zip(handles, labels):
        heuristic, size = label.split(', ')
        if heuristic not in by_heuristic:
            by_heuristic[heuristic] = handle
        if size not in by_size:
            by_size[size] = handle

    # Add heuristic legend
    first_legend = plt.legend(by_heuristic.values(), by_heuristic.keys(),
                              title="Heuristics", loc='upper left', bbox_to_anchor=(1, 1))
    plt.gca().add_artist(first_legend)

    # Add size legend
    plt.legend(by_size.values(), by_size.keys(),
               title="Board Sizes", loc='upper left', bbox_to_anchor=(1, 0.4))

    plt.tight_layout()
    plt.savefig('heuristics_varying_size.jpg', bbox_inches='tight')
    plt.clf()


def compare_lambdas(admissible_heuristic: Callable[[TileGameState], float], size: int = 3, num_trials: int = 1000) -> None:
    """
    Compares the performance of A* search using varying levels of inadmissibility.

    Args:
        admissible_heuristic (Callable[[TileGameState], int]):
            The admissible heuristic function to modify.
        size (int, optional):
            The size of the board to test, default is 3.
        num_trials (int, optional):
            The number of trials to run for each lambda value, default is 1000.

    Saves:
        A scatter plot comparing the performance (solution length vs. states expanded)
        of A* search with different lambda-modified heuristics, saved as 'heuristics.jpg'.
    """
    lambdas = np.geomspace(1, 5, 8, endpoint=True)
    states_expanded = {l: [] for l in lambdas}
    path_lengths = {l: [] for l in lambdas}
    my_heuristic_implemented = True

    plt.figure(figsize=(10, 6))

    for _ in tqdm.tqdm(range(num_trials)):
        tg = TileGame(size)
        for l in lambdas:
            heuristic = ScaledHeuristic(admissible_heuristic, l)
            tile_game = HeuristicTileGame(
                size, heuristic, start_state=tg.get_start_state())
            solution = _search_with_timeout(tile_game)
            if solution is None:
                continue
            states_expanded[l].append(solution.stats.num_nodes_expanded)
            if solution.path is not None:
                path_lengths[l].append(solution.path_length())

        # If my_heuristic is implemented, collect stats
        if not my_heuristic_implemented:
            continue
        if tile_game and my_heuristic(tile_game.get_start_state()) is None:
            print("My heuristic, not yet implemented (returns None)")
            my_heuristic_implemented = False
        else:
            heuristic_fn = my_heuristic
            tile_game = HeuristicTileGame(
                size, heuristic_fn, start_state=tg.get_start_state())

            solution = _search_with_timeout(tile_game)
            if solution is None:
                continue
            states_expanded[l].append(solution.stats.num_nodes_expanded)
            if solution.path is not None:
                path_lengths[l].append(solution.path_length())

    for l in lambdas:
        plt.scatter(np.mean(states_expanded[l]), np.mean(
            path_lengths[l]), label=r'$\lambda$={:.2f}'.format(l))

    if my_heuristic_implemented:
        plt.scatter(np.mean(states_expanded[l]), np.mean(
            path_lengths[l]), label='my_heuristic'.format(l))

    plt.legend()
    plt.ylabel('Length of Solution')
    plt.xlabel('# States Expanded')
    plt.xscale('log')
    plt.title(
        f'A* Search Performance with Different Heuristics on Size {size} Games')
    plt.tight_layout()
    plt.savefig('heuristics.jpg', bbox_inches='tight')
    plt.clf()


def main() -> None:
    """
    Runs comparisons of heuristics and creates performance plots.

    This function is the entry point of the script, calling other functions to generate
    plots comparing the performance of heuristics on TileGames. Specific comparisons
    can be toggled by commenting or uncommenting lines within this function.
    """
    # make_completion_rate_plot()
    compare_lambdas(admissible_heuristic)
    # lambdas = np.geomspace(1, 5, 8, endpoint=True)
    # heuristics = {'{:.2f}'.format(l): ScaledHeuristic(
    #     admissible_heuristic, l) for l in lambdas}
    # compare_problem_sizes(heuristics, sizes=range(2, 6))


if __name__ == "__main__":
    main()