from itertools import count
from queue import PriorityQueue
import time
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
        """
        Only going to check if the successor is the goal state once it is the current_state to ensure it is
        the most optimal path. If not then I could get a suboptimal path I believe.
        """
        solution = SearchSolution()
        
        stats= solution.stats
        start_time = time.perf_counter()   #  start the clock

        current_state= problem.get_start_state() # Initialize the current state
        
        parents: Dict[State, State] = {} #maps the current state to its parent state, used for reconstructing the path
        tie_breaker = count()  # Counter to break ties in the priority queue

        state_to_total: Dict[State, float] = {} #maps the current state to the total cost function
        state_to_total[current_state] = 0 # Add the start state to the dictionary with a total cost of 0
        open_queue= PriorityQueue() # Initialize the priority queue for the open set
        open_queue.put((state_to_total[current_state], next(tie_breaker), current_state)) # Add the start state to the priority queue with a priority ( 0 )
        closed_set= set() # Initialize the closed set to keep track of explored states
        while(not open_queue.empty()):
            current_state = open_queue.get()[2] #2nd index gets the state
            if(problem.is_goal_state(current_state)):
                solution.path = reconstruct_path(parents,current_state, problem) # Reconstruct the path to the goal state
                solution.cost = state_to_total[current_state] # Set the cost of the solution to the total cost of the goal state
                stats.runtime_seconds= time.perf_counter() - start_time   

                return solution
            if(current_state in closed_set):
                continue
            closed_set.add(current_state) #I know it is not a goal state (at least through the path A* is currently on)
            stats.num_nodes_expanded+=1
            for successor in problem.get_successors(current_state):
                new_cost = problem.get_cost(current_state, successor) + \
                state_to_total[current_state]
                # if I have been here and I already found something as good or better dont waste time
                if(successor in state_to_total and \
                   state_to_total[successor] <= new_cost): 
                    continue # get out of this successor loop 
                #but if I either have not been here before or this is a lower cost than before then add it 
                stats.num_nodes_generated+=1
                state_to_total[successor]= new_cost
                parents[successor] = current_state #this child to the parent
                heuristic_cost = problem.heuristic(successor)
                total_cost = new_cost + heuristic_cost
                #now I add it to the priority queue 
                open_queue.put((total_cost, next(tie_breaker), successor ))
                stats.max_frontier_size = max(stats.max_frontier_size,open_queue.qsize())  # Update the maximum frontier size

        stats.runtime_seconds= time.perf_counter() - start_time   
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
