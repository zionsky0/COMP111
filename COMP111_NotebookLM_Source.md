# COMP111 Artificial Intelligence: Master Interactive Curriculum and Codebase Documentation

## Overview
This document consolidates the complete architecture, theory, algorithms, heuristics, and mathematical foundations implemented in the COMP111 Artificial Intelligence repository.

---

## Unit 01: Classical State-Space Search
- Problem Formulation: State representation, Successor function Actions(s), Transition model Result(s, a), Step-cost c(s, a, s'), Goal-test Goal(s), Path-cost g(n).
- Uninformed Search Strategies:
  * Breadth-First Search (BFS): FIFO queue. Complete, optimal when all step costs are equal (c = 1). Time complexity O(b^d), Space complexity O(b^d).
  * Depth-First Search (DFS): LIFO stack. Complete on finite acyclic graphs, not optimal. Time O(b^m), Space O(b*m).
  * Uniform-Cost Search (UCS / Dijkstra): Priority queue ordered by g(n). Optimal for any positive step costs c >= eps > 0.
- Informed (Heuristic) Search:
  * Greedy Best-First Search: Priority queue ordered by h(n). Fast but neither complete in infinite spaces nor optimal.
  * A* Search: Priority queue ordered by evaluation function f(n) = g(n) + h(n).
  * Admissibility: An admissible heuristic never overestimates the true cost to the goal, i.e., h(n) <= h*(n). Guarantees A* tree search optimality.
  * Consistency (Monotonicity): h(n) <= c(n, a, n') + h(n') and h(G) = 0. Guarantees that f(n) never decreases along any path and that the first time a node is expanded in graph search, its optimal path is found.

---

## Unit 02: Heuristics, Sliding Tiles, & Optimization
- 8-Puzzle / 15-Puzzle Sliding Tiles Benchmark:
  * State space size: 9! / 2 = 181,440 reachable states for 8-Puzzle; 16! / 2 for 15-Puzzle.
  * Solvability: Inversion parity check. If parity of inversions matches blank-tile row parity rules, the configuration is reachable.
  * Heuristic Quality & Dominance:
    - h1: Misplaced Tiles. Number of tiles currently not in their target coordinates.
    - h2: Manhattan Distance. Sum of horizontal and vertical distances of each tile from its target. Dominates h1: h2(n) >= h1(n) for all n.
    - h3: Linear Conflict. Manhattan distance plus 2 * (number of pairs of tiles in the same row/col that must pass each other to reach goal). Dominates h2: h3(n) >= h2(n).
- Local Search & Metaheuristics:
  * Hill-Climbing: Greedy local ascent; prone to local optima, ridges, and plateaus.
  * Simulated Annealing: Escapes local optima using the Metropolis acceptance criterion: if delta_E < 0 accept; else accept with probability exp(-delta_E / T), where temperature T cools over time.

---

## Unit 03: Adversarial Search & Two-Player Zero-Sum Games
- Minimax Decision Rule:
  * MAX aims to maximize utility; MIN aims to minimize utility.
  * Minimax Value: V(s) = max_a V(Result(s, a)) for MAX; min_a V(Result(s, a)) for MIN; Utility(s) for terminal states.
- Alpha-Beta Pruning:
  * alpha: Value of the best (highest-value) choice found so far along the path for MAX.
  * beta: Value of the best (lowest-value) choice found so far along the path for MIN.
  * Pruning condition: Whenever alpha >= beta, the remaining children at the current node cannot affect the root decision and are pruned.
  * Optimal node ordering reduces time complexity from O(b^d) to O(b^(d/2)), effectively doubling the searchable depth.

---

## Unit 04: Constraint Satisfaction Problems (CSPs)
- Formal Representation: Variables X = {X1, ..., Xn}, Domains D = {D1, ..., Dn}, Constraints C = {C1, ..., Cm}.
- Constraint Propagation:
  * Arc Consistency (AC-3 Algorithm): Directed arc (Xi, Xj) is consistent if for every value x in Di, there exists some value y in Dj satisfying the binary constraint. Prunes domains before or during search.
- Backtracking Heuristics:
  * MRV (Minimum Remaining Values / Most Constrained Variable): Choose the variable with the fewest allowable domain values remaining.
  * Degree Heuristic: Tie-breaker for MRV; choose the variable involved in the most constraints with unassigned variables.
  * LCV (Least Constraining Value): Order domain values to rule out the fewest choices for neighboring unassigned variables.

---

## Unit 05: Knowledge Representation & Logical Inference
- Propositional Logic & CNF:
  * Conjunctive Normal Form (CNF): Conjunction of disjunctions of literals (clauses).
  * Resolution Refutation Rule: Given (A v B) and (~B v C), resolve on complementary literal B to infer resolvent (A v C).
  * Proof Procedure: To prove KB |= alpha, assert KB & ~alpha in CNF and resolve until the empty clause (contradiction) is derived.
- Horn Clauses & Forward Chaining:
  * Definite clauses (exactly one positive literal): (p1 & p2 & ... & pk) -> q.
  * Forward Chaining: Linear-time inference driven by known facts and matching rule premises.

---

## Unit 06: Sequential Decisions & Active Inference
- Markov Decision Processes (MDPs):
  * Tuple: <S, A, P(s'|s, a), R(s, a, s'), gamma>.
  * Bellman Optimality Equation:
    V*(s) = max_a sum_{s'} P(s'|s, a) [R(s, a, s') + gamma * V*(s')]
  * Value Iteration: Dynamic programming algorithm that iteratively updates V(s) until max change is below threshold theta. Guarantees convergence to the unique optimal value function.
- Active Inference & Free Energy Principle (FEP):
  * Agents maintain internal beliefs Q(s) over hidden states and sensory observation likelihood P(o|s).
  * Variational Free Energy: F = E_Q[ln Q(s) - ln P(s, o)] = D_KL(Q(s) || P(s)) - E_Q[ln P(o|s)].
  * Perception updates Q(s) to minimize free energy; Action modifies the world to make observations match prior preferences.
