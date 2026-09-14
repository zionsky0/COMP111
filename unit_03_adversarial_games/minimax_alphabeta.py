# Unit 03: Adversarial Search & Two-Player Zero-Sum Games
# COMP111 - Artificial Intelligence

from typing import List, Tuple, Optional, Any, Dict

class GameState:
    """Abstract game state interface for adversarial games."""
    def is_terminal(self) -> bool:
        raise NotImplementedError

    def utility(self, player: int) -> float:
        raise NotImplementedError

    def legal_moves(self) -> List[Any]:
        raise NotImplementedError

    def next_state(self, move: Any) -> 'GameState':
        raise NotImplementedError

    def current_player(self) -> int: # +1 for MAX, -1 for MIN
        raise NotImplementedError

class TicTacToe(GameState):
    """Tic-Tac-Toe formal game state."""
    def __init__(self, board: Optional[List[int]] = None, turn: int = 1):
        self.board = board or [0] * 9 # 1 for X (MAX), -1 for O (MIN), 0 empty
        self.turn = turn

    def current_player(self) -> int:
        return self.turn

    def legal_moves(self) -> List[int]:
        if self._check_winner() != 0 or 0 not in self.board:
            return []
        return [i for i, v in enumerate(self.board) if v == 0]

    def next_state(self, move: int) -> 'TicTacToe':
        nb = list(self.board)
        nb[move] = self.turn
        return TicTacToe(nb, -self.turn)

    def _check_winner(self) -> int:
        wins = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for a, b, c in wins:
            if self.board[a] != 0 and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return 0

    def is_terminal(self) -> bool:
        return self._check_winner() != 0 or (0 not in self.board)

    def utility(self, player: int = 1) -> float:
        w = self._check_winner()
        return float(w * player)

    def display(self) -> str:
        symbols = {1: 'X', -1: 'O', 0: '.'}
        rows = []
        for r in range(3):
            row = [symbols[self.board[r * 3 + c]] for c in range(3)]
            rows.append(' '.join(row))
        return '\n'.join(rows)

class MinimaxAgent:
    """Minimax with Alpha-Beta Pruning."""
    def __init__(self, depth_limit: int = 9):
        self.depth_limit = depth_limit
        self.nodes_evaluated = 0
        self.prunings = 0

    def get_best_move(self, state: GameState) -> Tuple[Optional[Any], float]:
        self.nodes_evaluated = 0
        self.prunings = 0
        player = state.current_player()

        best_move = None
        if player == 1: # MAX
            val = float('-inf')
            alpha = float('-inf')
            beta = float('inf')
            for move in state.legal_moves():
                child = state.next_state(move)
                child_val = self._min_value(child, 1, alpha, beta)
                if child_val > val:
                    val = child_val
                    best_move = move
                alpha = max(alpha, val)
            return best_move, val
        else: # MIN
            val = float('inf')
            alpha = float('-inf')
            beta = float('inf')
            for move in state.legal_moves():
                child = state.next_state(move)
                child_val = self._max_value(child, 1, alpha, beta)
                if child_val < val:
                    val = child_val
                    best_move = move
                beta = min(beta, val)
            return best_move, val

    def _max_value(self, state: GameState, depth: int, alpha: float, beta: float) -> float:
        self.nodes_evaluated += 1
        if state.is_terminal() or depth >= self.depth_limit:
            return state.utility(1)

        v = float('-inf')
        for move in state.legal_moves():
            child = state.next_state(move)
            v = max(v, self._min_value(child, depth + 1, alpha, beta))
            if v >= beta:
                self.prunings += 1
                return v # beta cut-off
            alpha = max(alpha, v)
        return v

    def _min_value(self, state: GameState, depth: int, alpha: float, beta: float) -> float:
        self.nodes_evaluated += 1
        if state.is_terminal() or depth >= self.depth_limit:
            return state.utility(1)

        v = float('inf')
        for move in state.legal_moves():
            child = state.next_state(move)
            v = min(v, self._max_value(child, depth + 1, alpha, beta))
            if v <= alpha:
                self.prunings += 1
                return v # alpha cut-off
            beta = min(beta, v)
        return v
