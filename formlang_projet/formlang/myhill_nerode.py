"""Classes de Myhill-Nerode (approx. sur suffixes témoins). À COMPLÉTER.
-> Jour 5 (E5.3)."""
from __future__ import annotations


def nerode_classes(accepts, words, suffixes):
    # Dictionnaire pour regrouper les mots par signature
    # Clé : signature (tuple de booléens) -> Valeur : liste de mots
    groups = {}
    
    for w in words:
        # Calcul de la signature pour le mot w sur tous les suffixes fournis
        sig = tuple(accepts(w + s) for s in suffixes)
        
        # Si c'est la première fois qu'on voit cette signature, on crée une liste vide
        if sig not in groups:
            groups[sig] = []
            
        # On ajoute le mot au groupe correspondant
        groups[sig].append(w)
        
    # La fonction doit retourner les classes d'équivalence.
    # On renvoie la liste de toutes les listes de mots regroupés.
    return list(groups.values())

def equivalent(u, v, accepts, suffixes) -> bool:
    # FOURNI
    return all(accepts(u + s) == accepts(v + s) for s in suffixes)
