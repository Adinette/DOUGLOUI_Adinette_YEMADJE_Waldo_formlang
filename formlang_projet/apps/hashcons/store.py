"""Hash-consing : partage de structure (DAG) sur formlang.tree.Term. À COMPLÉTER.
-> TP arbres (E4 intern/partage, E5 round-trip, Q5 compression).

Règle « gate » : INSTANCIER formlang.tree.Term, ne pas le réécrire."""
from __future__ import annotations
from formlang.tree import Term

NodeId = int


class CompactStore:
    def __init__(self):
        self._nodes: list[tuple] = []          # id -> (symbol, label, kids_ids)
        self._table: dict[tuple, NodeId] = {}   # clé canonique -> id
        self._total = 0

    def intern(self, t: Term) -> NodeId:
        # 1. Interner récursivement chaque enfant -> kids_ids (tuple)
        kids_ids = tuple(self.intern(child) for child in t.children)
        
        # 2. Incrémenter le nombre total de nœuds vus
        self._total += 1
        
        # 3. Clé canonique = (t.symbol, t.label, kids_ids)
        key = (t.symbol, t.label, kids_ids)
        
        # 4. Si déjà dans self._table -> renvoyer l'id existant
        if key in self._table:
            return self._table[key]
            
        # Sinon créer un nouvel id (= len(self._nodes)), l'enregistrer
        new_id = len(self._nodes)
        self._nodes.append(key)
        self._table[key] = new_id
        return new_id

    def get(self, nid: NodeId) -> Term:
        # Récupération de la clé canonique depuis l'id
        symbol, label, kids_ids = self._nodes[nid]
        
        # Reconstruction récursive des sous-arbres enfants
        children = tuple(self.get(kid_id) for kid_id in kids_ids)
        
        # Reconstruction du Term d'origine (Round-trip exact)
        return Term(symbol=symbol, children=children, label=label)

    def total_nodes(self) -> int:
        return self._total

    def unique_nodes(self) -> int:
        return len(self._nodes)

    def compression(self) -> float:
        if self._total == 0:
            return 0.0
        # Formule demandée : 1 - uniques / total
        return 1.0 - (self.unique_nodes() / self._total)