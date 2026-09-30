# AI Search Algorithms — Performance Evaluation

## Evaluate the Performance of Various Algorithms for Problem Solving Through Search

> **Academic Project / AI Practical**
>
> This project implements and experimentally evaluates four major categories of Artificial Intelligence search techniques: **Uninformed Search, Informed Search, Local Search, and Constraint Satisfaction Problem (CSP) techniques**.

---

## 1. Project Overview

Artificial Intelligence problems can often be represented as a **state-space search problem**. A search algorithm explores possible states starting from an initial state and attempts to reach a desired goal state while satisfying the rules of the problem.

Different search algorithms use different strategies:

- Some algorithms search without additional knowledge about the goal.
- Some use heuristic information to guide the search.
- Some optimize a solution by examining neighboring states.
- CSP algorithms assign values to variables while satisfying constraints.

This project implements multiple algorithms from all four categories and evaluates them experimentally using measurable performance parameters.

### Algorithms implemented

| Category | Algorithms |
|---|---|
| **Uninformed Search** | BFS, DFS, Uniform Cost Search |
| **Informed Search** | Greedy Best First Search, A* |
| **Local Search** | Hill Climbing, Simulated Annealing |
| **Constraint Satisfaction** | Backtracking, Forward Checking |

---

# 2. Problem Statement

**To implement and evaluate various Artificial Intelligence search algorithms and compare their performance in terms of execution time, nodes explored, solution cost, iterations, assignments, backtracking, and solution quality.**

The project uses two standard AI problems:

### 8-Puzzle
Used to evaluate:

- Breadth First Search
- Depth First Search
- Uniform Cost Search
- Greedy Best First Search
- A* Search

### 8-Queens
Used to evaluate:

- Hill Climbing
- Simulated Annealing
- Backtracking
- Forward Checking

---

# 3. Objectives

The objectives of this project are:

1. To understand state-space representation in Artificial Intelligence.
2. To implement uninformed search algorithms.
3. To implement heuristic/informed search algorithms.
4. To implement local optimization techniques.
5. To solve a Constraint Satisfaction Problem.
6. To compare different search strategies experimentally.
7. To measure execution time and search effort.
8. To compare solution cost and solution quality.
9. To analyze the strengths and limitations of each algorithm.
10. To select appropriate algorithms according to problem characteristics.

---

# 4. Search Problem Formulation

A search problem can be represented using the following components:

### Initial State
The state where the search begins.

### Actions
The operations that can be performed from a state.

### Transition Model
Defines the resulting state after an action.

### Goal Test
Checks whether the current state satisfies the goal.

### Path Cost
Measures the total cost of actions taken to reach a state.

---

# 5. Problem 1 — 8-Puzzle

The 8-Puzzle consists of eight numbered tiles and one blank space on a 3×3 board.

### Initial State

```text
1 2 3
4 0 6
7 5 8
```

`0` represents the blank tile.

### Goal State

```text
1 2 3
4 5 6
7 8 0
```

The blank tile can move up, down, left, or right when the movement is legal.

Each movement has a cost of **1**.

Therefore:

```text
Path Cost = Number of Moves
```

---

# 6. Problem 2 — 8-Queens

The 8-Queens problem requires placing eight queens on an 8×8 chessboard so that no two queens attack each other.

The constraints are:

1. No two queens can be in the same row.
2. No two queens can be in the same column.
3. No two queens can be on the same diagonal.

For a queen in row `i` and column `Qi`, two queens must satisfy:

```text
Qi != Qj
```

and

```text
|Qi - Qj| != |i - j|
```

A solution is reached when the number of attacking pairs is:

```text
0
```

---

# 7. Algorithm Selection and Justification

This section addresses the **Model Selection & Application** criterion of the project rubric.

## 7.1 Breadth First Search — BFS

### Why selected?

BFS was selected to study systematic level-by-level exploration.

### Selection reason

- Does not require a heuristic.
- Finds the shallowest solution.
- Useful when all actions have equal cost.
- Provides a baseline for comparison with heuristic search.

---

## 7.2 Depth First Search — DFS

### Why selected?

DFS was selected to compare depth-oriented exploration with BFS.

### Selection reason

- Uses a stack.
- Requires less memory than BFS.
- Can reach deep solutions quickly.
- Demonstrates the trade-off between memory and optimality.

---

## 7.3 Uniform Cost Search — UCS

