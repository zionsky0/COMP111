# Unit 04: Constraint Satisfaction Problems (CSP)
# COMP111 - Artificial Intelligence

from collections import deque
from typing import Dict, List, Set, Tuple, Any, Optional, Callable

class CSP:
    def __init__(self, variables: List[Any], domains: Dict[Any, List[Any]], neighbors: Dict[Any, Set[Any]], constraints: Callable[[Any, Any, Any, Any], bool]):
        self.variables = variables
        self.domains = {v: list(domains[v]) for v in variables}
        self.neighbors = neighbors
        self.constraints = constraints # constraints(var1, val1, var2, val2) -> bool

    def is_consistent(self, var: Any, val: Any, assignment: Dict[Any, Any]) -> bool:
        for neighbor in self.neighbors.get(var, []):
            if neighbor in assignment:
                if not self.constraints(var, val, neighbor, assignment[neighbor]):
                    return False
        return True

def ac3(csp: CSP, queue: Optional[List[Tuple[Any, Any]]] = None) -> bool:
    """Arc Consistency Algorithm #3."""
    if queue is None:
        arcs = deque([(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors.get(Xi, [])])
    else:
        arcs = deque(queue)

    while arcs:
        Xi, Xj = arcs.popleft()
        if revise(csp, Xi, Xj):
            if len(csp.domains[Xi]) == 0:
                return False
            for Xk in csp.neighbors.get(Xi, []):
                if Xk != Xj:
                    arcs.append((Xk, Xi))
    return True

def revise(csp: CSP, Xi: Any, Xj: Any) -> bool:
    revised = False
    for x in list(csp.domains[Xi]):
        if not any(csp.constraints(Xi, x, Xj, y) for y in csp.domains[Xj]):
            csp.domains[Xi].remove(x)
            revised = True
    return revised

def backtracking_search(csp: CSP, mrv: bool = True, lcv: bool = True) -> Optional[Dict[Any, Any]]:
    """Backtracking search with MRV and LCV heuristics."""
    return _backtrack({}, csp, mrv, lcv)

def _select_unassigned_variable(assignment: Dict[Any, Any], csp: CSP, use_mrv: bool) -> Any:
    unassigned = [v for v in csp.variables if v not in assignment]
    if not use_mrv:
        return unassigned[0]
    # MRV: Minimum Remaining Values, tie-break by highest degree
    return min(unassigned, key=lambda var: (len(csp.domains[var]), -len(csp.neighbors.get(var, []))))

def _order_domain_values(var: Any, assignment: Dict[Any, Any], csp: CSP, use_lcv: bool) -> List[Any]:
    if not use_lcv:
        return csp.domains[var]
    # LCV: Count how many choices are ruled out for unassigned neighbors
    def count_conflicts(val):
        conflicts = 0
        for n in csp.neighbors.get(var, []):
            if n not in assignment:
                for n_val in csp.domains[n]:
                    if not csp.constraints(var, val, n, n_val):
                        conflicts += 1
        return conflicts
    return sorted(csp.domains[var], key=count_conflicts)

def _backtrack(assignment: Dict[Any, Any], csp: CSP, mrv: bool, lcv: bool) -> Optional[Dict[Any, Any]]:
    if len(assignment) == len(csp.variables):
        return assignment

    var = _select_unassigned_variable(assignment, csp, mrv)
    for val in _order_domain_values(var, assignment, csp, lcv):
        if csp.is_consistent(var, val, assignment):
            assignment[var] = val
            result = _backtrack(assignment, csp, mrv, lcv)
            if result is not None:
                return result
            del assignment[var]
    return None

def create_australia_map_csp() -> CSP:
    """Classic Australia Map-Coloring CSP."""
    variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
    domains = {v: ['Red', 'Green', 'Blue'] for v in variables}
    neighbors = {
        'WA': {'NT', 'SA'},
        'NT': {'WA', 'SA', 'Q'},
        'SA': {'WA', 'NT', 'Q', 'NSW', 'V'},
        'Q': {'NT', 'SA', 'NSW'},
        'NSW': {'Q', 'SA', 'V'},
        'V': {'SA', 'NSW'},
        'T': set()
    }
    def diff_constraint(var1, val1, var2, val2):
        return val1 != val2

    return CSP(variables, domains, neighbors, diff_constraint)
