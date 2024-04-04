Author        : Anubhav Anand
Language used : python
Objective     : Creating Pathfinding Visualization Tool

This is a Python project that provides a graphical user interface for visualizing various pathfinding algorithms. It allows users to create obstacles, set start and target points, and observe how different algorithms find paths from the start to the target point.

++ Features

- Graphical representation of a grid-based environment.
- Ability to set start and target points by left-clicking on grid cells.
- Creation and removal of obstacles by left-clicking and right-clicking respectively.
- Visualization of pathfinding algorithms including:
  - Dijkstra's Algorithm
  - Depth First Search (DFS)
  - Breadth First Search (BFS)
  - A* Algorithm
- Real-time updating of the grid based on user interactions and algorithm executions.
- Informative alerts for when no path is found.

++ Requirements

- Python 3.x
- Pygame library
- Tkinter library (for alert messages)

++ How to Use

1. Install Python 3.x if not already installed.
2. Install the required libraries by running `pip install pygame` and `pip install tk` in your terminal or command prompt.
3. Clone or download this repository to your local machine.
4. Navigate to the project directory.
5. Run the `main.py` file using Python: `python main.py`.
6. Follow the on-screen instructions to interact with the visualization:
   - Left-click to set start and target points, and create obstacles.
   - Right-click to remove obstacles.
   - Press keys 1-4 to choose different pathfinding algorithms.
    
        Keys for executing pathfinding methods :
        ->      1   -   Djikstra Algorithm
        ->      2   -   Depth First Search Algorithm
        ->      3   -   Breadth First Algorithm
        ->      4   -   A*(star) Algorithm
        ->      0   -   Stop

   - Press 'r' to reset the grid.

++ Notes

- This project is intended for educational purposes to demonstrate pathfinding algorithms and their visualization.
- Feel free to modify the code or contribute to the project as needed.
- For any issues or suggestions, please open an issue in the GitHub repository.