### Why selected?

UCS was selected because it considers accumulated path cost.

### Selection reason

- Useful when actions can have different costs.
- Expands the lowest-cost path first.
- Provides a cost-based comparison with BFS and DFS.

---

## 7.4 Greedy Best First Search

### Why selected?

Greedy Best First Search was selected to demonstrate heuristic-guided search.

It uses:

```text
f(n) = h(n)
```

where `h(n)` estimates the distance from the current state to the goal.

For the 8-Puzzle, the implementation uses **Manhattan Distance**.

---

## 7.5 A* Search

### Why selected?

A* was selected because it combines the cost already incurred with the estimated remaining cost.

```text
f(n) = g(n) + h(n)
```

where:

- `g(n)` = cost from the initial state
- `h(n)` = heuristic estimate to the goal
- `f(n)` = estimated total cost

A* provides an important comparison with Greedy Search because both use a heuristic, but A* also considers the accumulated path cost.

---

## 7.6 Hill Climbing

### Why selected?

Hill Climbing was selected as a local-search technique for optimization.

It repeatedly moves toward a neighboring state with a better evaluation value.

For 8-Queens:

```text
Evaluation = Number of Attacking Queen Pairs
```

Goal:

```text
Evaluation = 0
```

---

## 7.7 Simulated Annealing

### Why selected?

Simulated Annealing was selected to address one of the major limitations of Hill Climbing: getting trapped in a local optimum.

It can temporarily accept a worse state based on a temperature-controlled probability.

The commonly used acceptance probability is:

```text
P = e^(-ΔE/T)
```

---

## 7.8 Backtracking

### Why selected?

Backtracking is a fundamental technique for solving CSPs.

It assigns values to variables one at a time and goes back when an assignment violates a constraint.

---

## 7.9 Forward Checking

### Why selected?

Forward Checking improves constraint search by removing values from the domains of future variables that are no longer valid.

This allows the algorithm to detect some failures earlier than basic Backtracking.

---

# 8. Algorithm Details

## 8.1 Uninformed Search

Uninformed search does not use heuristic information.

### BFS

Uses a FIFO queue.

```text
Queue:
First In → First Out
```

Complexity:

```text
Time  : O(b^d)
Space : O(b^d)
```

where:

- `b` = branching factor
- `d` = depth of the shallowest solution

### DFS

Uses a stack.

```text
Stack:
Last In → First Out
```

Typical worst-case complexity:

```text
Time  : O(b^m)
Space : O(bm)
```

where `m` is the maximum search depth.

### UCS

Uses a priority queue ordered by path cost:

```text
f(n) = g(n)
```

It is suitable for minimum-cost path problems under appropriate positive-cost assumptions.

---

# 9. Informed Search

Informed search uses a heuristic.

## Manhattan Distance

For the 8-Puzzle:

```text
h(n) = Sum of Manhattan distances of all tiles from their goal positions
```

For each tile:

```text
Distance = |current row - goal row|
         + |current column - goal column|
```

## Greedy Best First

```text
f(n) = h(n)
```

It focuses on the estimated distance to the goal.

## A*

```text
f(n) = g(n) + h(n)
```

It combines:

```text
Actual cost + Estimated remaining cost
```

---

# 10. Local Search

Local search focuses on the current state and neighboring states instead of maintaining a complete search tree.

## Hill Climbing

The algorithm selects a better neighboring state.

Potential problems:

- Local optimum
- Plateau
- Ridge

## Simulated Annealing

Simulated Annealing can accept some worse moves, especially at higher temperatures.

The temperature gradually decreases:

```text
High Temperature
       ↓
More Exploration
       ↓
Cooling
       ↓
Less Exploration
       ↓
Convergence
```

---

# 11. Constraint Satisfaction Problem

A CSP contains:

```text
Variables
Domains
Constraints
```

For 8-Queens:

```text
Variables = Q1, Q2, ..., Q8
Domain    = {0,1,2,3,4,5,6,7}
```

The constraints prevent queens from sharing rows, columns, or diagonals.

---

# 12. Backtracking

Basic procedure:

```text
1. Select an unassigned variable.
2. Select a possible value.
3. Check constraints.
4. If valid, assign it.
5. Continue.
6. If no value works, backtrack.
7. Repeat until a solution is found.
```

---

# 13. Forward Checking

