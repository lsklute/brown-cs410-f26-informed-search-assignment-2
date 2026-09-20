# assignment-2-informed-search

### Setup

Before starting, copy your entire Assignment 1 submission into this directory:

- `directed_graph.py`
- `undirected_graph.py`
- `maze.py`
- `maze_generator.py`
- `solve_maze.py`
- `search_problem.py`
- `search_algorithm.py`
- `search.py` (your BFS and DFS implementations)
- `unit_tests.py`

None of these change for this assignment, so bring them over as-is -- don't
retype or re-implement anything from Assignment 1. The only genuinely new
work in this assignment is the A* implementation, edge costs, and heuristics
(`informed_search.py`, `heuristic_search_problem.py`, `heuristics.py`, plus
IDS in `blind_search.py`).

Your new tests for this assignment go in `unit_tests_hw2.py`, kept separate
from your Assignment 1 `unit_tests.py` so copying that file over doesn't
overwrite these new tests.

## Implementation: 
The implementation for this assighnment mostly relies on HW1, adding in A* as a search algorithm. This was implemented using priority queue and a closed set to keep track of the 
states, and a dictionary mapping the states to the costs. While I was going through the states, if the state was already visited I would continue and NOT look at its successors, but if a successor was visited then I would check if the cost of it (through this path) was cheaper and then add it to the dictionary mapping the states to the cost. 

My heuristic implementation is defined later in the tasks. My testing implementation ensures that there are enough edge cases being accounted for, and my statistics are running correctly (in a non trivial way, which i define as the style guide does )

### Task 1.2

1. B) IDS < BFS < DFS — IDS's frontier depends the current depth limit, BFS's grows with the width of the deepest level it reaches, and DFS's grows with however deep it happens to wander

2. B) IDS restarts from the root at each new depth limit, so shallow states are re-expanded once per iteration

3. D) The metrics stabilize because the variance from unusually easy or hard starting boards shrinks

4. C) IDS — it's optimal like BFS but keeps a much smaller frontier; the cost is re-expanding shallow states, which is dominated by the work at the deepest level anyway


### Task 3.1

5. C) No — a single swap moves two tiles at once, so one move reduces the remaining number of swaps by two, just not one

6. A) Divide the total Manhattan distance by 2 — since half the total is a lower bound on the moves remaining

7. B) Average number of states expanded across random boards

8. A) Whether its path length always matches BFS's

## Task 4.1

My heuristic takes into consideration how far the current state is from the goal state and the probability that the 
state is already in the right position. By knowing how many rows and columns away each state is, I used the pythagoren
theorem to calculate the length between the state and the goal state. Given that I am calculating an inadmissable 
heuristic, I took the probability that the piece was in the right place and added 1 to it, because I basically wanted the estimate to be minimum the hypotaneous, and the probability to skew that increasingly. 

### Task 4.2

My heuristic preforms similarly to the manhattan heuristic with lambda value of 3.97 (proof of inadmissibility), with
the length of the solution being roughly 10.6, and the admissable heuristic (lambda 1) has a lenght under 10: proving its suboptimality. Meanwhile, the time of search (estimated based on list of expansion size) is roughly 10 for my heuristic, and the admissable heurisitc (lambda 1), has a expansion list size greater than 10^2: proving my heuristic has higher efficiency. 


### Tests

Test method : explanation 

def test_astar(self): This is testing whether A* works with an admissable heuristic, and that the length is the shortest one. 

def test_astar_big_game(self): This tests on a bigger board whether A* works, to ensure that bigger baords can run. Though there is just 1 move it needs to compute since when I tried to test for it to be many more moves it was too computatioanlly heavy. 

def test_astart_already_solved(sel): This tests if the start is the goal, ensuring that we check before we continue to look at succesors if the current node itself is the goal (and that we start with the intended starting node).

def test_astar_and_bfs(self): This test ensures that A* and BFS have the same path length since they both should return the most optimal. This works well since I already ensured the BFS is returning correctly in the unit1 testing. Meaning if it is the same, then I know A* is working correctly too.

def test_dfs_finds_a_path(self): This test ensures that DFS returns a valid path (but since DFS does not guarentee optimality it does not check length). This was important to check that it was working properly on the tilegames board (not just the maze from hw1).

def test_ids_matches_bfs_length(self): 
Since BFS and IDS are both optimal blind searches, the lengths they return should be the same. Again, checking this against the tilegame board, and not just the mazes from hw1. 

def test_astar_admissible_vs_inadmissible_cost(self):
Testing that aqn admissabile heursitic nevers costs more than an inadmissable heursitic (this is by defintion). 

def test_astar_stats(self): Testing the stats in a non trivial way, ensuring that the number of nodes expanded for Astar is less than or equal to the number of nodes expanded for BFS. 


Collaborators:none

Hours spent on homework: 8

Known bugs: None 

AI Use Description: N/A

You must acknowledge use here and submit transcript if AI was used for portions of the assignment
