import argparse
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from maze import Maze
from search import BFS, DFS


class MazeSearchVisualizer:
    """
    Displays the traversal of BFS or DFS through a maze.
    """

    def __init__(self, maze: Maze, algorithm_name: str, delay: float = 0.08):
        self.maze = maze
        self.algorithm_name = algorithm_name
        self.delay = delay

        # Turn on interactive plotting
        plt.ion()

        self.fig, self.ax = plt.subplots(figsize=(10, 8))

        self._draw_maze()

        # Marker showing the state currently being explored
        self.current_marker, = self.ax.plot(
            [],
            [],
            marker="o",
            markersize=9,
            color="orange"
        )

        self.ax.set_title(
            f"{self.algorithm_name}: Searching..."
        )

        plt.show(block=False)
        plt.pause(0.1)


    def _draw_maze(self):
        """
        Draws the fixed maze walls.
        """

        for row in range(self.maze.height):
            for col in range(self.maze.width):

                room = self.maze.board[row][col]

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

        self.ax.set_xlim(0, self.maze.width)
        self.ax.set_ylim(0, self.maze.height)

        self.ax.invert_yaxis()

        self.ax.set_xticks([])
        self.ax.set_yticks([])

        # Show start and goal
        start_row, start_col = self.maze.start_state.location
        goal_row, goal_col = self.maze.goal_state.location

        self.ax.text(
            start_col + 0.5,
            start_row + 0.5,
            "S",
            ha="center",
            va="center",
            fontweight="bold"
        )

        self.ax.text(
            goal_col + 0.5,
            goal_row + 0.5,
            "G",
            ha="center",
            va="center",
            fontweight="bold"
        )


    def visit(self, state):
        """
        Called whenever BFS/DFS explores a state.
        """

        row, col = state.location

        # Shade explored cell
        explored_cell = Rectangle(
            (col, row),
            1,
            1,
            facecolor="lightblue",
            alpha=0.5,
            edgecolor="none"
        )

        self.ax.add_patch(explored_cell)

        # Move current-state marker
        self.current_marker.set_data(
            [col + 0.5],
            [row + 0.5]
        )

        self.ax.set_title(
            f"{self.algorithm_name}: Exploring {state.location}"
        )

        self.fig.canvas.draw_idle()
        plt.pause(self.delay)


    def show_solution(self, path, solution):
        """
        Draws the final solution path after search finishes.
        """

        if not path:
            self.ax.set_title(
                f"{self.algorithm_name}: No solution found"
            )
            return

        path_x = [
            state.location[1] + 0.5
            for state in path
        ]

        path_y = [
            state.location[0] + 0.5
            for state in path
        ]

        # Draw final solution
        self.ax.plot(
            path_x,
            path_y,
            color="red",
            linewidth=3,
            marker="o",
            markersize=5
        )

        # Remove current-search marker
        self.current_marker.set_data([], [])

        self.ax.set_title(
            f"{self.algorithm_name}: Solution Found"
        )

        self.fig.canvas.draw_idle()

        # Stop interactive mode and keep window open
        plt.ioff()
        plt.show()


def main():

    parser = argparse.ArgumentParser(
        description="Solve a maze using BFS or DFS"
    )

    parser.add_argument(
        "--size",
        type=int,
        default=10,
        help="Width and height of the maze"
    )

    parser.add_argument(
        "--algorithm",
        choices=["bfs", "dfs"],
        required=True,
        help="Search algorithm to use"
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=0.08,
        help="Delay between visualization steps"
    )

    args = parser.parse_args()

    # --------------------------------------------------
    # Generate the maze
    # --------------------------------------------------

    maze = Maze(
        args.size,
        args.size
    )

    algorithm_name = args.algorithm.upper()

    # --------------------------------------------------
    # Create visualization
    # --------------------------------------------------

    visualizer = MazeSearchVisualizer(
        maze,
        algorithm_name,
        delay=args.delay
    )

    # --------------------------------------------------
    # Temporarily wrap is_goal_state so that every state
    # checked by the search gets displayed.
    # --------------------------------------------------

    original_is_goal_state = maze.is_goal_state

    def visualized_goal_test(state):

        visualizer.visit(state)

        return original_is_goal_state(state)

    maze.is_goal_state = visualized_goal_test

    # --------------------------------------------------
    # Run student's algorithm
    # --------------------------------------------------

    if args.algorithm == "bfs":
        solution = BFS().search(maze)

    else:
        solution = DFS().search(maze)

    # --------------------------------------------------
    # Print results
    # --------------------------------------------------

    print(f"\n{algorithm_name} Path:")
    print(solution.path)

    print(f"\n{algorithm_name} Statistics:")
    print(solution)

    # --------------------------------------------------
    # Show final solution
    # --------------------------------------------------

    visualizer.show_solution(
        solution.path,
        solution
    )


if __name__ == "__main__":
    main()