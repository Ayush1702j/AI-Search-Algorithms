
"""
AI Search Algorithms - Performance Evaluation
Algorithms:
1. BFS
2. DFS
3. Uniform Cost Search
4. Greedy Best First Search
5. A*
6. Hill Climbing
7. Simulated Annealing
8. CSP Backtracking
9. CSP Forward Checking

Problems:
- 8-Puzzle: BFS, DFS, UCS, Greedy, A*
- 8-Queens: Hill Climbing, Simulated Annealing, Backtracking, Forward Checking

Run:
    python main.py
"""

from __future__ import annotations

import csv
import heapq
import math
import random
import time
from collections import deque
from pathlib import Path

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "outputs"
GRAPH_DIR = ROOT / "graphs"
RESULT_DIR = ROOT / "results"

for folder in (OUTPUT_DIR, GRAPH_DIR, RESULT_DIR):
    folder.mkdir(exist_ok=True)


# ============================================================
# 8-PUZZLE UTILITIES
# ============================================================

START = (1, 2, 3,
         4, 0, 6,
         7, 5, 8)

GOAL = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)


def puzzle_neighbors(state):
    """Return (next_state, move_name, step_cost) for each legal move."""
    zero = state.index(0)
    row, col = divmod(zero, 3)

    moves = []
    directions = [
        (-1, 0, "UP"),
        (1, 0, "DOWN"),
        (0, -1, "LEFT"),
        (0, 1, "RIGHT"),
    ]

    for dr, dc, name in directions:
        nr, nc = row + dr, col + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_state = list(state)
            other = nr * 3 + nc
            new_state[zero], new_state[other] = new_state[other], new_state[zero]
            moves.append((tuple(new_state), name, 1))

    return moves


def manhattan_distance(state, goal=GOAL):
    """Manhattan-distance heuristic for the 8-puzzle."""
    goal_positions = {value: divmod(i, 3) for i, value in enumerate(goal)}
    distance = 0

    for i, value in enumerate(state):
        if value == 0:
            continue
        r1, c1 = divmod(i, 3)
        r2, c2 = goal_positions[value]
        distance += abs(r1 - r2) + abs(c1 - c2)

    return distance


def reconstruct_path(parent, action, goal_state):
    """Reconstruct state path and action path."""
    states = []
    actions = []
    current = goal_state

    while current is not None:
        states.append(current)
        if parent[current] is not None:
            actions.append(action[current])
        current = parent[current]

    states.reverse()
    actions.reverse()
    return states, actions


def format_puzzle(state):
    return (
        f"{state[0]} {state[1]} {state[2]}\n"
        f"{state[3]} {state[4]} {state[5]}\n"
        f"{state[6]} {state[7]} {state[8]}"
    )


def puzzle_result(name, goal_state, parent, action, explored,
                  generated, start_time, extra=None):
    elapsed = (time.perf_counter() - start_time) * 1000
    if goal_state is None:
        return {
            "algorithm": name,
            "problem": "8-Puzzle",
            "success": False,
            "time_ms": elapsed,
            "nodes_explored": explored,
            "nodes_generated": generated,
            "path_length": None,
            "path_cost": None,
            "extra": extra or "",
        }

    states, actions = reconstruct_path(parent, action, goal_state)
    return {
        "algorithm": name,
        "problem": "8-Puzzle",
        "success": True,
        "time_ms": elapsed,
        "nodes_explored": explored,
        "nodes_generated": generated,
        "path_length": len(actions),
        "path_cost": len(actions),
        "extra": extra or "",
        "path": actions,
        "states": states,
    }


# ============================================================
# 1. BREADTH FIRST SEARCH
# ============================================================

def bfs(start=START, goal=GOAL):
    start_time = time.perf_counter()

    queue = deque([start])
    visited = {start}
    parent = {start: None}
    action = {start: None}

    explored = 0
    generated = 1

    while queue:
        current = queue.popleft()
        explored += 1

        if current == goal:
            return puzzle_result(
                "BFS", current, parent, action, explored, generated, start_time
            )

        for nxt, move, _ in puzzle_neighbors(current):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = current
                action[nxt] = move
                queue.append(nxt)
                generated += 1

    return puzzle_result(
        "BFS", None, parent, action, explored, generated, start_time
    )


