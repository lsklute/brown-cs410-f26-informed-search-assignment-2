from collections import deque
from typing import Dict, List

from search_problem import SearchProblem, State
from search_solution import SearchSolution
from search_algorithm import SearchAlgorithm, reconstruct_path
from maze import Maze


class BFS(SearchAlgorithm[State]):
    """
    Performs Breadth-First Search (BFS) on a given search problem, using a
    FIFO queue as the frontier so that states are explored in order of
    increasing distance from the start state.
    """

    name = "BFS"

    def search(self, problem: SearchProblem[State]) -> SearchSolution[State]:
        solution = SearchSolution(problem)
        search_stats = solution.stats  # Access the SearchStats object to update statistics
        already_explored = set()  # Set to keep track of explored states
        queue= deque()  # frontier for BFS
        current_state = problem.get_start_state()  # Initialize the current state
        dictionary: Dict[State, State] = {} #maps the current state to its parent state, used for reconstructing the path
        queue.append(current_state)  # Add the start state to the queue
        already_explored.add(current_state)  # Mark the start state as explored

        if(problem.is_goal_state(current_state)):
            solution.path = [current_state]  # If the start state is the goal, the path is just the goal
            search_stats.num_nodes_generated += 1  
            search_stats.max_frontier_size = 1
            return solution 
        
        while(queue):
            current_state = queue.popleft()  # Move to the next state in the queue
            search_stats.num_nodes_expanded += 1  # Increment the number of nodes expanded (1 for the current node)    
            for successor in problem.get_successors(current_state):
                if successor not in already_explored:
                    dictionary[successor] = current_state  # Record the parent of the successor, given the current_state is the parent
                    queue.append(successor)  # Add successor to the queue
                    already_explored.add(successor)  # Mark successors as explored
                    search_stats.num_nodes_generated += 1  # Increment the number of nodes generated (1 for the successor )
                    search_stats.max_frontier_size = max(search_stats.max_frontier_size, len(queue))  # Update the maximum frontier size
                    if(problem.is_goal_state(successor)):
                        solution.path = reconstruct_path(dictionary, successor, problem,)  # Reconstruct the path to the goal state
                        return solution
                        
        return solution

        

class DFS(SearchAlgorithm[State]):
    """
    Performs Depth-First Search (DFS) on a given search problem, using a
    LIFO stack (not a Queue!) as the frontier so that states are explored
    depth-first.
    """

    name = "DFS"

    def search(self, problem: SearchProblem[State]) -> SearchSolution[State]:
        solution = SearchSolution(problem)
        search_stats = solution.stats  # Access the SearchStats object to update statistics
        already_explored = set()  # Set to keep track of explored states
        stack=  [] # frontier for DF
        current_state = problem.get_start_state()  # Initialize the current state
        dictionary: Dict[State, State] = {} #maps the current state to its parent state, used for reconstructing the path
        stack.append(current_state)  # Add the start state to the queue
        already_explored.add(current_state)  # Mark the start state as explored
        
        if(problem.is_goal_state(current_state)):
            solution.path = [current_state]  # If the start state is the goal, the path is just the goal
            search_stats.num_nodes_generated += 1  
            search_stats.max_frontier_size = 1
            return solution 
                
        while(stack):
            current_state = stack.pop()  # Move to the next state in the stack
            search_stats.num_nodes_expanded += 1  # Increment the number of nodes expanded (1 for the current node)    
            for successor in problem.get_successors(current_state):
                if successor not in already_explored:
                    dictionary[successor] = current_state  # Record the parent of the successor, given the current_state is the parent
                    stack.append(successor)  # Add successor to the queue
                    already_explored.add(successor)  # Mark successors as explored
                    search_stats.num_nodes_generated += 1  # Increment the number of nodes generated (1 for the successor )
                    search_stats.max_frontier_size = max(search_stats.max_frontier_size, len(stack))  # Update the maximum frontier size
                    if(problem.is_goal_state(successor)):
                        solution.path = reconstruct_path(dictionary, successor, problem,)  # Reconstruct the path to the goal state
                        print("DFS found path: ", solution.path)
                        return solution
                                
        return solution


############### SANDBOX ###############
def main() -> None:
    # Initialize the maze and generate it based on given dimensions
    print("Generated Maze:")
    width, height = 30, 30
    maze = Maze(width, height)

    # Run BFS and DFS to find paths
    print("BFS Path:")
    bfs = BFS()
    bfs_solution = bfs.search(maze)
    print(f"BFS found path: {bfs_solution.path}")
    print(f"BFS stats: {bfs_solution}")
    maze.visualize_maze(path=bfs_solution.path, algorithm_name=bfs.name)

    print("DFS Path:")
    dfs = DFS()
    dfs_solution = dfs.search(maze)
    print(f"DFS found path: {dfs_solution.path}")
    print(f"DFS stats: {dfs_solution}")
    maze.visualize_maze(path=dfs_solution.path, algorithm_name=dfs.name)


if __name__ == "__main__":
    main()
