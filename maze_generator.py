import random
import argparse
from typing import Set, Optional

from sympy import true
from maze import Maze, MazeState, MazeRoom
from search_problem import SearchProblem
from search import BFS, DFS
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class MazeGenerator(SearchProblem[MazeState]):
    """
    Generates a maze as a search problem 

    This class initializes a maze with walls surrounding every cell. The maze 
    generation process can be driven by applying search algorithms like BFS or DFS, 
    which explore the maze and create paths by visiting cells and removing walls. 
    It keeps track of the visited cells and checks when all cells have been 
    visited (i.e., when the maze is fully generated).

    Attributes:
        width (int): The width of the maze in terms of the number of cells.
        height (int): The height of the maze in terms of the number of cells.
        board (Tuple[Tuple[MazeRoom]]): A 2D list representing the maze grid where each cell is a MazeRoom.
        start_state (MazeState): The starting state of the maze, where the generation begins.
        visited_cells_count (int): The count of cells that have been visited during maze generation.
        total_cells (int): The total number of cells in the maze.
    """
    def __init__(self, width: int, height: int) -> None:
        """
        Initializes the maze generator with a given width and height.

        Args:
            width (int): The width of the maze.
            height (int): The height of the maze.
        """
        self.width = width
        self.height = height

        #TODO: Initialize the maze board with MazeRoom objects
        self.board = [[MazeRoom() for col in range(self.width)] for row in range(self.height)]  # A 2D list representing the maze grid
        start_row= random.randint(0, height - 1)  # Randomly select a starting row
        start_col= random.randint(0, width - 1)  # Randomly select
        self.start_state = MazeState(self.board, (start_row, start_col))  # Set the starting state of the maze
        self.board[start_row][start_col].visited = True

        self.visited_cells_count=1 #I can do this now or during goal state skip the first one
        #TODO: Set the starting state of the maze (randomly select a cell)
        #TODO: Initialize the count of visited cells and total cells in the maze  
        self.total_cells = self.width * self.height  # Total number of cells in the maze

    # TODO: Fill out this method
    def get_start_state(self) -> MazeState:
        """
        Returns the start state of the maze.

        This method retrieves the initial starting state of the maze, which is
        typically used as the entry point for maze generation or solving algorithms.

        Returns:
            MazeState: The initial state of the maze.
        """
        return self.start_state  # Return the starting state of the maze
        #TODO: Implement the logic to return the start state of the maze.
        

    # TODO: Fill out this method
    def is_goal_state(self, state: MazeState) -> bool:
        """
        Determines whether the goal state of the maze has been reached.

        This method checks if all cells in the maze have been visited, indicating
        that the maze generation or solving process is complete.

        Args:
            state (MazeState): The current state of the maze.

        Returns:
            bool: True if all cells have been visited and the goal state is reached,
                False otherwise.
        """
        for row in self.board:
            for room in row:
                if not room.visited:
                    return False

        return True 

        #TODO: Implement the logic to check if all cells have been visited.
        

    # TODO: Fill out this method (Hint: we provide two helper functions below that may be of use)
    def get_successors(self, state: MazeState) -> Set[MazeState]:
        """
        Generates the successor states from the current state in the maze.

        This method explores the possible moves from the current state by checking 
        adjacent cells in the four cardinal directions (north, south, east, west). 
        It only considers cells that have not been visited and are within the maze's 
        boundaries. When a valid move is found, the wall between the current cell 
        and the adjacent cell is removed, and the adjacent cell is marked as visited.

        Args:
            state (MazeState): The current state of the maze.

        Returns:
            set[MazeState]: A set of successor MazeState objects.
        """
        # TODO: Implement the logic to generate successor states based on the current state.
        successors = set()
        row, col = state.location[0], state.location[1]
        for direction in ["north", "south", "east", "west"]:
            if direction == "north":
                next_row, next_col = row - 1, col
            elif direction == "south":
                next_row, next_col = row + 1, col
            elif direction == "east":
                next_row, next_col = row, col + 1
            else: #west, changed this from elif to else so that line 121 could access the next_row and next_col variables
                next_row, next_col = row, col - 1

            if self.is_in_range(next_row, next_col):
                neighbor_room = self.board[next_row][next_col]
                if not neighbor_room.visited:
                    # Remove the wall between the current room and the neighbor room
                    setattr(self.board[row][col], direction, 0)
                    opposite_direction = self.opposite_direction(direction)
                    setattr(neighbor_room, opposite_direction, 0)
                    neighbor_room.visited = True
                    self.visited_cells_count+=1
                    successors.add(MazeState(self.board, (next_row, next_col)))
        return successors

# /////////////////////////////// Don't Edit Beyond this Line! /////////////////////////////////////

    def is_in_range(self, row: int, col: int) -> bool:
        """
        Checks whether a given position is within the bounds of the maze.

        This method verifies if the specified row and column indices fall within 
        the valid range of the maze's dimensions.

        Args:
            row (int): The row index to check.
            col (int): The column index to check.

        Returns:
            bool: True if the position is within the maze's boundaries, False otherwise.
        """
        return 0 <= row < self.height and 0 <= col < self.width

    def opposite_direction(self, direction: str) -> str:
        """
        Returns the opposite direction of the given direction.

        This method maps a given cardinal direction (north, south, east, west) 
        to its opposite direction.

        Args:
            direction (str): The direction for which the opposite is needed.

        Returns:
            str: The opposite direction.
        """
        opposites = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}
        return opposites[direction]