# ============================================================
# 2. DEPTH FIRST SEARCH
# ============================================================

def dfs(start=START, goal=GOAL, max_depth=50):
    start_time = time.perf_counter()

    stack = [(start, 0)]
    visited_depth = {start: 0}
    parent = {start: None}
    action = {start: None}

    explored = 0
    generated = 1

    while stack:
        current, depth = stack.pop()
        explored += 1

        if current == goal:
            return puzzle_result(
                "DFS", current, parent, action, explored, generated, start_time,
                f"Depth limit={max_depth}"
            )

        if depth >= max_depth:
            continue

        neighbors = puzzle_neighbors(current)

        # Reverse so the first listed move is explored first.
        for nxt, move, _ in reversed(neighbors):
            new_depth = depth + 1
            if nxt not in visited_depth or new_depth < visited_depth[nxt]:
                visited_depth[nxt] = new_depth
                parent[nxt] = current
                action[nxt] = move
                stack.append((nxt, new_depth))
                generated += 1

    return puzzle_result(
        "DFS", None, parent, action, explored, generated, start_time,
        f"Depth limit={max_depth}"
    )


# ============================================================
# 3. UNIFORM COST SEARCH
# ============================================================

def uniform_cost_search(start=START, goal=GOAL):
    start_time = time.perf_counter()

    counter = 0
    frontier = [(0, counter, start)]
    best_cost = {start: 0}

    parent = {start: None}
    action = {start: None}

    explored = 0
    generated = 1

    while frontier:
        cost, _, current = heapq.heappop(frontier)

        if cost != best_cost.get(current):
            continue

        explored += 1

        if current == goal:
            return puzzle_result(
                "UCS", current, parent, action, explored, generated, start_time
            )

        for nxt, move, step_cost in puzzle_neighbors(current):
            new_cost = cost + step_cost

            if new_cost < best_cost.get(nxt, float("inf")):
                best_cost[nxt] = new_cost
                parent[nxt] = current
                action[nxt] = move
                counter += 1
                heapq.heappush(frontier, (new_cost, counter, nxt))
                generated += 1

    return puzzle_result(
        "UCS", None, parent, action, explored, generated, start_time
    )


# ============================================================
# 4. GREEDY BEST FIRST SEARCH
# ============================================================

def greedy_best_first(start=START, goal=GOAL):
    start_time = time.perf_counter()

    counter = 0
    frontier = [(manhattan_distance(start, goal), counter, start)]
    visited = {start}

    parent = {start: None}
    action = {start: None}

    explored = 0
    generated = 1

    while frontier:
        _, _, current = heapq.heappop(frontier)
        explored += 1

        if current == goal:
            return puzzle_result(
                "Greedy Best First", current, parent, action,
                explored, generated, start_time,
                "Heuristic: Manhattan Distance"
            )

        for nxt, move, _ in puzzle_neighbors(current):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = current
                action[nxt] = move
                counter += 1
                heapq.heappush(
                    frontier,
                    (manhattan_distance(nxt, goal), counter, nxt)
                )
                generated += 1

    return puzzle_result(
        "Greedy Best First", None, parent, action,
        explored, generated, start_time,
        "Heuristic: Manhattan Distance"
    )


# ============================================================
# 5. A* SEARCH
# ============================================================

def a_star(start=START, goal=GOAL):
    start_time = time.perf_counter()

    counter = 0
    g_cost = {start: 0}
    frontier = [(manhattan_distance(start, goal), counter, start)]

    parent = {start: None}
    action = {start: None}

    explored = 0
    generated = 1

    while frontier:
        f_score, _, current = heapq.heappop(frontier)

        expected_f = g_cost[current] + manhattan_distance(current, goal)
        if f_score != expected_f:
            continue

        explored += 1

        if current == goal:
            return puzzle_result(
                "A*", current, parent, action, explored, generated, start_time,
                "f(n) = g(n) + h(n); h = Manhattan Distance"
            )

        for nxt, move, step_cost in puzzle_neighbors(current):
            tentative_g = g_cost[current] + step_cost

            if tentative_g < g_cost.get(nxt, float("inf")):
                g_cost[nxt] = tentative_g
                parent[nxt] = current
                action[nxt] = move
                counter += 1
                f = tentative_g + manhattan_distance(nxt, goal)
                heapq.heappush(frontier, (f, counter, nxt))
                generated += 1

    return puzzle_result(
        "A*", None, parent, action, explored, generated, start_time,
        "f(n) = g(n) + h(n); h = Manhattan Distance"
    )


