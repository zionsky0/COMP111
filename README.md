# COMP111: Artificial Intelligence — Interactive Master Curriculum

Welcome to the interactive companion and codebase for **COMP111 - Artificial Intelligence**.

This repository is designed as an end-to-end, runnable, pedagogical master suite covering the core theoretical foundations, algorithmic mechanics, heuristics, search strategies, game theory, constraint satisfaction, logic, and intelligent agent principles.

---

## 📚 Curriculum Overview

1. **Unit 01: Foundations and Classical Search**
   - Breadth-First Search (BFS)
   - Depth-First Search (DFS) & Depth-Limited Search (DLS)
   - Iterative Deepening Search (IDS)
   - Uniform Cost Search (UCS / Dijkstra)
   - Greedy Best-First Search
   - A* Search (admissibility & consistency)

2. **Unit 02: Heuristic Optimization & Sliding Tiles**
   - 8-Puzzle and 15-Puzzle state spaces
   - Heuristics: Misplaced tiles, Manhattan distance, Linear conflict
   - Local search: Hill Climbing, Simulated Annealing, Genetic Algorithms

3. **Unit 03: Adversarial Search & Game Theory**
   - Minimax decision rule
   - Alpha-Beta Pruning with move ordering
   - Horizon cutoff & evaluation functions
   - Expectiminimax (chance/stochastic games)

4. **Unit 04: Constraint Satisfaction Problems (CSP)**
   - Backtracking search
   - MRV (Minimum Remaining Values) & Degree heuristic
   - LCV (Least Constraining Value)
   - AC-3 (Arc Consistency) & Forward Checking
   - Benchmarks: Map Coloring, N-Queens, Sudoku

5. **Unit 05: Knowledge Representation & Logic**
   - Propositional logic & truth tables
   - Inference via Resolution in CNF
   - Forward Chaining & Backward Chaining (definite clauses)
   - First-Order Logic basics

6. **Unit 06: Sequential Decisions & Active Inference**
   - Markov Decision Processes (MDPs)
   - Bellman Optimality Equation
   - Value Iteration & Policy Iteration
   - Active Inference: Generative models and Free Energy minimization

---

## 🚀 Running the Interactive CLI Tutor

Run the master interactive terminal tutor:
`ash
python run_tutor.py
`
Or run the full test suite:
`ash
python -m unittest discover tests
`
