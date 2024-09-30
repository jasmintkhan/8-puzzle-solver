# 8-Puzzle Solver

This repository contains Python implementations of various search algorithms to solve the classic 8-puzzle problem. The project includes solutions for two different goal states using Depth-First Search (DFS), Breadth-First Search (BFS), Uniform Cost Search (UCS), and A* search with both Manhattan and Euclidean distance heuristics.

## Table of Contents
- [Introduction](#introduction)
- [Search Algorithms](#search-algorithms)
- [Goal States](#goal-states)
- [File Structure](#file-structure)
- [How to Run](#how-to-run)
- [Results](#results)

## Introduction
The 8-puzzle is a sliding puzzle consisting of a 3x3 grid with numbered tiles from 1 to 8 and a blank space. The objective is to rearrange the tiles to meet a specific goal state. This repository explores different search techniques to find the solution efficiently.

## Search Algorithms
The following search algorithms are implemented in this project:
1. **Depth-First Search (DFS)**
2. **Breadth-First Search (BFS)**
3. **Uniform Cost Search (UCS)**
4. **A\* Search (with Manhattan Distance)**
5. **A\* Search (with Euclidean Distance)**

Each algorithm searches for the shortest path to the solution and returns the number of node expansions along with the solution path.

## Goal States

### Goal State 1 (Standard Goal State)
The traditional goal state for the 8-puzzle problem is to rearrange the tiles in the following order:
```
_12
345
678
```

### Goal State 2 (Sum Goal State)
In this variation, the goal is to rearrange the tiles such that the numbers in the top row sum up to 11. There can be multiple configurations that satisfy this condition.

## File Structure
The repository is structured as follows:

8-puzzle-solver/
- **`standard_goal.py`**: Handles the search algorithms for the traditional goal state (`_,1,2,3,4,5,6,7,8,9`).
- **`sum_goal.py`**: Modifies the search algorithms to work for the second goal state, where the top row sums to 11 (adjustable).
- **`input.txt`**: Contains the initial state of the puzzle, formatted as a comma-separated string (e.g., `1,2,3,4,5,6,7,_,8`).



## How to Run

### Prerequisites
- Python 3.x installed on your machine.

### Instructions
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/jasmintkhan/8-puzzle-solver.git
   cd 8-puzzle-solver

Modify the input.txt file to specify the initial state of the puzzle. Format the input as a comma-separated string:

```
1,2,3,4,5,6,7,_,8
```

Run the code to solve for the traditional goal state:
```
python standard_goal.py
```

Run the code to solve for the sum-goal state:
```
python sum_goal.py
```

### Results
The solutions for each algorithm will be printed in the console, showing the sequence of moves and the number of node expansions. Example moves:
```
L (Left)
R (Right)
U (Up)
D (Down)
```

## An Example of Output (Standard Goal, BFS)
<img width="544" alt="Screenshot 2024-09-30 at 11 39 02 AM" src="https://github.com/user-attachments/assets/0a87d526-a1ce-4112-b291-8a252c6731b8">


Initial State:
```
1,4,2,3,_,5,6,7,8
```

Goal State:
```
_,1,2,3,4,5,6,7,8
```

BFS will return: 
```
4D,1R
```
Meaning, the shortest path to the Goal State is by moving tile 4 Down, and then tile 1 right.