# ============================================================
# 8-QUEENS UTILITIES
# ============================================================

N = 8


def conflicts(board):
    """
    board[row] = column of queen in that row.
    Counts attacking queen pairs.
    """
    count = 0
    for i in range(N):
        for j in range(i + 1, N):
            same_column = board[i] == board[j]
            same_diagonal = abs(board[i] - board[j]) == abs(i - j)
            if same_column or same_diagonal:
                count += 1
    return count


def print_board(board):
    lines = []
    for r in range(N):
        row = []
        for c in range(N):
            row.append("Q" if board[r] == c else ".")
        lines.append(" ".join(row))
    return "\n".join(lines)


# ============================================================
# 6. HILL CLIMBING
# ============================================================

def hill_climbing(max_restarts=100, seed=42):
    start_time = time.perf_counter()
    rng = random.Random(seed)

    total_iterations = 0
    restarts = 0

    best_board = None
    best_score = float("inf")

    for restart in range(max_restarts):
        restarts += 1
        board = [rng.randrange(N) for _ in range(N)]
        current_score = conflicts(board)

        while True:
            total_iterations += 1

            neighbors = []
            for row in range(N):
                original = board[row]
                for col in range(N):
                    if col == original:
                        continue
                    candidate = board.copy()
                    candidate[row] = col
                    score = conflicts(candidate)
                    neighbors.append((score, candidate))

            min_score = min(score for score, _ in neighbors)

            if min_score >= current_score:
                break

            # Randomly select among equally good best neighbors.
            best_neighbors = [
                candidate for score, candidate in neighbors
                if score == min_score
            ]
            board = rng.choice(best_neighbors)
            current_score = min_score

            if current_score == 0:
                elapsed = (time.perf_counter() - start_time) * 1000
                return {
                    "algorithm": "Hill Climbing",
                    "problem": "8-Queens",
                    "success": True,
                    "time_ms": elapsed,
                    "iterations": total_iterations,
                    "final_conflicts": 0,
                    "restarts": restarts,
                    "board": board,
                }

        if current_score < best_score:
            best_score = current_score
            best_board = board.copy()

    elapsed = (time.perf_counter() - start_time) * 1000
    return {
        "algorithm": "Hill Climbing",
        "problem": "8-Queens",
        "success": best_score == 0,
        "time_ms": elapsed,
        "iterations": total_iterations,
        "final_conflicts": best_score,
        "restarts": restarts,
        "board": best_board,
    }


# ============================================================
# 7. SIMULATED ANNEALING
# ============================================================

def simulated_annealing(
    max_iterations=10000,
    initial_temperature=10.0,
    cooling_rate=0.995,
    seed=42
):
    start_time = time.perf_counter()
    rng = random.Random(seed)

    board = [rng.randrange(N) for _ in range(N)]
    current_score = conflicts(board)

    best_board = board.copy()
    best_score = current_score

    temperature = initial_temperature

    for iteration in range(1, max_iterations + 1):
        if current_score == 0:
            elapsed = (time.perf_counter() - start_time) * 1000
            return {
                "algorithm": "Simulated Annealing",
                "problem": "8-Queens",
                "success": True,
                "time_ms": elapsed,
                "iterations": iteration,
                "final_conflicts": 0,
                "initial_temperature": initial_temperature,
                "cooling_rate": cooling_rate,
                "board": board,
            }

        row = rng.randrange(N)
        new_board = board.copy()

        new_col = rng.randrange(N - 1)
        if new_col >= new_board[row]:
            new_col += 1
        new_board[row] = new_col

        new_score = conflicts(new_board)
        delta = new_score - current_score

        if delta <= 0:
            accept = True
        else:
            temperature = max(temperature, 1e-12)
            probability = math.exp(-delta / temperature)
            accept = rng.random() < probability

        if accept:
            board = new_board
            current_score = new_score

        if current_score < best_score:
            best_score = current_score
            best_board = board.copy()

        temperature *= cooling_rate

    elapsed = (time.perf_counter() - start_time) * 1000
    return {
        "algorithm": "Simulated Annealing",
        "problem": "8-Queens",
        "success": best_score == 0,
        "time_ms": elapsed,
        "iterations": max_iterations,
        "final_conflicts": best_score,
        "initial_temperature": initial_temperature,
        "cooling_rate": cooling_rate,
        "board": best_board,
    }


