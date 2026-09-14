# Unit 02: Heuristics & Local Optimization
# COMP111 - Artificial Intelligence

import math
import random
from typing import List, Tuple, Optional, Callable, Any
from unit_01_search.search_algorithms import Problem

class EightPuzzle(Problem):
    """
    Classic 8-Puzzle sliding tile problem.
    State representation: tuple of 9 integers, 0 represents blank tile.
    Example goal: (1, 2, 3, 4, 5, 6, 7, 8, 0)
    """
    GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    def __init__(self, initial_state: Tuple[int, ...], goal_state: Tuple[int, ...] = GOAL):
        super().__init__(initial_state, goal_state)

    def actions(self, state: Tuple[int, ...]) -> List[str]:
        blank = state.index(0)
        row, col = divmod(blank, 3)
        valid = []
        if row > 0: valid.append('UP')
        if row < 2: valid.append('DOWN')
        if col > 0: valid.append('LEFT')
        if col < 2: valid.append('RIGHT')
        return valid

    def result(self, state: Tuple[int, ...], action: str) -> Tuple[int, ...]:
        blank = state.index(0)
        row, col = divmod(blank, 3)
        if action == 'UP': target = (row - 1) * 3 + col
        elif action == 'DOWN': target = (row + 1) * 3 + col
        elif action == 'LEFT': target = row * 3 + (col - 1)
        elif action == 'RIGHT': target = row * 3 + (col + 1)
        else: raise ValueError(f'Invalid action {action}')

        s = list(state)
        s[blank], s[target] = s[target], s[blank]
        return tuple(s)

    def is_solvable(self) -> bool:
        inv = 0
        arr = [x for x in self.initial_state if x != 0]
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                if arr[i] > arr[j]:
                    inv += 1
        return inv % 2 == 0

    @staticmethod
    def h_misplaced(state: Tuple[int, ...], goal: Tuple[int, ...] = GOAL) -> float:
        """h1: Number of misplaced tiles (excluding blank). Admissible."""
        return sum(1 for i in range(9) if state[i] != 0 and state[i] != goal[i])

    @staticmethod
    def h_manhattan(state: Tuple[int, ...], goal: Tuple[int, ...] = GOAL) -> float:
        """h2: Sum of Manhattan distances of tiles to goal positions. Admissible and dominates h1."""
        dist = 0
        goal_pos = {val: (i // 3, i % 3) for i, val in enumerate(goal)}
        for i, val in enumerate(state):
            if val != 0:
                r, c = divmod(i, 3)
                gr, gc = goal_pos[val]
                dist += abs(r - gr) + abs(c - gc)
        return float(dist)

    @staticmethod
    def h_linear_conflict(state: Tuple[int, ...], goal: Tuple[int, ...] = GOAL) -> float:
        """h3: Manhattan distance + 2 * linear conflicts. Dominates Manhattan."""
        base_md = EightPuzzle.h_manhattan(state, goal)
        conflicts = 0
        goal_pos = {val: (i // 3, i % 3) for i, val in enumerate(goal)}

        # Row conflicts
        for r in range(3):
            row_tiles = [state[r * 3 + c] for c in range(3) if state[r * 3 + c] != 0]
            for i in range(len(row_tiles)):
                for j in range(i + 1, len(row_tiles)):
                    t1, t2 = row_tiles[i], row_tiles[j]
                    if goal_pos[t1][0] == r and goal_pos[t2][0] == r:
                        if goal_pos[t1][1] > goal_pos[t2][1]:
                            conflicts += 1

        # Column conflicts
        for c in range(3):
            col_tiles = [state[r * 3 + c] for r in range(3) if state[r * 3 + c] != 0]
            for i in range(len(col_tiles)):
                for j in range(i + 1, len(col_tiles)):
                    t1, t2 = col_tiles[i], col_tiles[j]
                    if goal_pos[t1][1] == c and goal_pos[t2][1] == c:
                        if goal_pos[t1][0] > goal_pos[t2][0]:
                            conflicts += 1

        return float(base_md + 2 * conflicts)

    def heuristic(self, state: Tuple[int, ...]) -> float:
        return self.h_manhattan(state, self.goal_state)

def simulated_annealing(initial_state: Any,
                        neighbor_fn: Callable[[Any], List[Any]],
                        cost_fn: Callable[[Any], float],
                        initial_temp: float = 1000.0,
                        cooling_rate: float = 0.95,
                        min_temp: float = 1e-3,
                        max_iterations: int = 2000) -> Tuple[Any, float, List[float]]:
    """
    Simulated Annealing metaheuristic.
    Escapes local optima using Metropolis acceptance probability: exp(-delta_E / T).
    """
    current = initial_state
    current_cost = cost_fn(current)
    best = current
    best_cost = current_cost

    temp = initial_temp
    history = [current_cost]

    for _ in range(max_iterations):
        if temp < min_temp or best_cost == 0:
            break

        neighbors = neighbor_fn(current)
        if not neighbors:
            break
        neighbor = random.choice(neighbors)
        neighbor_cost = cost_fn(neighbor)
        delta_e = neighbor_cost - current_cost

        if delta_e < 0 or random.random() < math.exp(-delta_e / temp):
            current = neighbor
            current_cost = neighbor_cost
            if current_cost < best_cost:
                best = current
                best_cost = current_cost

        history.append(current_cost)
        temp *= cooling_rate

    return best, best_cost, history
