import math
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

    dimension = len(state.board)
    total_distance = 0
    for i in range(dimension):
        for j in range(dimension):
            num = state.board[i][j]
            row = (num-1) // dimension
            col = (num-1) % dimension
            total_distance += abs(row-i) + abs(col-j)
    #As long as I divide by lambda, (defined in handout) then it should be admissable
    return total_distance /2
    


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
    heuristic_value = 0.0
    dim= len(state.board) #these are squares, so how many rows is how many cols
    num_states= dim * dim 
    prob_state_is_right= 1/num_states 
    for i in range(dim):
        for j in range(dim):
            num = state.board[i][j]
            goal_row = (num-1) // dim
            goal_col = (num-1) % dim
            row_distance= abs(goal_row - i)
            col_distance= abs(goal_col - j)
            # i can make like a triangle with this and guess with the hypotanous distance squared 
            #NOTE: THE HYPOTANOUS IS AN INADMISSABLE HEURISTIC SINCE IT IS SQUARED VALUE: INDEPENDENT OF THE PROBABILITY CONSTANT, I JUST WANTED TO INCLUDE THE PROBABILITY :)
            total_moves_away= (row_distance)**2 + (col_distance) **2
            heuristic_value += total_moves_away * (1+prob_state_is_right)
    return heuristic_value