class MazeGenerationVisualizer:
    """
    Animates maze generation as BFS or DFS explores cells and removes walls.
    """

    def __init__(
        self,
        generator: MazeGenerator,
        algorithm_name: str,
        delay: float = 0.08
    ):
        self.generator = generator
        self.algorithm_name = algorithm_name
        self.delay = delay

        plt.ion()

        self.fig, self.ax = plt.subplots(figsize=(10, 8))

        # Initial frame: every cell still has all four walls
        self.draw()

        plt.show(block=False)
        plt.pause(0.1)

    def draw(self, current_state: Optional[MazeState] = None):
        """
        Redraws the entire maze using its current wall configuration.
        """

        # Important: clear old wall lines so removed walls disappear visually
        self.ax.clear()

        board = self.generator.board

        for row in range(self.generator.height):
            for col in range(self.generator.width):

                room = board[row][col]

                # Shade visited cells
                if room.visited:
                    visited_cell = Rectangle(
                        (col, row),
                        1,
                        1,
                        facecolor="lightblue",
                        alpha=0.5,
                        edgecolor="none"
                    )

                    self.ax.add_patch(visited_cell)

                # Draw the walls that currently still exist
                if room.north == 1:
                    self.ax.plot(
                        [col, col + 1],
                        [row, row],
                        color="black"
                    )

                if room.south == 1:
                    self.ax.plot(
                        [col, col + 1],
                        [row + 1, row + 1],
                        color="black"
                    )

                if room.east == 1:
                    self.ax.plot(
                        [col + 1, col + 1],
                        [row, row + 1],
                        color="black"
                    )

                if room.west == 1:
                    self.ax.plot(
                        [col, col],
                        [row, row + 1],
                        color="black"
                    )

        # Highlight the state currently being expanded
        if current_state is not None:
            row, col = current_state.location

            self.ax.plot(
                col + 0.5,
                row + 0.5,
                marker="o",
                markersize=9,
                color="orange"
            )

            self.ax.set_title(
                f"{self.algorithm_name}: Generating from {current_state.location}"
            )
        else:
            self.ax.set_title(
                f"{self.algorithm_name}: Initial Maze"
            )

        self.ax.set_xlim(0, self.generator.width)
        self.ax.set_ylim(0, self.generator.height)

        self.ax.invert_yaxis()

        self.ax.set_xticks([])
        self.ax.set_yticks([])

        self.fig.canvas.draw_idle()
        plt.pause(self.delay)

    def finish(self):
        """
        Displays the completed maze and keeps the window open.
        """

        self.draw()

        self.ax.set_title(
            f"{self.algorithm_name}: Maze Generation Complete"
        )

        self.fig.canvas.draw_idle()

        plt.ioff()
        plt.show()

def main() -> None:
    """
    Main function to generate a maze using BFS or DFS.
    """

    parser = argparse.ArgumentParser(
        description="Run maze generator"
    )

    parser.add_argument(
        "--size",
        type=int,
        default=10,
        help="Size of the maze (default: 10)"
    )

    parser.add_argument(
        "--algorithm",
        choices=["bfs", "dfs"],
        default="dfs",
        help="Algorithm used to generate the maze"
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=0.08,
        help="Delay between visualization steps"
    )

    args = parser.parse_args()

    SIZE = args.size
    algorithm_name = args.algorithm.upper()

    # -----------------------------------------
    # Create an initially fully-walled maze
    # -----------------------------------------

    generator = MazeGenerator(SIZE, SIZE)

    # -----------------------------------------
    # Open visualization BEFORE search starts
    # -----------------------------------------

    visualizer = MazeGenerationVisualizer(
        generator,
        algorithm_name,
        delay=args.delay
    )

    # -----------------------------------------
    # Wrap get_successors
    #
    # Student get_successors() performs the
    # actual wall-removal logic.
    # -----------------------------------------

    original_get_successors = generator.get_successors

    def visualized_get_successors(state):

        successors = original_get_successors(state)

        # At this point, the student's method has
        # modified the walls, so redraw the maze.
        visualizer.draw(state)

        return successors

    generator.get_successors = visualized_get_successors

    # -----------------------------------------
    # Run student's BFS or DFS
    # -----------------------------------------

    if args.algorithm == "bfs":
        solution = BFS().search(generator)

    else:
        solution = DFS().search(generator)

    # -----------------------------------------
    # Print results
    # -----------------------------------------

    print(f"\n{algorithm_name} maze generation")

    print("\nGeneration Path:")
    print(solution.path)

    print("\nStatistics:")
    print(solution)

    # -----------------------------------------
    # Leave completed maze visible
    # -----------------------------------------

    visualizer.finish()

if __name__ == "__main__":
    main()