# ============================================================
# 8. BACKTRACKING CSP
# ============================================================

def is_safe(board, row, col):
    """Check whether placing a queen at (row, col) is valid."""
    for previous_row in range(row):
        previous_col = board[previous_row]

        if previous_col == col:
            return False

        if abs(previous_col - col) == abs(previous_row - row):
            return False

    return True


def solve_backtracking():
    start_time = time.perf_counter()

    board = [-1] * N
    assignments = 0
    backtracks = 0

    def backtrack(row):
        nonlocal assignments, backtracks

        if row == N:
            return True

        for col in range(N):
            assignments += 1

            if is_safe(board, row, col):
                board[row] = col

                if backtrack(row + 1):
                    return True

                board[row] = -1

        backtracks += 1
        return False

    success = backtrack(0)
    elapsed = (time.perf_counter() - start_time) * 1000

    return {
        "algorithm": "Backtracking",
        "problem": "8-Queens",
        "success": success,
        "time_ms": elapsed,
        "assignments": assignments,
        "backtracks": backtracks,
        "board": board.copy(),
    }


# ============================================================
# 9. FORWARD CHECKING CSP
# ============================================================

def solve_forward_checking():
    start_time = time.perf_counter()

    board = [-1] * N
    domains = [set(range(N)) for _ in range(N)]

    assignments = 0
    backtracks = 0

    def consistent(row, col):
        for previous_row in range(row):
            previous_col = board[previous_row]
            if previous_col == -1:
                continue

            if previous_col == col:
                return False

            if abs(previous_col - col) == abs(previous_row - row):
                return False

        return True

    def forward_check(row, col):
        """
        Assign row=col and remove invalid values from future domains.
        Return changes so they can be restored during backtracking.
        """
        changes = []

        for future_row in range(row + 1, N):
            invalid = set()

            for future_col in domains[future_row]:
                if future_col == col:
                    invalid.add(future_col)
                elif abs(future_col - col) == abs(future_row - row):
                    invalid.add(future_col)

            if invalid:
                domains[future_row] -= invalid
                changes.append((future_row, invalid))

            if not domains[future_row]:
                return False, changes

        return True, changes

    def restore(changes):
        for row, removed_values in reversed(changes):
            domains[row].update(removed_values)

    def backtrack(row):
        nonlocal assignments, backtracks

        if row == N:
            return True

        # Minimum Remaining Values is unnecessary here because
        # each row is assigned in sequence, but domains are pruned.
        for col in sorted(domains[row]):
            assignments += 1

            if not consistent(row, col):
                continue

            board[row] = col
            old_domain = domains[row].copy()
            domains[row] = {col}

            valid, changes = forward_check(row, col)

            if valid and backtrack(row + 1):
                return True

            restore(changes)
            domains[row] = old_domain
            board[row] = -1

        backtracks += 1
        return False

    success = backtrack(0)
    elapsed = (time.perf_counter() - start_time) * 1000

    return {
        "algorithm": "Forward Checking",
        "problem": "8-Queens",
        "success": success,
        "time_ms": elapsed,
        "assignments": assignments,
        "backtracks": backtracks,
        "board": board.copy(),
    }


# ============================================================
# REPORTING
# ============================================================