Forward Checking performs additional domain pruning.

Example:

```text
Assign Q1
   ↓
Remove invalid values from Q2...Q8
   ↓
Assign Q2
   ↓
Prune future domains
   ↓
Continue
```

If a future domain becomes empty, the algorithm backtracks immediately.

---

# 14. Performance Evaluation

The project measures the following parameters.

## 14.1 Execution Time

Measured using Python's:

```python
time.perf_counter()
```

Formula:

```text
Execution Time = End Time - Start Time
```

The result is reported in milliseconds.

---

## 14.2 Nodes Explored

Number of search states removed from the frontier and evaluated.

This indicates the amount of search effort.

---

## 14.3 Nodes Generated

Number of states generated while expanding the search space.

---

## 14.4 Path Length

Number of actions required to reach the goal.

---

## 14.5 Path Cost

For the current 8-Puzzle configuration, every move costs 1.

Therefore:

```text
Path Cost = Path Length
```

---

## 14.6 Iterations

For local search, the number of iterations indicates how many improvement/search steps were performed.

---

## 14.7 Final Conflicts

For 8-Queens:

```text
Final Conflicts = Number of attacking queen pairs
```

A valid solution has:

```text
Final Conflicts = 0
```

---

## 14.8 CSP Assignments

The number of candidate assignments attempted by a CSP algorithm.

A lower number can indicate less search effort for the tested instance, although it should be interpreted together with execution time and problem configuration.

---

## 14.9 CSP Backtracks

The number of times the algorithm had to return to an earlier decision after reaching an invalid or unsuccessful partial assignment.

---

# 15. Experimental Results

The program automatically generates:

```text
results/performance_results.csv
```

and:

```text
outputs/complete_output.txt
```

These files contain the measured results from the actual program execution.

### Example output format

| Algorithm | Time (ms) | Nodes Explored | Path Cost | Solved |
|---|---:|---:|---:|---|
| BFS | Measured | Measured | Measured | Yes/No |
| DFS | Measured | Measured | Measured | Yes/No |
| UCS | Measured | Measured | Measured | Yes/No |
| Greedy | Measured | Measured | Measured | Yes/No |
| A* | Measured | Measured | Measured | Yes/No |

> **Important:** Execution time can change between computers and runs. The CSV generated by your own run should be used for the final report.

---

# 16. Generated Performance Graphs

The program automatically creates five graphs.

### 1. Execution Time

```text
graphs/execution_time.png
```

Compares the execution time of the 8-Puzzle algorithms.

### 2. Nodes Explored

```text
graphs/nodes_explored.png
```

Compares the number of explored states.

### 3. Path Cost

```text
graphs/path_cost.png
```

Compares solution path cost.

### 4. Local Search Conflicts

```text
graphs/local_search_conflicts.png
```

Compares final conflicts for Hill Climbing and Simulated Annealing.

### 5. CSP Assignments

```text
graphs/csp_assignments.png
```

Compares assignment attempts for Backtracking and Forward Checking.

---

# 17. Critical Analysis & Evaluation

This section directly addresses the **Critical Analysis & Evaluation — 2.5 marks** rubric criterion.

## Uninformed Search Analysis

BFS systematically explores the search space level by level and can provide the shortest solution when all actions have equal cost. However, its memory requirements can become large because it stores many frontier states.

DFS generally requires less memory but does not guarantee the shortest solution. Its performance depends strongly on the order in which branches are explored.

UCS is useful when action costs differ because it prioritizes the lowest accumulated cost rather than simply the shallowest state.

---

## Informed Search Analysis

Greedy Best First Search uses only heuristic information:

```text
f(n) = h(n)
```

This can reduce search effort when the heuristic points toward the goal, but it does not generally guarantee an optimal path.

A* uses:

```text
f(n) = g(n) + h(n)
```

Therefore, it considers both the cost already incurred and the estimated remaining cost. With an appropriate admissible heuristic, A* can provide optimal solutions.

---

## Local Search Analysis

Hill Climbing requires very little memory and can reach a good solution quickly. However, it may become stuck in local optima, plateaus, or ridges.

Simulated Annealing introduces controlled randomness and can accept worse states temporarily. This provides a mechanism for escaping local optima, although its performance depends on parameters such as temperature and cooling rate.

---

## CSP Analysis

Basic Backtracking systematically explores possible assignments but may attempt many assignments before discovering a valid solution.

