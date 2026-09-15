from typing import Optional
from tile_game import TileGameState



def admissible_heuristic(state: TileGameState) -> float:
    """
    Produces a number for the given tile game state representing
    an estimate of the cost to get to the goal state. Remember that this heuristic must be
    admissible, that is it should never overestimate the cost to reach the goal.

    Args:
        state - the tilegame state to evaluate. Consult handout for how the tilegame state is represented

    Returns: a float.
    """
    # TODO Task 3.2: Write the admissable heuristic function. 
    # You can reuse code from the inadmissible heuristic, but you will need to modify it to ensure that it is admissible.
    return 0.0


def inadmissible_heuristic(state: TileGameState) -> float:
    """
    Produces a number for the given tile game state representing
    an estimate of the cost to get to the goal state. This heuristic
    is inadmissible, meaning it can, at times, overestimate the cost-to-goal.
    This inadmissible heuristic uses the sum of all manhattan distances for 
    each tile to their goal location.

    Args:
        state - the tilegame state to evaluate. Consult handout for how the tilegame state is represented

    Returns: a float.
    """
    dimension = len(state.board)
    total_distance = 0
    for i in range(dimension):
        for j in range(dimension):
            num = state.board[i][j]
            row = (num-1) // dimension
            col = (num-1) % dimension
            total_distance += abs(row-i) + abs(col-j)
    return total_distance


def my_heuristic(state: TileGameState) -> Optional[float]:
    """
    Your implementation of an inadmissible heuristic.
    Args:
        state - the tilegame state to evaluate. Consult handout for how the tilegame state is represented

    Returns: a float (the heuristic value of state), or None if not yet implemented.
    """
    # TODO: Calculate heuristic of state
    heuristic_value = None

    return heuristic_value