def write_text_output(results):
    output_file = OUTPUT_DIR / "complete_output.txt"

    with output_file.open("w", encoding="utf-8") as f:
        f.write("AI SEARCH ALGORITHMS - PERFORMANCE EVALUATION\n")
        f.write("=" * 70 + "\n\n")

        f.write("8-PUZZLE RESULTS\n")
        f.write("-" * 70 + "\n")

        for r in results["puzzle"]:
            f.write(f"\nAlgorithm: {r['algorithm']}\n")
            f.write(f"Success: {r['success']}\n")
            f.write(f"Execution Time: {r['time_ms']:.4f} ms\n")
            f.write(f"Nodes Explored: {r['nodes_explored']}\n")
            f.write(f"Nodes Generated: {r['nodes_generated']}\n")
            f.write(f"Path Length: {r.get('path_length', 'N/A')}\n")
            f.write(f"Path Cost: {r.get('path_cost', 'N/A')}\n")
            f.write(f"Details: {r.get('extra', '')}\n")
            if r["success"]:
                f.write(f"Moves: {' -> '.join(r['path'])}\n")

        f.write("\n\n8-QUEENS RESULTS\n")
        f.write("-" * 70 + "\n")

        for r in results["queens"]:
            f.write(f"\nAlgorithm: {r['algorithm']}\n")
            f.write(f"Success: {r['success']}\n")
            f.write(f"Execution Time: {r['time_ms']:.4f} ms\n")

            if "iterations" in r:
                f.write(f"Iterations: {r['iterations']}\n")
            if "final_conflicts" in r:
                f.write(f"Final Conflicts: {r['final_conflicts']}\n")
            if "assignments" in r:
                f.write(f"Assignments: {r['assignments']}\n")
            if "backtracks" in r:
                f.write(f"Backtracks: {r['backtracks']}\n")

            f.write("\nBoard:\n")
            f.write(print_board(r["board"]) + "\n")

    return output_file


def write_csv(results):
    csv_file = RESULT_DIR / "performance_results.csv"

    rows = []

    for r in results["puzzle"]:
        rows.append({
            "Problem": r["problem"],
            "Algorithm": r["algorithm"],
            "Success": r["success"],
            "Execution_Time_ms": round(r["time_ms"], 6),
            "Nodes_Explored": r["nodes_explored"],
            "Nodes_Generated": r["nodes_generated"],
            "Path_Length": r.get("path_length", ""),
            "Path_Cost": r.get("path_cost", ""),
            "Iterations": "",
            "Final_Conflicts": "",
            "Assignments": "",
            "Backtracks": "",
        })

    for r in results["queens"]:
        rows.append({
            "Problem": r["problem"],
            "Algorithm": r["algorithm"],
            "Success": r["success"],
            "Execution_Time_ms": round(r["time_ms"], 6),
            "Nodes_Explored": "",
            "Nodes_Generated": "",
            "Path_Length": "",
            "Path_Cost": "",
            "Iterations": r.get("iterations", ""),
            "Final_Conflicts": r.get("final_conflicts", ""),
            "Assignments": r.get("assignments", ""),
            "Backtracks": r.get("backtracks", ""),
        })

    with csv_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    return csv_file


