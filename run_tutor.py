# COMP111 Interactive CLI Tutor
import sys
import subprocess

def banner():
    print('''
========================================================================
   COMP111: ARTIFICIAL INTELLIGENCE - INTERACTIVE TUTOR
========================================================================
 Curriculum Units:
   [1] Classical Search & Heuristics (BFS, UCS, A*)
   [2] 8-Puzzle Sliding Tiles & Heuristics (Misplaced, Manhattan, Linear)
   [3] Adversarial Games (Minimax & Alpha-Beta Pruning)
   [4] Constraint Satisfaction Problems (AC-3 & Map-Coloring)
   [5] Logical Inference (Propositional Resolution & Forward Chaining)
   [6] Markov Decision Processes (GridWorld Value Iteration)
   [7] Run Complete Automated Verification Suite
   [0] Exit
========================================================================
''')

def run_search_demo():
    from unit_01_search.search_algorithms import GraphSearchProblem, breadth_first_search, uniform_cost_search, a_star_search
    print('\n--- [1] SEARCH ALGORITHMS COMPARISON ---')
    graph = {
        'Arad': {'Zerind': 75.0, 'Sibiu': 140.0, 'Timisoara': 118.0},
        'Zerind': {'Arad': 75.0, 'Oradea': 71.0},
        'Oradea': {'Zerind': 71.0, 'Sibiu': 151.0},
        'Sibiu': {'Arad': 140.0, 'Oradea': 151.0, 'Fagaras': 99.0, 'Rimnicu Vilcea': 80.0},
        'Timisoara': {'Arad': 118.0, 'Lugoj': 111.0},
        'Lugoj': {'Timisoara': 111.0, 'Mehadia': 70.0},
        'Mehadia': {'Lugoj': 70.0, 'Drobeta': 75.0},
        'Drobeta': {'Mehadia': 75.0, 'Craiova': 120.0},
        'Craiova': {'Drobeta': 120.0, 'Rimnicu Vilcea': 146.0, 'Pitesti': 138.0},
        'Rimnicu Vilcea': {'Sibiu': 80.0, 'Craiova': 146.0, 'Pitesti': 97.0},
        'Fagaras': {'Sibiu': 99.0, 'Bucharest': 211.0},
        'Pitesti': {'Rimnicu Vilcea': 97.0, 'Craiova': 138.0, 'Bucharest': 101.0},
        'Bucharest': {'Fagaras': 211.0, 'Pitesti': 101.0}
    }
    h_bucharest = {
        'Arad': 366.0, 'Zerind': 374.0, 'Oradea': 380.0, 'Sibiu': 253.0,
        'Timisoara': 329.0, 'Lugoj': 244.0, 'Mehadia': 241.0, 'Drobeta': 242.0,
        'Craiova': 160.0, 'Rimnicu Vilcea': 193.0, 'Fagaras': 176.0,
        'Pitesti': 100.0, 'Bucharest': 0.0
    }
    prob = GraphSearchProblem('Arad', 'Bucharest', graph, h_bucharest)

    for name, fn in [('BFS', breadth_first_search), ('UCS', uniform_cost_search), ('A*', a_star_search)]:
        res = fn(prob)
        print(f'[{name}] Success: {res.success} | Cost: {res.cost:.1f} | Expanded Nodes: {res.nodes_expanded} | Path: {res.path}')

def run_puzzle_demo():
    from unit_02_heuristics_optimization.puzzle_and_heuristics import EightPuzzle
    from unit_01_search.search_algorithms import a_star_search
    print('\n--- [2] 8-PUZZLE HEURISTIC DOMINANCE ---')
    state = (1, 2, 3, 0, 4, 6, 7, 5, 8)
    puzzle = EightPuzzle(state)
    print(f'Starting State: {state}')
    print(f'  h1 (Misplaced Tiles):     {EightPuzzle.h_misplaced(state):.0f}')
    print(f'  h2 (Manhattan Distance):  {EightPuzzle.h_manhattan(state):.0f}')
    print(f'  h3 (Linear Conflict):     {EightPuzzle.h_linear_conflict(state):.0f}')
    print('Dominance Property: h3 >= h2 >= h1 holds everywhere on the state space.')
    
    res = a_star_search(puzzle, EightPuzzle.h_manhattan)
    print(f'A* with Manhattan solved in {len(res.actions)} moves with {res.nodes_expanded} nodes expanded.')

def run_games_demo():
    from unit_03_adversarial_games.minimax_alphabeta import TicTacToe, MinimaxAgent
    print('\n--- [3] ADVERSARIAL GAMES (MINIMAX + ALPHA-BETA) ---')
    game = TicTacToe()
    agent = MinimaxAgent()
    move, val = agent.get_best_move(game)
    print(f'Root evaluation: {val} (0.0 means optimal draw)')
    print(f'Nodes evaluated: {agent.nodes_evaluated} | Pruning events: {agent.prunings}')

def run_csp_demo():
    from unit_04_constraint_satisfaction.csp_solver import create_australia_map_csp, backtracking_search, ac3
    print('\n--- [4] CONSTRAINT SATISFACTION (AUSTRALIA MAP COLORING) ---')
    csp = create_australia_map_csp()
    print(f'Running AC-3 Preprocessing: Arc-consistent? {ac3(csp)}')
    solution = backtracking_search(csp, mrv=True, lcv=True)
    print('Solution found with MRV & LCV:')
    for k, v in sorted(solution.items()):
        print(f'  {k}: {v}')

def run_logic_demo():
    from unit_05_logic_and_reasoning.logic_engines import PropositionalResolution, HornClauseKB
    print('\n--- [5] LOGICAL REASONING ---')
    kb = {frozenset({'A', 'B'}), frozenset({'~A'})}
    query = {frozenset({'~B'})}
    proved = PropositionalResolution.pl_resolution(kb, query)
    print(f'Resolution Proof: KB {{A v B, ~A}} entails B? {proved}')

def run_mdp_demo():
    from unit_06_markov_and_active_inference.mdp_and_active_inference import GridWorldMDP
    print('\n--- [6] MARKOV DECISION PROCESS (GRIDWORLD) ---')
    mdp = GridWorldMDP()
    V, policy = mdp.value_iteration()
    print('Optimal State Values V*(s):')
    for r in range(mdp.rows):
        row_str = ' | '.join(f'({r},{c}): {V.get((r,c), 0.0):+0.2f}' for c in range(mdp.cols) if (r, c) not in mdp.obstacles)
        print(f'  {row_str}')

def run_all_tests():
    print('\n--- RUNNING FULL TEST SUITE ---')
    subprocess.run([sys.executable, '-m', 'unittest', 'discover', 'tests'])

def main():
    while True:
        banner()
        try:
            choice = input('Select an option (0-7): ').strip()
        except EOFError:
            break
        if choice == '1': run_search_demo()
        elif choice == '2': run_puzzle_demo()
        elif choice == '3': run_games_demo()
        elif choice == '4': run_csp_demo()
        elif choice == '5': run_logic_demo()
        elif choice == '6': run_mdp_demo()
        elif choice == '7': run_all_tests()
        elif choice == '0':
            print('Goodbye!')
            break
        else:
            print('Invalid choice.')
        try:
            input('\nPress Enter to continue...')
        except EOFError:
            break

if __name__ == '__main__':
    main()
