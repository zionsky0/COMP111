# Unit 06: Markov Decision Processes & Active Inference Fundamentals
# COMP111 - Artificial Intelligence

import math
from typing import Dict, List, Tuple

class GridWorldMDP:
    """
    GridWorld MDP with stochastic transitions.
    States: (row, col)
    Actions: UP, DOWN, LEFT, RIGHT
    Stochastic: 0.8 intended, 0.1 perpendicular left, 0.1 perpendicular right
    """
    ACTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT']

    def __init__(self, rows: int = 3, cols: int = 4, terminals: Dict[Tuple[int, int], float] = None, obstacles: List[Tuple[int, int]] = None, gamma: float = 0.9):
        self.rows = rows
        self.cols = cols
        self.terminals = terminals or {(0, 3): 1.0, (1, 3): -1.0}
        self.obstacles = set(obstacles or [(1, 1)])
        self.gamma = gamma

    def states(self) -> List[Tuple[int, int]]:
        s_list = []
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) not in self.obstacles:
                    s_list.append((r, c))
        return s_list

    def transitions(self, state: Tuple[int, int], action: str) -> List[Tuple[float, Tuple[int, int], float]]:
        """Returns list of (prob, next_state, reward)."""
        if state in self.terminals:
            return [(1.0, state, 0.0)]

        directions = {
            'UP': (-1, 0),
            'DOWN': (1, 0),
            'LEFT': (0, -1),
            'RIGHT': (0, 1)
        }
        perpendicular = {
            'UP': ['LEFT', 'RIGHT'],
            'DOWN': ['LEFT', 'RIGHT'],
            'LEFT': ['UP', 'DOWN'],
            'RIGHT': ['UP', 'DOWN']
        }

        def step(s, a):
            dr, dc = directions[a]
            nr, nc = s[0] + dr, s[1] + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and (nr, nc) not in self.obstacles:
                return (nr, nc)
            return s # bump into wall

        intended_state = step(state, action)
        left_state = step(state, perpendicular[action][0])
        right_state = step(state, perpendicular[action][1])

        outcomes = [
            (0.8, intended_state),
            (0.1, left_state),
            (0.1, right_state)
        ]

        results = []
        for prob, ns in outcomes:
            reward = -0.04  # standard step cost
            results.append((prob, ns, reward))
        return results

    def value_iteration(self, theta: float = 1e-4) -> Tuple[Dict[Tuple[int, int], float], Dict[Tuple[int, int], str]]:
        """
        Solves Bellman Optimality Equation iteratively:
        V(s) <- max_a sum_{s'} P(s'|s,a) [R + gamma * V(s')]
        """
        states = self.states()
        V = {s: 0.0 for s in states}
        for term, r in self.terminals.items():
            V[term] = r

        while True:
            delta = 0.0
            new_V = dict(V)
            for s in states:
                if s in self.terminals:
                    continue
                q_vals = []
                for a in self.ACTIONS:
                    q = sum(p * (r + self.gamma * V[ns]) for p, ns, r in self.transitions(s, a))
                    q_vals.append(q)
                best_q = max(q_vals)
                delta = max(delta, abs(best_q - V[s]))
                new_V[s] = best_q
            V = new_V
            if delta < theta:
                break

        # Extract optimal policy
        policy = {}
        for s in states:
            if s in self.terminals:
                policy[s] = 'TERM'
                continue
            best_a = max(self.ACTIONS, key=lambda a: sum(p * (r + self.gamma * V[ns]) for p, ns, r in self.transitions(s, a)))
            policy[s] = best_a

        return V, policy

class ActiveInferenceToyAgent:
    """
    Minimal pedagogical demonstration of Active Inference & Free Energy Principle (FEP).
    Agent maintains internal beliefs Q(s), receives observations o,
    and acts to minimize expected free energy (aligning world with prior preferences P(o)).
    """
    def __init__(self, prior_preferences: Dict[int, float]):
        self.preferences = prior_preferences # P(o): preferred observations
        self.beliefs = {0: 0.5, 1: 0.5} # Q(s)

    def variational_free_energy(self, obs: int) -> float:
        """
        F = E_q[ln Q(s) - ln P(s, o)] = KL(Q(s) || P(s)) - E_q[ln P(o|s)]
        Simplified discrete surrogate.
        """
        fe = 0.0
        for s, q_s in self.beliefs.items():
            if q_s > 1e-6:
                p_o_given_s = 0.9 if s == obs else 0.1
                fe += q_s * (math.log(q_s) - math.log(p_o_given_s * self.preferences.get(obs, 0.5)))
        return fe