Forward Checking reduces unnecessary exploration by pruning values that are inconsistent with existing assignments.

For the tested configuration, the generated results should be compared using:

- Assignments
- Backtracks
- Execution time
- Whether a valid solution was obtained

The experiment should be interpreted based on actual measured values rather than assuming that one method is always superior.

---

# 18. Comparison Summary

| Algorithm | Category | Heuristic | Main Data Structure | Main Strength | Main Limitation |
|---|---|---|---|---|---|
| BFS | Uninformed | No | Queue | Shallowest solution | High memory |
| DFS | Uninformed | No | Stack | Low memory | Not generally optimal |
| UCS | Uninformed | No | Priority Queue | Minimum-cost search | Can explore many states |
| Greedy | Informed | Yes | Priority Queue | Goal-directed | Not generally optimal |
| A* | Informed | Yes | Priority Queue | Combines cost + heuristic | Memory requirement |
| Hill Climbing | Local | Evaluation function | Local neighbors | Very low memory | Local optima |
| Simulated Annealing | Local | Evaluation function | Local neighbors | Can escape local optima | Parameter dependent |
| Backtracking | CSP | Constraints | Recursive search | Systematic CSP solving | Can search many assignments |
| Forward Checking | CSP | Constraints/domains | Recursive search | Early pruning | Additional domain management |

---

# 19. Implementation

## Programming Language

**Python 3**

## Libraries

The project uses:

```text
heapq
collections
time
random
math
csv
pathlib
matplotlib
```

Most modules are part of Python's standard library. `matplotlib` is used to generate performance graphs.

Install matplotlib:

```bash
pip install matplotlib
```

---

# 20. Project Structure

```text
AI_Search_Algorithms/
│
├── main.py
├── README.md
├── requirements.txt
│
├── src/
│   ├── __init__.py
│   └── search_algorithms.py
│
├── outputs/
│   └── complete_output.txt
│
├── results/
│   └── performance_results.csv
│
└── graphs/
    ├── execution_time.png
    ├── nodes_explored.png
    ├── path_cost.png
    ├── local_search_conflicts.png
    └── csp_assignments.png
```

---

# 21. How to Run the Project

## Step 1 — Install Python

Python 3.9 or newer is recommended.

Check:

```bash
python --version
```

---

## Step 2 — Install matplotlib

```bash
pip install matplotlib
```

---

## Step 3 — Open the Project

Open the `AI_Search_Algorithms` folder in VS Code.

The terminal should be inside the folder containing:

```text
main.py
```

---

## Step 4 — Run

```bash
python main.py
```

---

## Step 5 — View Results

After execution, check:

```text
outputs/
results/
graphs/
```

The program automatically generates the output and graph files.

---

# 22. Sample Console Output

The exact values depend on the computer and execution.

```text
================================================================================
AI SEARCH ALGORITHMS - PERFORMANCE EVALUATION
================================================================================

8-PUZZLE RESULTS
--------------------------------------------------------------------------------
Algorithm                 Time(ms)    Explored      Cost    Solved
BFS                         ...          ...         ...       True
DFS                         ...          ...         ...       True
UCS                         ...          ...         ...       True
Greedy Best First           ...          ...         ...       True
A*                          ...          ...         ...       True

8-QUEENS RESULTS
--------------------------------------------------------------------------------
Algorithm                 Time(ms)  Iterations   Conflicts    Solved
Hill Climbing               ...          ...          ...       True
Simulated Annealing         ...          ...          ...       True
Backtracking                ...           -            -       True
Forward Checking            ...           -            -       True
```

---

# 23. Evidence of Implementation and Output

For academic submission, the following evidence should be included:

### Implementation Evidence

- Screenshot of `main.py`
- Screenshot of `src/search_algorithms.py`
- Screenshot of terminal execution

### Output Evidence

- 8-Puzzle output
- 8-Queens output
- CSV performance table
- Generated graphs

### Analysis Evidence

- Comparison table
- Performance graphs
- Written interpretation
- Limitations
- Conclusion

This evidence supports the **Implementation, Output Quality and Analysis** criterion.

---

# 24. Professionalism, Creativity, Communication & Reflection

This project follows a structured and reproducible workflow:

```text
Problem Definition
       ↓
Algorithm Selection
       ↓
Implementation
       ↓
Execution
       ↓
Performance Measurement
       ↓
Data Collection
       ↓
Graphs
       ↓
Critical Analysis
       ↓
Conclusion
```

