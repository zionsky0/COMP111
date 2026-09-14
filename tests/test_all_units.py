# Comprehensive Test Suite for COMP111 Modules
import unittest
from unit_01_search.search_algorithms import (
    GraphSearchProblem, breadth_first_search, depth_first_search,
    uniform_cost_search, a_star_search, depth_limited_search, iterative_deepening_search
)
from unit_02_heuristics_optimization.puzzle_and_heuristics import EightPuzzle
from unit_03_adversarial_games.minimax_alphabeta import TicTacToe, MinimaxAgent
from unit_04_constraint_satisfaction.csp_solver import create_australia_map_csp, backtracking_search, ac3
from unit_05_logic_and_reasoning.logic_engines import PropositionalResolution, HornClauseKB
from unit_06_markov_and_active_inference.mdp_and_active_inference import GridWorldMDP

class TestSearchAlgorithms(unittest.TestCase):
    def setUp(self):
        self.graph = {
            'A': {'B': 1.0, 'C': 4.0},
            'B': {'D': 2.0, 'E': 5.0},
            'C': {'E': 1.0},
            'D': {'E': 1.0},
            'E': {}
        }
        self.heuristics = {'A': 3.0, 'B': 2.0, 'C': 1.0, 'D': 1.0, 'E': 0.0}
        self.problem = GraphSearchProblem('A', 'E', self.graph, self.heuristics)

    def test_bfs(self):
        res = breadth_first_search(self.problem)
        self.assertTrue(res.success)
        self.assertEqual(res.path[-1], 'E')

    def test_ucs(self):
        res = uniform_cost_search(self.problem)
        self.assertTrue(res.success)
        self.assertEqual(res.cost, 4.0) # A -> B -> D -> E (1+2+1=4) vs A->C->E (4+1=5)

    def test_astar(self):
        res = a_star_search(self.problem)
        self.assertTrue(res.success)
        self.assertEqual(res.cost, 4.0)

    def test_dls_and_ids(self):
        # Goal E is at depth 2 via C, depth 3 via D
        # DLS with limit 1 should fail
        dls_fail = depth_limited_search(self.problem, limit=1)
        self.assertFalse(dls_fail.success)

        # DLS with limit 2 finds a depth-2 path to E
        dls_succ = depth_limited_search(self.problem, limit=2)
        self.assertTrue(dls_succ.success)
        self.assertEqual(len(dls_succ.path), 3)
        self.assertEqual(dls_succ.path[-1], 'E')

        # IDS finds optimal path by hops (depth 2)
        ids_res = iterative_deepening_search(self.problem)
        self.assertTrue(ids_res.success)
        self.assertEqual(len(ids_res.path), 3)
        self.assertEqual(ids_res.path[-1], 'E')

class TestHeuristics(unittest.TestCase):
    def test_heuristics_dominance(self):
        # Initial state 2 moves away from goal
        state = (1, 2, 3, 4, 0, 5, 7, 8, 6)
        h1 = EightPuzzle.h_misplaced(state)
        h2 = EightPuzzle.h_manhattan(state)
        h3 = EightPuzzle.h_linear_conflict(state)
        self.assertTrue(h3 >= h2 >= h1)

class TestGameTheory(unittest.TestCase):
    def test_tic_tac_toe_unbeatable(self):
        agent = MinimaxAgent()
        game = TicTacToe()
        move, val = agent.get_best_move(game)
        self.assertIsNotNone(move)
        # Optimal play from empty board leads to a draw (utility 0.0)
        self.assertEqual(val, 0.0)

class TestCSP(unittest.TestCase):
    def test_australia_coloring(self):
        csp = create_australia_map_csp()
        self.assertTrue(ac3(csp))
        solution = backtracking_search(csp)
        self.assertIsNotNone(solution)
        for var, neighbors in csp.neighbors.items():
            for n in neighbors:
                self.assertNotEqual(solution[var], solution[n])

class TestLogic(unittest.TestCase):
    def test_resolution(self):
        # KB: A or B, ~A. Prove: B
        kb = {frozenset({'A', 'B'}), frozenset({'~A'})}
        alpha = {frozenset({'~B'})}
        self.assertTrue(PropositionalResolution.pl_resolution(kb, alpha))

    def test_forward_chaining(self):
        # A & B -> C, C -> D. Facts: A, B. Query: D
        clauses = [
            (['A', 'B'], 'C'),
            (['C'], 'D')
        ]
        kb = HornClauseKB(clauses)
        self.assertTrue(kb.pl_fc_entails({'A', 'B'}, 'D'))
        self.assertFalse(kb.pl_fc_entails({'A'}, 'D'))

class TestMDP(unittest.TestCase):
    def test_value_iteration(self):
        mdp = GridWorldMDP()
        V, policy = mdp.value_iteration()
        self.assertGreater(V[(0, 2)], 0.5) # State next to +1 goal
        self.assertEqual(policy[(0, 3)], 'TERM')

if __name__ == '__main__':
    unittest.main()