def make_graphs(results):
    if plt is None:
        print("\nmatplotlib is not installed. Graphs were not created.")
        return

    puzzle = results["puzzle"]
    names = [r["algorithm"] for r in puzzle]

    # Execution time
    plt.figure(figsize=(10, 5))
    plt.bar(names, [r["time_ms"] for r in puzzle])
    plt.ylabel("Execution Time (ms)")
    plt.xlabel("Algorithm")
    plt.title("8-Puzzle: Execution Time Comparison")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(GRAPH_DIR / "execution_time.png", dpi=200)
    plt.close()

    # Nodes explored
    plt.figure(figsize=(10, 5))
    plt.bar(names, [r["nodes_explored"] for r in puzzle])
    plt.ylabel("Nodes Explored")
    plt.xlabel("Algorithm")
    plt.title("8-Puzzle: Nodes Explored Comparison")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(GRAPH_DIR / "nodes_explored.png", dpi=200)
    plt.close()

    # Path cost
    plt.figure(figsize=(10, 5))
    values = [
        r["path_cost"] if r["path_cost"] is not None else 0
        for r in puzzle
    ]
    plt.bar(names, values)
    plt.ylabel("Path Cost")
    plt.xlabel("Algorithm")
    plt.title("8-Puzzle: Solution Path Cost Comparison")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(GRAPH_DIR / "path_cost.png", dpi=200)
    plt.close()

    queens = results["queens"]
    qnames = [r["algorithm"] for r in queens]

    # Local search comparison
    local = queens[:2]
    plt.figure(figsize=(8, 5))
    plt.bar(
        [r["algorithm"] for r in local],
        [r["final_conflicts"] for r in local]
    )
    plt.ylabel("Final Conflicts")
    plt.xlabel("Algorithm")
    plt.title("8-Queens: Local Search Final Conflicts")
    plt.tight_layout()
    plt.savefig(GRAPH_DIR / "local_search_conflicts.png", dpi=200)
    plt.close()

    # CSP comparison
    csp = queens[2:]
    plt.figure(figsize=(8, 5))
    plt.bar(
        [r["algorithm"] for r in csp],
        [r["assignments"] for r in csp]
    )
    plt.ylabel("Assignments Tried")
    plt.xlabel("Algorithm")
    plt.title("8-Queens CSP: Assignment Comparison")
    plt.tight_layout()
    plt.savefig(GRAPH_DIR / "csp_assignments.png", dpi=200)
    plt.close()


def print_console_results(results):
    print("\n" + "=" * 80)
    print("AI SEARCH ALGORITHMS - PERFORMANCE EVALUATION")
    print("=" * 80)

    print("\n8-PUZZLE RESULTS")
    print("-" * 80)
    print(
        f"{'Algorithm':<22}"
        f"{'Time(ms)':>12}"
        f"{'Explored':>12}"
        f"{'Cost':>10}"
        f"{'Solved':>10}"
    )

    for r in results["puzzle"]:
        print(
            f"{r['algorithm']:<22}"
            f"{r['time_ms']:>12.4f}"
            f"{r['nodes_explored']:>12}"
            f"{str(r['path_cost']):>10}"
            f"{str(r['success']):>10}"
        )

    print("\n8-QUEENS RESULTS")
    print("-" * 80)
    print(
        f"{'Algorithm':<22}"
        f"{'Time(ms)':>12}"
        f"{'Iterations':>12}"
        f"{'Conflicts':>12}"
        f"{'Solved':>10}"
    )

    for r in results["queens"]:
        print(
            f"{r['algorithm']:<22}"
            f"{r['time_ms']:>12.4f}"
            f"{str(r.get('iterations', '-')):>12}"
            f"{str(r.get('final_conflicts', '-')):>12}"
            f"{str(r['success']):>10}"
        )

    print("\nCSP DETAILS")
    print("-" * 80)
    for r in results["queens"][2:]:
        print(
            f"{r['algorithm']}: "
            f"Assignments={r['assignments']}, "
            f"Backtracks={r['backtracks']}, "
            f"Time={r['time_ms']:.4f} ms"
        )

    print("\nFiles generated:")
    print(f"- {OUTPUT_DIR / 'complete_output.txt'}")
    print(f"- {RESULT_DIR / 'performance_results.csv'}")
    print(f"- {GRAPH_DIR / 'execution_time.png'}")
    print(f"- {GRAPH_DIR / 'nodes_explored.png'}")
    print(f"- {GRAPH_DIR / 'path_cost.png'}")
    print(f"- {GRAPH_DIR / 'local_search_conflicts.png'}")
    print(f"- {GRAPH_DIR / 'csp_assignments.png'}")


def main():
    print("Running search algorithm evaluation...")

    puzzle_results = [
        bfs(),
        dfs(),
        uniform_cost_search(),
        greedy_best_first(),
        a_star(),
    ]

    # Fixed seed makes local-search experiments reproducible.
    queens_results = [
        hill_climbing(seed=42),
        simulated_annealing(seed=42),
        solve_backtracking(),
        solve_forward_checking(),
    ]

    results = {
        "puzzle": puzzle_results,
        "queens": queens_results,
    }

    write_text_output(results)
    write_csv(results)
    make_graphs(results)
    print_console_results(results)


if __name__ == "__main__":
    main()