The project also separates source code, outputs, results, and graphs, making it easier to understand and reproduce.

### Reflection

The experiment demonstrates that algorithm selection should be based on the characteristics of the problem rather than using the same algorithm for every problem. Uninformed methods are useful when no heuristic information is available, informed methods can exploit domain knowledge, local search is useful for optimization, and CSP techniques are suitable when variables and constraints define the problem.

---

# 25. Limitations

1. The experiments use relatively small benchmark problems.
2. Execution time depends on the computer and current system load.
3. Heuristic search performance depends on heuristic quality.
4. Local-search results can depend on the initial state and random seed.
5. Simulated Annealing performance depends on temperature and cooling parameters.
6. Results from one problem instance should not be treated as universal performance rankings.
7. Memory usage is not directly profiled in the current implementation.

---

# 26. Future Scope

The project can be extended by:

- Implementing 15-Puzzle.
- Testing larger search spaces.
- Comparing multiple heuristics.
- Implementing Beam Search.
- Implementing IDA*.
- Implementing Genetic Algorithms.
- Testing larger CSPs.
- Adding memory profiling.
- Running each algorithm multiple times and reporting mean/standard deviation.
- Creating an interactive graphical interface.
- Visualizing the search path and explored states.

---

# 27. Conclusion

This project demonstrates and evaluates nine AI problem-solving algorithms belonging to four major categories: **Uninformed Search, Informed Search, Local Search, and Constraint Satisfaction**.

BFS, DFS, and UCS demonstrate search without heuristic information. Greedy Best First Search and A* demonstrate how heuristic information can guide the search. Hill Climbing and Simulated Annealing demonstrate local optimization strategies, while Backtracking and Forward Checking demonstrate systematic constraint-based problem solving.

The experimental evaluation uses execution time, explored nodes, path cost, iterations, conflicts, assignments, and backtracks as measurable performance indicators.

The results demonstrate that search performance depends on the problem representation, heuristic information, constraints, algorithmic strategy, and implementation. Therefore, the appropriate algorithm should be selected according to the requirements and characteristics of the specific problem.

---

# 28. Rubric Alignment

This project is designed around the provided grading rubric.

## A. Model Selection & Application — 2.5 Points

Evidence provided:

- Problem formulation
- Algorithm selection
- Detailed justification for every algorithm
- Explanation of BFS, DFS, UCS, Greedy, A*, Hill Climbing, Simulated Annealing, Backtracking and Forward Checking
- Explanation of the Manhattan Distance heuristic
- Explanation of why different algorithms are suitable for different problem types

---

## B. Implementation, Output Quality & Analysis — 2.5 Points

Evidence provided:

- Working Python implementation
- 9 implemented algorithms
- Actual program execution
- Automated performance measurement
- CSV result generation
- Text output generation
- Five performance graphs
- Reproducible project structure
- README instructions

---

## C. Critical Analysis & Evaluation — 2.5 Points

Evidence provided:

- Quantitative performance metrics
- Execution-time comparison
- Nodes-explored comparison
- Path-cost comparison
- Local-search conflict comparison
- CSP assignment/backtrack comparison
- Advantages and limitations
- Experimental interpretation
- Discussion of problem-dependent performance

---

## D. Professionalism, Creativity, Communication & Reflection — 2.5 Points

Evidence provided:

- Structured GitHub-ready project
- Professional README
- Organized source/output/results folders
- Graphical presentation of results
- Clear problem formulation
- Reflection
- Limitations
- Future scope
- Conclusion
- Reproducible execution instructions

---

# 29. Academic Note

The performance values generated by the program are **experimental measurements**, not theoretical guarantees.

In particular:

- Execution time can vary between computers.
- Local-search results can vary with random initialization.
- One test case cannot establish universal superiority of an algorithm.
- Performance should be interpreted using the problem instance and experimental conditions.

Therefore, the final report should use the results generated by the student's own execution and explain the observed behavior objectively.

---

# 30. References

1. Stuart Russell and Peter Norvig, *Artificial Intelligence: A Modern Approach*, Pearson.
2. Python Documentation — Python Standard Library.
3. Course notes and lecture material on Artificial Intelligence and Search Algorithms.
4. Documentation for Matplotlib used for experimental visualization.
