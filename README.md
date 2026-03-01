# Dynamic Pathfinding Agent

## Project Overview

The Dynamic Pathfinding Agent is a grid-based pathfinding simulator. It demonstrates how search algorithms find a path from a starting point to a goal while avoiding obstacles. The system also supports dynamic environments where new obstacles may appear, requiring the agent to recalculate its path in real time.

The project implements informed search algorithms and provides visual feedback so that users can observe the search process step by step.

---
## Features

### Grid Management

- Create grids of different sizes
- Add or remove obstacles by clicking on the grid
- Generate random mazes

### Visualization

- Visualize the search process
- Highlight visited nodes
- Show the final path
- Display frontier nodes during search

### Dynamic Behavior

- Dynamic obstacle handling
- Automatic path replanning
- Real-time navigation updates

### Performance Metrics

- Live metrics dashboard
- Nodes visited count
- Path cost calculation
- Execution time tracking

### Algorithm Support

- Multiple search algorithms
- Heuristic-based navigation
- Dynamic replanning capabilities

---
## Algorithms

### A Star Search

A Star Search finds the shortest path by considering:

#### Path Cost

The cost from the start node to the current node.

#### Heuristic Estimate

The estimated cost from the current node to the goal.

#### Formula

f(n) = g(n) + h(n)

Where:
g(n) is the cost from the start to the node  
h(n) is the heuristic estimate to the goal

A Star guarantees the shortest path when an admissible heuristic is used.

---
### Greedy Best First Search

Greedy Best First Search uses only the heuristic value.

#### Formula

f(n) = h(n)

This approach is faster but does not guarantee the shortest path.

---
## Heuristics

### Manhattan Distance

Used for grid movement (up, down, left, right).

Formula:
|x1 - x2| + |y1 - y2|

It calculates the total number of steps required to reach the goal in a grid.

---
### Euclidean Distance

Measures the straight-line distance between two points.

Formula:
Square root of ((x1 - x2) squared + (y1 - y2) squared)

It estimates direct distance but may not always suit grid-based movement.

---
## Dynamic Mode

When dynamic mode is enabled:

- New obstacles appear randomly
- The agent detects blockages
- The path is recalculated automatically
- Navigation adapts to changing environments

This simulates real-world dynamic navigation.

---
## Visualization

The grid uses colors to represent different states:

- Green – Final path and agent position
- Blue – Visited nodes
- Yellow – Frontier nodes
- Black – Obstacles
- White – Empty space

---
## Requirements

### Software Requirements

- Python 3.x
- Tkinter (built-in with Python)

### Dependencies

No external libraries are required.

---
## How to Run

### Step 1

Open the project folder.

### Step 2

Run the following command:

python main.py

### Step 3

The application window will open.

---
## How to Use

### Grid Setup

- Create a grid by specifying rows and columns
- Click cells to add or remove obstacles
- Generate a random maze (optional)

### Search Configuration

- Select the search algorithm
- Choose the heuristic
- Enable dynamic mode (optional)

### Execution

- Start the search
- Observe visualization
- Monitor live metrics
---
