# Les quatre approches

Même fichier, même découpage, mêmes cinq modèles, mêmes métriques : **seule la préparation change**. Chaque approche est un ensemble cohérent de décisions, et chaque notebook commence par le tableau de ses choix.

| | Régression logistique | kNN | Réseau de neurones | Forêt aléatoire | Gradient boosting |
|---|---|---|---|---|---|
| Famille (fiche réflexe du cours 2) | linéaire | distances | réseau | arbres | arbres |
| Réglage | `max_iter=2000` | `n_neighbors=50` | `(64, 32)`, arrêt précoce | 200 arbres, `min_samples_leaf=5` | réglages par défaut |

Les cinq modèles sont définis une fois pour toutes dans `fe_tp.evaluation.modeles()`, et `fe_tp.evaluation.evaluer()` les entraîne tous derrière la préparation de l'approche, dans un `Pipeline` : la règle d'or est respectée par construction.

## A · Le strict minimum

*Que vaut la donnée brute, correctement encodée ?* → [notebook 01](notebooks/01_approche_A_strict_minimum.ipynb)

| Décision | Choix | Pourquoi |
|---|---|---|
| Variables | les 25 colonnes brutes autorisées, aucune création | la référence à battre |
| Numériques | médiane, puis `StandardScaler` | les modèles à distance et à gradient en ont besoin |
| Catégorielles | `OneHotEncoder(min_frequency=20, handle_unknown="infrequent_if_exist")` | aucun ordre inventé ; les modalités rares et inconnues vont dans une colonne « autres » |
| `agent`, `company`, `country` | one-hot, comme les autres | ce sont des étiquettes, pas des nombres |

## B · Le métier d'abord

*Une variable dérivée est une hypothèse qu'on peut énoncer.* → [notebook 02](notebooks/02_approche_B_variables_metier.ipynb)

| Décision | Choix | Pourquoi |
|---|---|---|
| Séjour et prix | nuits, personnes, famille, prix total, prix par personne | un gros séjour engage davantage |
| Dates | mois et jour de la semaine en (sin, cos), arrivée le week-end | décembre est voisin de janvier |
| Délai | `lead_time` et tranches métier (une semaine, un mois, trois mois, six mois) | on annule d'autant plus qu'on a réservé longtemps à l'avance |
| Historique du client | taux d'annulation passé, client connu | le passé du client prédit son comportement |
| Historique **à date** de l'agent et du pays | `merge_asof` sur la date de clôture | le passé, rien que le passé |
| Manquants | agent absent (réservation directe), société absente | l'absence est une information |
| Jointure | référentiel des pays → continent, UE, domestique | un pays rare garde son continent |
| Encodage | one-hot (petites cardinalités), `TargetEncoder` (pays, agent, société), ordinal imposé (tranches) | selon l'ordre, la cardinalité et le modèle |
| Distributions | Yeo-Johnson sur les variables asymétriques, standardisation | les modèles linéaires digèrent mal les longues traînes |

## C · Tout générer, puis réduire

*Et si l'on laissait la machine fabriquer les variables ?* → [notebook 03](notebooks/03_approche_C_generer_puis_reduire.ipynb)

| Décision | Choix | Pourquoi |
|---|---|---|
| Génération | `PolynomialFeatures(degree=2)` sur les 14 numériques, plus le one-hot : environ 470 colonnes | toutes les interactions, sans hypothèse |
| C1 · extraire | `PCA(n_components=0.95)` | garder 95 % de la variance |
| C2 · filtrer | `SelectKBest(f_classif, k=40)` | un score par variable, sans modèle |
| C3 · embedded | `SelectFromModel(LogisticRegression(l1_ratio=1, solver="liblinear", C=0.05))` | la pénalité L1 met des coefficients à zéro |
| Wrapper | `SequentialFeatureSelector` en démonstration | trop coûteux sur 470 colonnes |
| Toujours | la réduction est **dans** le pipeline | sélectionner avant de valider donne une erreur trop optimiste |

## D · Laisser faire les arbres

*Les arbres ont-ils besoin de tout ce travail ?* → [notebook 04](notebooks/04_approche_D_arbres.ipynb)

| Décision | Choix | Pourquoi |
|---|---|---|
| Variables | les 25 colonnes brutes | comme A |
| Catégorielles | `OrdinalEncoder` : un code par modalité | un arbre isole une modalité en quelques coupes |
| Échelle | aucune | un arbre ne regarde que l'ordre des valeurs |
| Gradient boosting | `HistGradientBoostingClassifier(categorical_features=...)` | le support natif des catégorielles |
| Les autres modèles | inchangés | pour voir ce que ces choix leur coûtent |

Les scores de chaque approche, modèle par modèle, sont sur la page [Résultats et fiche réflexe](resultats.md).
