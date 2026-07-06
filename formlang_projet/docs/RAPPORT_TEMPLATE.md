# Rapport de projet — formlang

**Binôme :** DOUGLOUI Adinette · YEMADJE Waldo Coras
**Dépôt Git :** <https://github.com/Adinette/DOUGLOUI_Adinette_YEMADJE_Waldo_formlang.git>·   **Commit final :** <hash>

## 0. Résumé (½ page)

Ce projet implémente et orchestre une chaîne complète de traitement des langages formels, structurée rigoureusement selon les différents étages de la hiérarchie de Chomsky. L'architecture globale est articulée autour d'un noyau théorique modulaire ("formlang") fournissant les moteurs d'exécution abstraits (automates finis, transducteurs, automates à pile, automates d'arbres BUTA et machines de Turing), exploitée par des applications concrètes de sécurité (détection d'attaques complexes et normalisation de chaînes) et de calcul (calculatrice unaire compilée via une machine de Turing universelle). Un pipeline d'intégration centralise le traitement de bout en bout d'une entrée, validant ainsi la transition fluide de la donnée à travers chaque couche théorique.

L'intégralité du banc de tests unitaires a été validée avec succès sur notre environnement local, attestant de la robustesse mathématique et algorithmique de chacun de nos composants.

Résultat global de pytest :
................................................................ [100%]
======================= short test summary info =======================
28 passed in 0.31s

## 1. Étage régulier & transducteurs (Jour 1)
- AFD de `L₁`, table de transition, **minimalité** (justification).
- regex → AFN → AFD → minimal.
- Idempotence du FST leet (preuve).
- Miroir : one-way impossible / two-way possible (argument mémoire bornée).

### Q1.1. Expression reguliere pour L1 : 
(a|o|r)*or(a|o|r)*
Explication :
Un mot de L1 possede obligatoirement la sous-chaine "or". Ce facteur peut etre precede par n'importe quelle suite de lettres de l'alphabet (representee par (a|o|r)*) et suivi par n'importe quelle suite de lettres de l'alphabet (representee par (a|o|r)*).

### Q1.2. Construire un AFN pour $L_1$, le déterminiser puis le minimiser. Donner la table de l'AFD minimal, le dessiner, indiquer le nombre d'états.
1. AFN d'origine :
Etats : {q0, q1, q2} avec q0 initial et q2 acceptant.
Transitions :
- En q0 : boucle sur 'a', 'o', 'r'. Sur la lettre 'o', on peut aussi aller en q1.
- En q1 : sur la lettre 'r', on va en q2.
- En q2 : boucle sur 'a', 'o', 'r'.

2. Table de transition de l'AFD minimal (3 etats) :
Etat | Lettre 'a' | Lettre 'o' | Lettre 'r' | Acceptant ?
---------------------------------------------------------
A    |     A      |     B      |     A      | Non (Initial)
B    |     A      |     B      |     C      | Non
C    |     C      |     C      |     C      | Oui (Absorbant)

Nombre d'etats : 3 etats (A, B, C). C'est exactement l'automate qui a ete implemente dans le fichier detector.py.

### Q1.3. Expression reguliere pour L1' :
(a|o|r)*o(a|o|r)*r(a|o|r)*

Difference avec L1 :
Dans L1, le 'o' et le 'r' doivent etre immediatement adjacents (c'est le facteur strict "or"). Des mots comme "oar" ou "orar" ne fonctionnent pas.
Dans L1', le 'o' doit simplement apparaitre avant le 'r' (sous-sequence). Le mot "oar" est donc valide pour L1' car le 'o' est bien suivi plus loin d'un 'r'.

Inclusion L1 dans L1' :
Cette inclusion est vraie. Tout mot qui contient le facteur immediat "or" contient obligatoirement un 'o' suivi (immediatement) d'un 'r'. Donc, tout mot de L1 appartient forcement a L1'. L'inverse n'est pas vrai (par exemple, "oar" appartient a L1' mais pas a L1).

Miroir (dans le rapport) :
Pourquoi un transducteur two-way le permet :
Un transducteur two-way possede une tete de lecture capable de se deplacer vers la gauche et vers la droite. Pour effectuer le renversement, il lui suffit de deplacer sa tete tout a la fin du mot d'entree sans rien ecrire, puis de revenir pas a pas vers la gauche jusqu'au debut en ecrivant chaque lettre sur laquelle il passe. La memoire infinie est ici compressee par la possibilite de relire le ruban d'entree.

## 2. Hors-contexte (Jour 2)
- Preuve de non-régularité de `{[ⁿ]ⁿ}` (pompage).
- Grammaire des prompts bien parenthésés ; ambiguïté + désambiguïsation.
- PDA : fonction de transition.

### Q2.1.
Preuve par le lemme de l'etoile pour D = { [^n ]^n | n >= 0 } :

1. Supposons par l'absurde que le langage D soit regulier. Alors, d'apres le lemme de l'etoile, il existe un entier de pompage p >= 1 tel que tout mot w de D avec une longueur |w| >= p peut se decomposer en w = xyz avec |xy| <= p, |y| > 0, et xy^iz appartenant a D pour tout i >= 0.

2. Choisissons le mot critique w = [^p ]^p. Ce mot appartient a D et sa longueur est 2p >= p.

3. Analysons la decomposition w = xyz. Puisque la condition du lemme impose |xy| <= p, la sous-chaine xy est entierement contenue dans la premiere moitie du mot, c'est-a-dire uniquement dans la sequence de crochets ouvrants [^p. Par consequent, la chaine a pomper 'y' ne contient que des crochets ouvrants (y = [^k avec k >= 1 car y != epsilon).

4. Effectuons le pompage pour i = 2 : le mot pompe devient w' = xy^2z. Ce mot contient desormais p + k crochets ouvrants (car on a duplique y), mais contient toujours exactement p crochets fermants (car z est reste intact). Comme k >= 1, le nombre d'ouvrants p+k est strictement superieur au nombre de fermants p. Donc w' n'appartient pas a D.

Conclusion :
Il y a une contradiction avec le lemme de l'etoile. Notre supposition initiale est fausse : le langage D n'est pas regulier. Par extension, le SingularityDetector (base sur un AFD) possede une memoire finie bornee par son nombre d'etats ; il est donc structurellement incapable de compter un nombre arbitrairement grand de crochets pour verifier leur bonne imbrication.

### Q2.2.
Grammaire G des prompts bien parentheses sur l'alphabet {a, o, r, [, ], (, )} :

S -> S S | [ S ] | ( S ) | V | epsilon
V -> a | o | r

Explication : Un prompt bien forme peut etre la concatenation de deux blocs bien formes (SS), un bloc entoure de crochets ([S]), un bloc entoure de parentheses ((S)), une lettre libre (V), ou simplement vide (epsilon).

### Q2.3.
1. Ambiguite de G : Oui, la grammaire G est ambigue.
Le mot "aaa" (qui derive de VVV) peut obtenir plusieurs arbres de derivation a cause de la regle associative gauche/droite S -> SS.
- Arbre 1 (Regroupement a gauche) : S => SS => (SS)S => (VV)S => VVV => aaa
- Arbre 2 (Regroupement a droite) : S => SS => S(SS) => SVV => VVV => aaa

2. Grammaire non ambigue equivalente :
Pour supprimer l'ambiguite, on force une structure stricte de gauche a droite pour la concatenation et on separe les blocs atomiques :

S -> T S | epsilon
T -> [ S ] | ( S ) | a | o | r

## 3. Arbres (Jour 3) — pivot
- BUTA : définition utilisée, règles Δ morpho et Δ shield.
- **Preuve d'unité** : extrait montrant que les deux apps instancient
  `formlang.tree.TreeAutomaton`.
- Pourquoi un AFD de mots échoue ; théorème du yield ; produit (intersection).
- Traces : exécution ascendante sur 2–3 arbres (état par nœud).

### Q3.1.
Demonstration du determinisme et du cout O(n) :

1. Determinisme :
Les automates d'arbres morpho_automaton et shield_automaton sont deterministes car leur table de transition Delta contient au plus une seule regle (c'est-a-dire un unique etat cible) pour chaque couple compose d'un (symbole, etats des enfants). Il n'y a donc aucun choix ambigu lors du calcul.

2. Unicite et cout :
Puisque l'automate est deterministe, l'arbre possede une unique execution possible (un seul marquage d'etats de bas en haut). Pour chaque noeud de l'arbre, on effectue une seule verification dans la table de transition. L'acces a un dictionnaire/table se fait en temps constant O(1). Par consequent, le temps total necessaire pour verifier un arbre est proportionnel au nombre total de noeuds 'n', ce qui donne une complexite lineaire stricte en O(n).

### Q3.2.
Echec d'un AFD de mots pour valider la structure :

Un AFD de mots ne lit que la frontiere (le "yield", c'est-a-dire la sequence plate des feuilles de gauche a droite). Il est donc totalement aveugle a l'organisation hierarchique et aux parentheses structurelles implicites.

Exemple de deux arbres differents ayant exactement la meme frontiere :
Prenons le cas de la morphologie d'un mot contenant un prefixe et un suffixe.
Arbre 1 (Le prefixe s'attache d'abord) :
    word
   /    \
 rest  suffix
 /  \
pref root

Arbre 2 (Le suffixe s'attache d'abord) :
    word
   /    \
pref   rest
       /  \
    root suffix

Ces deux arbres ont exactement la meme frontiere textuelle (prefixe + root + suffixe), mais des structures hierarchiques completement differentes. Un AFD classique acceptera ou rejettera les deux de la meme maniere, echouant a capturer la bonne relation syntaxique.

### Q3.3.
Theoreme du yield et lien avec le Jour 1 :

D'apres le theoreme du yield, l'ensemble des frontieres textuelles des arbres acceptes par un automate d'arbres regulier forme un langage hors-contexte (algebrique).

Dans le cas particulier de notre automate morphologique, les structures d'arbres imposent qu'on regroupe une liste de prefixes, suivis d'une racine unique, suivis d'une liste de suffixes. La frontiere de ces arbres correspond a la sequence reguliere : p* r s* (zero ou plusieurs prefixes, une racine, zero ou plusieurs suffixes).
C'est un langage regulier, ce qui montre le pont direct entre la structure interne (l'arbre calcule au jour 3) et la surface du mot (la chaine de caracteres analysee au jour 1).

### Q3.4.
La reduplication et la regularite :

1. Regularite du langage d'arbres :
Non, la reduplication n'engendre pas un langage d'arbres regulier. 

2. Intuition :
La reduplication consiste a copier une partie arbitraire de la racine (par exemple doubler un mot comme dans le langage classique {ww | w dans Sigma*}). Pour verifier qu'une structure est la copie conforme d'une autre structure de taille non bornee, un automate fini ou un automate d'arbres regulier devrait disposer d'un nombre infini d'etats pour memoriser la premiere partie avant de la comparer a la seconde. Comme la memoire d'un automate regulier est finie, il est impossible de capturer cette dependance croisee. Culy (1985) a d'ailleurs montre en linguistique reelle que la reduplication dans la langue Bambara depasse meme les capacites des grammaires hors-contexte.

### Q3.5.
Analyse de la compression par Hash-consing :

Formule : compression = 1 - (uniques / total)

1. Famille de langues ciblee :
On attend un taux de partage et de compression beaucoup plus eleve sur les langues *agglutinantes* (comme le turc ou le finnois). Ces langues construisent leurs mots en empilant de longues chaines de suffixes grammaticaux standardises. Beaucoup de mots partagent donc exactement les memes sous-arbres de suffixes. A l'inverse, les langues isolantes (comme l'anglais) utilisent peu d'affixes et partagent donc beaucoup moins de sous-structures en memoire.

## 4. Calculabilité (Jour 4)
- MT générique : invariant, trace d'une exécution.
- MTU : encodage, vérification `U(⟨M⟩##w) == M(w)`.
- Calculatrice : tables ADD/SUB **expliquées ligne par ligne** ; MUL/DIV par
  composition. Résultats des tests exhaustifs.
- Surcoût de simulation (sourcé) ; indécidabilité de l'arrêt.

### Q4.1. Pourquoi le format JSON permet-il un encodage injectif des machines de Turing ?
Le format JSON convertit les objets structurés (dictionnaires, listes, ensembles triés) en chaînes de caractères brutes. En utilisant l'argument `sort_keys=True` lors du `json.dumps`, on s'assure que l'ordre des transitions reste strictement identique peu importe l'état initial de la mémoire. Deux machines ayant le même comportement auront exactement la même chaîne de description <M>, garantissant l'injectivité de la linéarisation.

### Q4.2. Quelle est la différence fondamentale entre la méthode run() classique et la machine universelle ?
La méthode `run()` standard simule directement une machine figée en exécutant sa table de transitions sur un mot. La machine universelle (UTM), quant à elle, reçoit la description d'une machine sous forme de données (<M>) et un mot (w). Elle extrait et reconstruit dynamiquement l'automate à la volée avant de déléguer l'exécution. Cela illustre le concept d'Alan Turing où un programme est traité exactement comme une donnée manipulable en mémoire.

## 5. Intégration & Myhill–Nerode (Jour 5)
- `pipeline.py` : un exemple bout-en-bout commenté.
- Classes d'équivalence de `L₁` ; lien avec l'AFD minimal.
- (Bonus) hash-consing : `total / uniques / compression` mesurés.

### Q5.1 : Énoncé de Myhill–Nerode et application à L1
La relation de congruence de Myhill-Nerode (notée ≈_L) stipule que deux mots u et v sont équivalents par rapport à un langage L si et seulement si pour tout suffixe w, on a :
uw ∈ L ⟺ vw ∈ L.

Le théorème de Myhill-Nerode démontre qu'un langage L est régulier si et seulement si le nombre de classes d'équivalence de cette relation (appelé l'indice de la relation) est fini. De plus, cet indice est exactement égal au nombre d'états de l'AFD minimal reconnaissant L. 

Pour L₁ = {w contient « or »}, il existe exactement 3 classes d'équivalence :
1. La classe des mots ne contenant pas « or » et ne se terminant pas par 'o' (ex: "abc").

2. La classe des mots ne contenant pas « or » mais se terminant par 'o' (ex: "abco").

3. La classe des mots contenant déjà le facteur « or » (ex: "abcor").
Ces 3 classes correspondent bijectivement aux 3 états de l'AFD minimal développé lors du Jour 1.

### Q5.2 : Critère des suffixes témoins et lien avec la fusion d'états
En pratique, tester l'ensemble infini des suffixes possibles est impossible. On restreint donc l'évaluation à un ensemble fini de "suffixes témoins" pertinents (distinctifs). Deux mots u et v possèdent la même "signature de Nerode" s'ils se comportent de la même manière vis-à-vis de tous les éléments de cet ensemble témoin.

Lors de la minimisation d'un AFD (Jour 1), la fusion de deux états revient précisément à identifier que tous les mots menant à ces deux états partagent la même signature future pour tous les suffixes possibles. Fusionner deux états équivaut à regrouper leurs mots d'accès dans une seule et unique classe de congruence de Myhill-Nerode.

## 6. Difficultés rencontrées & choix de conception

### Difficultés rencontrées
* Gestion des types de clés lors de l'encodage JSON (Jour 4) : La principale difficulté technique a résidé dans la sérialisation des tables de transitions des machines de Turing pour la machine universelle (UTM). Le format JSON convertissant nativement toutes les clés de dictionnaire en chaînes de caractères (str), cela a provoqué des incohérences de types et des erreurs KeyError ou des échecs de comparaison de traces de rubans lors de l'exécution via l'interpréteur universel. Nous avons dû harmoniser et forcer le transtypage des coordonnées des rubans et des états pour assurer la conformité avec le framework de test.

* Gestion des effets de bord sur le ruban (Soustraction unaire) : Concevoir une machine de Turing pour la soustraction tronquée à 0 qui valide à la fois les cas standards (ex: 3 - 2 = 1) et les cas d'égalités strictes (ex: 2 - 2 = 0) a nécessité de nombreuses itérations. Le nettoyage complet des symboles résiduels (le tiret '-' notamment) sans casser la fonction interne _read() ou laisser de clés orphelines a demandé une restructuration fine des états de fin de course (q_clean).

* Croisement des règles pour l'intersection d'automates d'arbres (Jour 3) : L'implémentation du produit cartésien pour le TreeAutomaton a révélé des subtilités concernant le repérage exact des attributs d'états finaux (final_states), l'automate devant propager des couples d'états de manière strictement synchrone sur des structures de termes inductives.

### Choix de conception
* Encodage hermétique au sein de l'interpréteur : Pour immuniser l'application de calculatrice contre les variations de types de données induites par le couple encode / decode de l'UTM, nous avons opté pour une encapsulation stricte et un nettoyage à la volée des transitions au sein de la classe UniversalInterpreter. Cela a permis de découpler proprement la logique de simulation pure de l'automate de celle du framework de test global.

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