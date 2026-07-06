"""Automate morphologique (instancie formlang.tree). À COMPLÉTER : règles Delta.
-> Jour 3 (E3.2). Constructeurs et classify FOURNIS."""
from formlang.tree import Term, TreeAutomaton


# ----- constructeurs FOURNIS ------------------------------------------------
def prefix(s): return Term("prefix", label=s)
def root(s):   return Term("root",   label=s)
def suffix(s): return Term("suffix", label=s)
def nil():     return Term("nil")
def prefixes(h, t): return Term("prefixes", (h, t))
def suffixes(h, t): return Term("suffixes", (h, t))
def rest(r, s):     return Term("rest", (r, s))
def word(p, r):     return Term("word", (p, r))


def build_word(pres, root_str, sufs) -> Term:
    pc = nil()
    for p in reversed(pres):
        pc = prefixes(prefix(p), pc)
    sc = nil()
    for s in reversed(sufs):
        sc = suffixes(suffix(s), sc)
    return word(pc, rest(root(root_str), sc))


# ----- à compléter ----------------------------------------------------------
# ==============================================================================
# ----- À COMPLÉTER : AUTOMATE MORPHOLOGIQUE (E3.2) -----------------------------
# ==============================================================================
def morpho_automaton() -> TreeAutomaton:
    A = TreeAutomaton(final_states={"WORD"})
    
    # 1. Règles pour les feuilles de base
    A.add_rule("prefix", (), "PREF")
    A.add_rule("root", (), "ROOT")
    A.add_rule("suffix", (), "SUF")
    A.add_rule("nil", (), "NIL")
    
    # 2. Règles pour construire la liste des préfixes
    A.add_rule("prefixes", ("PREF", "NIL"), "LIST_P")
    A.add_rule("prefixes", ("PREF", "LIST_P"), "LIST_P")
    
    # 3. Règles pour construire la liste des suffixes
    A.add_rule("suffixes", ("SUF", "NIL"), "LIST_S")
    A.add_rule("suffixes", ("SUF", "LIST_S"), "LIST_S")
    
    # 4. Règles pour combiner la racine et les suffixes (rest)
    A.add_rule("rest", ("ROOT", "NIL"), "REST")
    A.add_rule("rest", ("ROOT", "LIST_S"), "REST")
    
    # 5. Règles finales pour construire un mot (word)
    A.add_rule("word", ("NIL", "REST"), "WORD")
    A.add_rule("word", ("LIST_P", "REST"), "WORD")
    
    return A


# ==============================================================================
# ----- À COMPLÉTER : ATTACK DECOMPOSER SHIELD (E3.3) -------------------------
# ==============================================================================
def _seq(x, y):
    if x == DANGER or y == DANGER:
        return DANGER
    # Si ROLE rencontre OVR (ou inversement), privilèges cumulés -> DANGER
    if (x == ROLE and y == OVR) or (x == OVR and y == ROLE):
        return DANGER
    # Sinon, on prend le maximum selon l'ordre de sévérité défini
    return _BY_SEV[max(_SEV[x], _SEV[y])]


def shield_automaton() -> TreeAutomaton:
    A = TreeAutomaton(final_states={DANGER})
    
    # 1. Règles pour les feuilles atomiques
    A.add_rule("txt", (), SAFE)
    A.add_rule("enc", (), SAFE)
    A.add_rule("ovr", (), OVR)
    A.add_rule("role", (), ROLE)
    
    # 2. Règle binaire seq : croisement de tous les états possibles via _seq
    for x in _ALL:
        for y in _ALL:
            A.add_rule("seq", (x, y), _seq(x, y))
            
    # 3. Règles unaires pour frame et sys
    for x in _ALL:
        # frame protège ou transmet l'état actuel
        A.add_rule("frame", (x,), x)
        
        # sys bloque s'il contient autre chose que du pur SAFE
        if x == SAFE:
            A.add_rule("sys", (x,), SAFE)
        else:
            A.add_rule("sys", (x,), DANGER)
            
    return A


# ==============================================================================
# ----- À COMPLÉTER : BONUS COMPTAGE ENCODAGES & PRODUIT (E3.6) -----------------
# ==============================================================================
def enc_automaton() -> TreeAutomaton:
    # Automate qui compte le nombre d'encodages (feuilles 'enc') rencontrés (plafond à 2)
    # Les états cibles possibles sont 0, 1, 2. L'état final attendu est 2.
    A = TreeAutomaton(final_states={2})
    
    # Feuilles : 'enc' vaut 1, les autres valent 0
    A.add_rule("txt", (), 0)
    A.add_rule("ovr", (), 0)
    A.add_rule("role", (), 0)
    A.add_rule("enc", (), 1)
    
    # Règle binaire seq : somme des encodages plafonnée à 2
    for x in (0, 1, 2):
        for y in (0, 1, 2):
            A.add_rule("seq", (x, y), min(2, x + y))
            
    # Règles unaires : frame et sys transmettent simplement le compteur
    for x in (0, 1, 2):
        A.add_rule("frame", (x,), x)
        A.add_rule("sys", (x,), x)
        
    return A


def dangerous_and_double_encoded() -> TreeAutomaton:
    from formlang.tree import product
    return product(shield_automaton(), enc_automaton())

# ----- FOURNI ---------------------------------------------------------------
def _contains(t: Term, sym: str) -> bool:
    if t.symbol == sym:
        return True
    return any(_contains(c, sym) for c in t.children)


def classify(A: TreeAutomaton, t: Term) -> str:
    if not A.accepts(t):
        return "INVALID"
    p, s = _contains(t, "prefix"), _contains(t, "suffix")
    if p and s:
        return "CIRCUMFIXED"
    if s:
        return "SUFFIXED"
    if p:
        return "PREFIXED"
    return "BARE"
