# Unit 05: Knowledge Representation & Logical Inference
# COMP111 - Artificial Intelligence

from typing import Set, FrozenSet, List, Dict, Tuple

class PropositionalResolution:
    """
    Resolution Theorem Proving for Propositional Logic in CNF.
    Each clause is represented as a frozenset of literals (e.g. frozenset({'A', '~B'})).
    """
    @staticmethod
    def negate_literal(lit: str) -> str:
        return lit[1:] if lit.startswith('~') else '~' + lit

    @classmethod
    def resolve(cls, ci: FrozenSet[str], cj: FrozenSet[str]) -> List[FrozenSet[str]]:
        resolvents = []
        for lit in ci:
            complement = cls.negate_literal(lit)
            if complement in cj:
                new_clause = (ci - {lit}) | (cj - {complement})
                resolvents.append(frozenset(new_clause))
        return resolvents

    @classmethod
    def pl_resolution(cls, kb_clauses: Set[FrozenSet[str]], alpha_clauses: Set[FrozenSet[str]]) -> bool:
        """
        Proves KB |= alpha by refutation: checking unsatisfiability of KB & ~alpha.
        Returns True if KB entails alpha, False otherwise.
        """
        clauses = set(kb_clauses) | set(alpha_clauses)
        new = set()

        while True:
            clause_list = list(clauses)
            n = len(clause_list)
            for i in range(n):
                for j in range(i + 1, n):
                    resolvents = cls.resolve(clause_list[i], clause_list[j])
                    for resolvent in resolvents:
                        if len(resolvent) == 0: # Empty clause derived -> contradiction!
                            return True
                        new.add(resolvent)

            if new.issubset(clauses):
                return False
            clauses |= new

class HornClauseKB:
    """
    Forward Chaining inference for definite / Horn clauses.
    Clause format: premises -> conclusion.
    """
    def __init__(self, clauses: List[Tuple[List[str], str]]):
        self.clauses = clauses

    def pl_fc_entails(self, facts: Set[str], query: str) -> bool:
        if query in facts:
            return True

        count = {i: len(premises) for i, (premises, _) in enumerate(self.clauses)}
        inferred = {f: True for f in facts}
        agenda = list(facts)

        while agenda:
            p = agenda.pop()
            if p == query:
                return True
            for i, (premises, head) in enumerate(self.clauses):
                if p in premises:
                    count[i] -= 1
                    if count[i] == 0:
                        if not inferred.get(head, False):
                            inferred[head] = True
                            agenda.append(head)
        return inferred.get(query, False)
