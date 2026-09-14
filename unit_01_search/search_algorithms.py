# Classical Search Algorithms Module
# COMP111 - Artificial Intelligence

import heapq
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

@dataclass(order=True)
class PriorityItem:
    priority: float
    count: int
    item: Any = field(compare=False)

class SearchNode:
    def __init__(self, state: Any, parent: Optional['SearchNode'] = None, action: Any = None, path_cost: float = 0.0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0 if parent is None else parent.depth + 1

    def path(self) -> List['SearchNode']:
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def solution(self) -> List[Any]:
        return [node.action for node in self.path()[1:]]

    def __repr__(self) -> str:
        return f'<Node state={self.state} cost={self.path_cost}>'

class Problem:
    def __init__(self, initial_state: Any, goal_state: Optional[Any] = None):
        self.initial_state = initial_state
        self.goal_state = goal_state

    def actions(self, state: Any) -> List[Any]:
        raise NotImplementedError

    def result(self, state: Any, action: Any) -> Any:
        raise NotImplementedError

    def is_goal(self, state: Any) -> bool:
        return state == self.goal_state

    def step_cost(self, state: Any, action: Any, next_state: Any) -> float:
        return 1.0

    def heuristic(self, state: Any) -> float:
        return 0.0

@dataclass
class SearchResult:
    algorithm: str
    success: bool
    path: List[Any]
    actions: List[Any]
    cost: float
    nodes_expanded: int
    max_frontier_size: int

def breadth_first_search(problem: Problem) -> SearchResult:
    initial_node = SearchNode(problem.initial_state)
    if problem.is_goal(initial_node.state):
        return SearchResult('BFS', True, [initial_node.state], [], 0.0, 0, 1)

    frontier = deque([initial_node])
    explored: Set[Any] = {problem.initial_state}
    nodes_expanded = 0
    max_frontier = 1

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        node = frontier.popleft()
        nodes_expanded += 1

        for action in problem.actions(node.state):
            child_state = problem.result(node.state, action)
            if child_state not in explored:
                cost = node.path_cost + problem.step_cost(node.state, action, child_state)
                child = SearchNode(child_state, node, action, cost)
                if problem.is_goal(child.state):
                    return SearchResult(
                        'BFS', True, [n.state for n in child.path()],
                        child.solution(), child.path_cost, nodes_expanded, max_frontier
                    )
                explored.add(child_state)
                frontier.append(child)

    return SearchResult('BFS', False, [], [], float('inf'), nodes_expanded, max_frontier)

def depth_first_search(problem: Problem) -> SearchResult:
    frontier = [SearchNode(problem.initial_state)]
    explored: Set[Any] = set()
    nodes_expanded = 0
    max_frontier = 1

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        node = frontier.pop()
        if problem.is_goal(node.state):
            return SearchResult(
                'DFS', True, [n.state for n in node.path()],
                node.solution(), node.path_cost, nodes_expanded, max_frontier
            )

        if node.state not in explored:
            explored.add(node.state)
            nodes_expanded += 1
            for action in reversed(problem.actions(node.state)):
                child_state = problem.result(node.state, action)
                if child_state not in explored:
                    cost = node.path_cost + problem.step_cost(node.state, action, child_state)
                    frontier.append(SearchNode(child_state, node, action, cost))

    return SearchResult('DFS', False, [], [], float('inf'), nodes_expanded, max_frontier)

def depth_limited_search(problem: Problem, limit: int) -> SearchResult:
    """Depth-Limited Search (Lecture 4). Prunes paths exceeding depth limit."""
    frontier = [SearchNode(problem.initial_state)]
    nodes_expanded = 0
    max_frontier = 1
    cutoff = False

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        node = frontier.pop()

        if problem.is_goal(node.state):
            return SearchResult(
                'DLS', True, [n.state for n in node.path()],
                node.solution(), node.path_cost, nodes_expanded, max_frontier
            )

        if node.depth < limit:
            nodes_expanded += 1
            # Level 2 cycle check: prevent duplicate states along active path
            path_states = {n.state for n in node.path()}
            for action in reversed(problem.actions(node.state)):
                child_state = problem.result(node.state, action)
                if child_state not in path_states:
                    cost = node.path_cost + problem.step_cost(node.state, action, child_state)
                    frontier.append(SearchNode(child_state, node, action, cost))
        else:
            cutoff = True

    return SearchResult('DLS', False, [], [], float('inf'), nodes_expanded, max_frontier)

def iterative_deepening_search(problem: Problem, max_depth: int = 50) -> SearchResult:
    """Iterative Deepening Search (Lecture 4). The sweet spot combining BFS optimality with DFS space."""
    total_expanded = 0
    max_frontier = 1

    for depth in range(max_depth + 1):
        res = depth_limited_search(problem, depth)
        total_expanded += res.nodes_expanded
        max_frontier = max(max_frontier, res.max_frontier_size)
        if res.success:
            return SearchResult(
                'IDS', True, res.path, res.actions,
                res.cost, total_expanded, max_frontier
            )

    return SearchResult('IDS', False, [], [], float('inf'), total_expanded, max_frontier)

def uniform_cost_search(problem: Problem) -> SearchResult:
    node = SearchNode(problem.initial_state)
    frontier: List[PriorityItem] = []
    count = 0
    heapq.heappush(frontier, PriorityItem(node.path_cost, count, node))
    best_cost: Dict[Any, float] = {node.state: node.path_cost}
    nodes_expanded = 0
    max_frontier = 1

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        item = heapq.heappop(frontier)
        node = item.item

        if problem.is_goal(node.state):
            return SearchResult(
                'UCS', True, [n.state for n in node.path()],
                node.solution(), node.path_cost, nodes_expanded, max_frontier
            )

        if node.path_cost > best_cost[node.state]:
            continue

        nodes_expanded += 1

        for action in problem.actions(node.state):
            child_state = problem.result(node.state, action)
            child_cost = node.path_cost + problem.step_cost(node.state, action, child_state)

            if child_state not in best_cost or child_cost < best_cost[child_state]:
                best_cost[child_state] = child_cost
                child_node = SearchNode(child_state, node, action, child_cost)
                count += 1
                heapq.heappush(frontier, PriorityItem(child_cost, count, child_node))

    return SearchResult('UCS', False, [], [], float('inf'), nodes_expanded, max_frontier)

def a_star_search(problem: Problem, heuristic: Optional[Callable[[Any], float]] = None) -> SearchResult:
    h = heuristic or problem.heuristic
    node = SearchNode(problem.initial_state)
    f_cost = node.path_cost + h(node.state)
    frontier: List[PriorityItem] = []
    count = 0
    heapq.heappush(frontier, PriorityItem(f_cost, count, node))
    best_g: Dict[Any, float] = {node.state: node.path_cost}
    nodes_expanded = 0
    max_frontier = 1

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        item = heapq.heappop(frontier)
        node = item.item

        if problem.is_goal(node.state):
            return SearchResult(
                'A*', True, [n.state for n in node.path()],
                node.solution(), node.path_cost, nodes_expanded, max_frontier
            )

        if node.path_cost > best_g[node.state]:
            continue

        nodes_expanded += 1

        for action in problem.actions(node.state):
            child_state = problem.result(node.state, action)
            child_g = node.path_cost + problem.step_cost(node.state, action, child_state)

            if child_state not in best_g or child_g < best_g[child_state]:
                best_g[child_state] = child_g
                child_node = SearchNode(child_state, node, action, child_g)
                child_f = child_g + h(child_state)
                count += 1
                heapq.heappush(frontier, PriorityItem(child_f, count, child_node))

    return SearchResult('A*', False, [], [], float('inf'), nodes_expanded, max_frontier)

class GraphSearchProblem(Problem):
    def __init__(self, initial: str, goal: str, graph: Dict[str, Dict[str, float]], heuristics: Optional[Dict[str, float]] = None):
        super().__init__(initial, goal)
        self.graph = graph
        self.heuristics = heuristics or {}

    def actions(self, state: str) -> List[str]:
        return list(self.graph.get(state, {}).keys())

    def result(self, state: str, action: str) -> str:
        return action

    def step_cost(self, state: str, action: str, next_state: str) -> float:
        return self.graph[state][next_state]

    def heuristic(self, state: str) -> float:
        return self.heuristics.get(state, 0.0)
