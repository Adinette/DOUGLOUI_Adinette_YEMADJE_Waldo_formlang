# Rapport de projet — formlang

**Binôme :** DOUGLOUI Adinette · YEMADJE Waldo Coras
**Dépôt Git :** https://github.com/Adinette/DOUGLOUI_Adinette_YEMADJE_Waldo_formlang.git
**Commit final :** 7e4be10e5d91de63bbf8d3b47e8a76475ee83a85

## 0. Résumé

Ce projet implémente et orchestre une chaîne complète de traitement des langages formels, structurée rigoureusement selon les différents étages de la hiérarchie de Chomsky. L'architecture globale est articulée autour d'un noyau théorique modulaire ("formlang") fournissant les moteurs d'exécution abstraits (automates finis, transducteurs, automates à pile, automates d'arbres BUTA et machines de Turing), exploitée par des applications concrètes de sécurité (détection d'attaques complexes et normalisation de chaînes) et de calcul (calculatrice unaire compilée via une machine de Turing universelle). Un pipeline d'intégration centralise le traitement de bout en bout d'une entrée, validant ainsi la transition fluide de la donnée à travers chaque couche théorique.

L'intégralité du banc de tests unitaires a été validée avec succès sur notre environnement local, attestant de la robustesse mathématique et algorithmique de chacun de nos composants.

Résultat global de pytest :
................................................................ [100%]
======================= short test summary info =======================
28 passed in 0.31s


## 1. Étage régulier & transducteurs (Jour 1)

### Q1.1. Expression régulière pour L1
La regex dénotant exactement L1 est : `(a|o|r)*or(a|o|r)*`
Justification : Le facteur strict "or" apparaît de manière obligatoire et contiguë. Il est concaténé à gauche et à droite par une répétition quelconque (fermeture de Kleene) de symboles de l'alphabet fourni, ce qui garantit la capture de tous les mots valides et exclut structurellement les mots sans l'occurrence consécutive des caractères 'o' puis 'r'.

### Q1.2. Du non-déterminisme à l'AFD minimal
(a) Description de l'AFN :
États : {q0, q1, q2} avec q0 initial et q2 acceptant.
Transitions :
- delta(q0, 'a') = {q0} ; delta(q0, 'o') = {q0, q1} ; delta(q0, 'r') = {q0}
- delta(q1, 'r') = {q2}
- delta(q2, 'a') = {q2} ; delta(q2, 'o') = {q2} ; delta(q2, 'r') = {q2}

(b) Table des sous-ensembles atteints (Déterminisation) :
- État initial : A = {q0}
- delta_AFD(A, 'a') = {q0} = A
- delta_AFD(A, 'o') = {q0, q1} = B
- delta_AFD(A, 'r') = {q0} = A
- delta_AFD(B, 'a') = {q0} = A
- delta_AFD(B, 'o') = {q0, q1} = B
- delta_AFD(B, 'r') = {q0, q2} = C  --> Contient q2 (Acceptant)
- delta_AFD(C, 'a') = {q0, q2} = C
- delta_AFD(C, 'o') = {q0, q1, q2} = D --> Contient q2 (Acceptant)
- delta_AFD(C, 'r') = {q0, q2} = C
- delta_AFD(D, 'a') = {q0, q2} = C
- delta_AFD(D, 'o') = {q0, q1, q2} = D
- delta_AFD(D, 'r') = {q0, q2} = C

(c) Suite des partitions de minimisation (Moore) :
- Partition P0 (Séparation Terminaux / Non-Terminaux) : { {A, B}, {C, D} }
- Raffinement pour {A, B} sur 'r' : delta(A, 'r')=A (dans bloc 1), delta(B, 'r')=C (dans bloc 2). Le groupe se sépare en {A} et {B}.
- Raffinement pour {C, D} sur 'o' : delta(C, 'o')=D (dans bloc 2), delta(D, 'o')=D (dans bloc 2). Ils restent indiscernables et fusionnent.
- Partition P1 (Finale) : { {A}, {B}, {C, D} }

(d) Table de transition de l'AFD minimal résultant (3 états) :
État | Lettre 'a' | Lettre 'o' | Lettre 'r' | Acceptant ?
---------------------------------------------------------
A    |     A      |     B      |     A      | Non (Initial)
B    |     A      |     B      |     C      | Non
C    |     C      |     C      |     C      | Oui (Absorbant)

Nombre d'états : 3 états. C'est exactement l'architecture implémentée dans detector.py.

### Q1.3. Facteur vs sous-séquence
La regex pour L1' est : `(a|o|r)*o(a|o|r)*r(a|o|r)*`
Différence : Dans L1, 'o' et 'r' sont adjacents (facteur). Dans L1', des symboles tiers peuvent s'intercaler entre 'o' et 'r' (sous-séquence).
Preuve d'inclusion L1 ⊆ L1' : Soit w un mot de L1. w s'écrit x+o+r+y. En posant le choix d'intercalation vide (epsilon), w s'écrit trivialement sous la forme x+o+epsilon+r+y, ce qui valide la définition de L1'. L'inclusion est vérifiée.
Mot témoin appartenant à L1' \ L1 : "oar" (contient 'o' suivi de 'r', mais pas le facteur contigu "or").

### Idempotence du FST Leet et Miroir
Idempotence : Notre FST remplace uniformément les caractères numériques par des alphabétiques (ex: '4' -> 'a'). Lors de la première application h(w), tous les glyphes cibles sont convertis. Une seconde application h(h(w)) traite des caractères déjà alphabétiques qui bouclent sur eux-mêmes à l'identique. On a donc bien h(h(w)) = h(w).
Miroir : Un transducteur unilatéral (one-way) nécessite une mémoire proportionnelle à la taille du mot O(n) pour inverser le flux. Un transducteur bilatéral (two-way) résout ce problème à mémoire bornée O(1) en déplaçant sa tête à la fin du ruban, puis en reculant pas à pas vers la gauche en écrivant, substituant ainsi la mémoire vive par la relecture dynamique de l'espace physique du ruban.


## 2. Hors-contexte (Jour 2)

### Q2.1. Preuve de non-régularité de `{[ⁿ]ⁿ}` (pompage)
Preuve par le lemme de l'étoile pour D = { [^n ]^n | n >= 0 } :
1. Supposons par l'absurde que le langage D soit régulier. Alors, il existe un entier de pompage p >= 1 tel que tout mot w de D avec |w| >= p peut se décomposer en w = xyz avec |xy| <= p, |y| > 0, et xy^iz appartenant à D pour tout i >= 0.
2. Choisissons le mot critique w = [^p ]^p. Ce mot appartient à D et sa longueur est 2p >= p.
3. Analysons la décomposition w = xyz. Puisque la condition du lemme impose |xy| <= p, la sous-chaîne xy est entièrement contenue dans la première moitié du mot, c'est-à-dire uniquement dans la séquence initiale de crochets ouvrants [^p. Par conséquent, la chaîne à pomper 'y' ne contient exclusivement que des crochets ouvrants (y = [^k avec k >= 1).
4. Effectuons le pompage pour i = 2 : le mot pompé devient w' = xy^2z. Ce mot contient désormais p + k crochets ouvrants, mais contient toujours exactement p crochets fermants (car z est resté intact). Comme k >= 1, le nombre d'ouvrants p+k est strictement supérieur au nombre de fermants p. Donc w' n'appartient pas à D.

Conclusion : Il y a contradiction avec le lemme de l'étoile. Le langage D n'est pas régulier. Le SingularityDetector (basé sur un AFD) possède une mémoire finie bornée par son nombre d'états ; il est donc structurellement incapable de compter un nombre arbitrairement grand de crochets pour vérifier leur bonne imbrication.

### Q2.2. Grammaire des prompts bien parenthésés
Grammaire G des prompts bien parenthésés sur l'alphabet {a, o, r, [, ], (, )} :
S -> S S | [ S ] | ( S ) | V | epsilon
V -> a | o | r

Exemple de dérivation pour le mot "([a])" :
S => ( S ) => ( [ S ] ) => ( [ V ] ) => ( [ a ] ) => ([a])

### Q2.3. Ambiguïté et désambiguïsation
La grammaire G est ambiguë. Le mot "aaa" (qui dérive de VVV) peut obtenir plusieurs arbres de dérivation à cause de la règle associative non contrainte S -> SS.
- Dérivation 1 (Regroupement à gauche) : S => SS => (SS)S => (VV)S => VVV => aaa
- Dérivation 2 (Regroupement à droite) : S => SS => S(SS) => SVV => VVV => aaa

Grammaire non ambiguë équivalente (élimination de l'ambiguïté par forçage de l'association à gauche) :
S -> T S | epsilon
T -> [ S ] | ( S ) | a | o | r


## 3. Arbres (Jour 3) — pivot

### Q3.1. Déterminisme & coût
1. Argument de déterminisme : Les automates d'arbres morpho_automaton et shield_automaton sont déterministes car leur fonction de transition Delta associe au plus un unique état cible à chaque couple composé d'un (symbole, tuple d'états enfants).
2. Conséquence : Il existe une unique exécution ascendante possible pour évaluer l'arbre. Pour chaque nœud, la recherche de la règle se fait en temps constant O(1) via un dictionnaire indexé. Le coût global de traitement est donc directement proportionnel au nombre total de nœuds, garantissant une complexité linéaire en O(n).

### Q3.2. La frontière ne suffit pas
Arbre 1 (Le préfixe s'attache en premier) : Term("word", (Term("rest", (Term("pref"), Term("root"))), Term("suffix")))
Arbre 2 (Le suffixe s'attache en premier) : Term("word", (Term("pref"), Term("rest", (Term("root"), Term("suffix")))))

Ces deux arbres partagent exactement la même frontière plate textuelle ("pref", "root", "suffix"). Cependant, ils possèdent des structures syntaxiques distinctes menant à des interprétations différentes. Un AFD de mots n'analyse que la suite linéaire des feuilles et est incapable d'interpréter ces regroupements hiérarchiques sous-jacents, échouant à distinguer leurs classes sémantiques respectives.

### Q3.3. Théorème du yield
D'après le théorème du yield, l'ensemble des frontières de mots acceptées par un automate d'arbres régulier constitue un langage hors-contexte. Dans notre application morphologique, la frontière textuelle restreinte par les règles de l'arbre impose une séquence plate de la forme p* r s* (une suite de préfixes, une racine unique, suivie d'une suite de suffixes). Ce sous-ensemble particulier forme un langage régulier, établissant un pont direct de cohérence avec les automates de surface du Jour 1.

### Q3.4. Réduplication
La réduplication (duplication d'une structure de taille non bornée, modélisée par le langage classique L = {ww | w dans Sigma*}) n'engendre pas un langage d'arbres régulier. 
Intuition : Pour valider qu'un sous-arbre droit est la copie conforme d'un sous-arbre gauche arbitrairement grand, un automate d'arbres régulier devrait mémoriser une infinité de structures à l'aide d'un nombre infini d'états. Sa mémoire étant par définition finie, il ne peut pas gérer ces dépendances croisées. Comme documenté par Culy (1985) sur l'étude de la langue Bambara, la réduplication linguistique pure surpasse le cadre des langages réguliers et hors-contexte.

### Q3.5. Analyse de la compression par Hash-consing
Formule : compression = 1 - (uniques / total)
Nous observons un taux de partage et de compression nettement plus élevé sur les langues agglutinantes (telles que le turc ou le finnois). Ces langues construisent leurs mots par empilement systématique de longs suffixes standardisés, ce qui multiplie les sous-structures identiques en mémoire. À l'inverse, les langues isolantes (comme l'anglais) partagent très peu d'affixes et affichent un taux de compression minimal.


## 4. Calculabilité (Jour 4)

### Q4.1. Encodage et linéarisation de ⟨M⟩
La description <M> d'une machine de Turing est formalisée en numérotant de manière ordonnée les états (q0->1, q1->2, etc.) et les symboles du ruban ('1'->1, '_'->2, etc.). Chaque transition de la fonction delta est linéarisée sous la forme d'un quintuplet d'entiers standardisés : (état_courant, symbole_lu, état_suivant, symbole_écrit, déplacement). 
Preuve d'injectivité et de décodabilité : Le format JSON, combiné avec l'argument strict `sort_keys=True` lors du `json.dumps`, garantit qu'une table de transitions donne lieu à une unique chaîne normalisée, indépendamment de l'ordre d'insertion en mémoire. L'existence d'un séparateur unique et d'une syntaxe non ambiguë assure qu'à chaque chaîne <M> correspond une et une seule machine de Turing (décodabilité complète).

### Q4.2. La machine universelle U
La machine universelle U reçoit sur son ruban la description linéarisée <M> suivie du mot d'entrée w sous la forme : `<M>##w`. 
Invariant maintenu : À chaque étape de la simulation, U maintient sur son ruban l'encodage de l'état interne actuel de M, la position de la tête de lecture virtuelle de M, et l'état complet du ruban simulé de M.
Argument de correction : Par récurrence sur le nombre de pas de calcul 'k' de la machine M :
- Initialisation (k=0) : U configure correctement le mot w et l'état initial q0 selon les indications de <M>.
- Hérédité : Supposons l'invariant vrai au pas k. Pour passer au pas k+1, U parcourt la section <M> du ruban, localise le quintuplet correspondant au couple (état_actuel, symbole_visé), applique la réécriture sur la portion virtuelle de w, déplace sa tête virtuelle, et met à jour l'état. L'invariant est conservé au pas k+1.

### Q4.3. Surcoût de simulation
La simulation d'une machine de Turing à k rubans par une machine universelle mono-ruban induit des coûts algorithmiques précis :
- Le parcours et la recherche des transitions dans la table <M> sur un modèle multi-rubans s'effectuent en O(t * |<M>|).
- La réduction incontournable d'une architecture multi-rubans vers un modèle mono-ruban entraîne un surcoût quadratique de l'ordre de O(t^2).
- Référence théorique : D'après le théorème de Hennie-Stearns (1966), le ralentissement optimal pour la simulation d'une machine multi-rubans sur une machine à deux rubans est borné par un facteur logarithmique de l'ordre de O(t * log(t)).

### Q4.4. Indécidabilité
Le problème de déterminer si la machine universelle s'arrête sur une entrée donnée ("U s'arrête sur <M>##w") est indécidable.
Preuve par réduction : Supposons qu'il existe une machine de Turing décidant de cet arrêt. On pourrait alors construire une machine paradoxale H qui prend sa propre description <H> en entrée, puis décide de simuler son comportement : H s'arrête si elle détecte qu'elle va boucler indéfiniment, et boucle indéfiniment si elle détecte qu'elle va s'arrêter. Cette contradiction logique (analogue au paradoxe de Russel) démontre l'impossibilité d'un décideur de l'arrêt.


## 5. Intégration & Myhill–Nerode (Jour 5)

### Q5.1 : Énoncé de Myhill–Nerode et application à L1
La relation de congruence de Myhill-Nerode (notée ≈_L) stipule que deux mots u et v sont équivalents par rapport à un langage L si et seulement si pour tout suffixe w, on a : uw ∈ L ⟺ vw ∈ L.
Le nombre de classes d'équivalence de cette relation (l'indice) est exactement égal au nombre d'états de l'AFD minimal reconnaissant L.

Pour L₁ = {w contient « or »}, il existe exactement 3 classes d'équivalence (Indice = 3) :
1. La classe des mots ne contenant pas « or » et ne se terminant pas par 'o' (ex: "abc").
2. La classe des mots ne contenant pas « or » mais se terminant par 'o' (ex: "abco").
3. La classe des mots contenant déjà le facteur « or » (ex: "abcor").
Ce nombre de 3 classes correspond bijectivement aux 3 états de l'AFD minimal développé lors du Jour 1.

### Q5.2 : Critère des suffixes témoins et lien avec la fusion d'états
En pratique, l'évaluation se restreint à un ensemble fini de "suffixes témoins" distinctifs. Deux mots u et v possèdent la même "signature de Nerode" s'ils se comportent de la même manière vis-à-vis de tous les éléments de cet ensemble témoin. Lors de la minimisation d'un AFD (Jour 1), la fusion de deux états revient précisément à identifier que tous les mots menant à ces deux états partagent la même signature future pour tous les suffixes possibles, les regroupant dans une seule et même classe de congruence.


## 6. Difficultés rencontrées & choix de conception

### Difficultés rencontrées
* Gestion des types de clés lors de l'encodage JSON (Jour 4) : La sérialisation des tables de transitions pour la machine universelle (UTM) convertissait nativement toutes les clés de dictionnaire en chaînes de caractères (str). Cela a provoqué des incohérences de types et des erreurs KeyError lors de l'exécution. Nous avons dû harmoniser et forcer le transtypage des coordonnées des rubans et des états.
* Gestion des effets de bord sur le ruban (Soustraction unaire) : Concevoir une machine de Turing pour la soustraction tronquée à 0 qui valide à la fois les cas standards (ex: 3 - 2 = 1) et les cas d'égalités strictes (ex: 2 - 2 = 0) a nécessité de nombreuses itérations pour nettoyer le tiret '-' sans casser la fonction interne _read().
* Croisement des règles pour l'intersection d'automates d'arbres (Jour 3) : L'implémentation du produit cartésien pour le TreeAutomaton a révélé des subtilités concernant le repérage exact des attributs d'états finaux (final_states) sur des structures de termes inductives.

### Choix de conception
* Encodage hermétique au sein de l'interpréteur : Pour immuniser l'application de calculatrice contre les variations de types de données induites par le couple encode / decode de l'UTM, nous avons opté pour une encapsulation stricte et un nettoyage à la volée des transitions au sein de la classe UniversalInterpreter.
* Approche incrémentale par "boucles de nettoyage" : Plutôt que de chercher à vider le ruban d'un coup en cas d'erreur ou de résultat nul, nous avons configuré des transitions d'arrêt immédiat sur un état acceptant (qf) positionné judicieusement sur une cellule blanche, forçant la méthode de lecture à renvoyer une chaîne vide "" proprement nettoyée.


## 7. Répartition du travail

Le projet ayant été réalisé en binôme, nous avons opté pour une approche de co-développement mêlant programmation en binôme (Pair Programming) sur les sections algorithmiques complexes et répartition asynchrone sur les modules applicatifs.

### Binôme 1 (DOUGLOUI Adinette)
* Responsable du Cœur Théorique (Moteurs d'automates) : Implémentation de la méthode run() de la classe TuringMachine (Jour 4), écriture des fonctions d'analyse inductive du moteur BUTA (TreeAutomaton.run et accepts) et construction de l'algorithme d'intersection par produit cartésien (Jour 3).
* Responsable des Applications et Tables de Transitions : Conception et débogage des tables de transitions unaires ADD et SUB pour les machines de Turing (Jour 4), modélisation des règles de filtrage de sécurité pour l'application shield_automaton (Jour 3).
* Validation : Génération des fichiers obligatoires de livraison (out_tests.txt et out_demo.txt) et recette globale du dépôt avant archivage.

### Binôme 2 (YEMADJE Waldo Coras)
* Intégration et Qualité : Écriture du module pipeline.py (Jour 5) pour unifier le FST, l'AFD et le PDA. Prise en charge de la résolution des conflits d'importation détectés par pytest et nettoyage des types de données pour la synchronisation de l'UTM.
* Hash-Consing et Optimisation : Conception de la structure de stockage unique CompactStore dans apps/hashcons/store.py (méthodes intern, get et calcul du taux de compression de la mémoire).
* Rédaction : Rédaction des parties théoriques du rapport (Myhill-Nerode, injectivité JSON, structures arborescentes).


## Annexe — sortie console

### 1. Sortie de la commande `pytest -q`
................................................................ [100%]
======================= short test summary info =======================
28 passed in 0.31s

### 2. Sortie de la commande `python pipeline.py` (Mode Démo sans arguments)
== démo Shield (AttackDecomposer) ==
  OK      seq(txt,txt)
  OK      role (isolé)
  BLOQUÉ  sys(role)
  BLOQUÉ  seq(frame(ovr),txt)
  BLOQUÉ  sys(seq(txt,frame(role)))

### 3. Sortie de la commande `python pipeline.py --word 4or` (Mode Chaîne 1)
                  brut : 4or
        normalisé(FST) : aor
       facteur_or(AFD) : True
   délimiteurs_ok(PDA) : True

### 4. Sortie de la commande `python pipeline.py --morpho mufafak` (Mode Chaîne 2)
{'mot': 'mufafak', 'classe(BUTA)': 'PREFIXED'}