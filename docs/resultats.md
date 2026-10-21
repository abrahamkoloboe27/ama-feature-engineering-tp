# Résultats et fiche réflexe

## L'AUC ROC sur le test

24 018 réservations, avec des arrivées du 22 avril au 31 août 2017. Le meilleur score de chaque colonne est en gras.

| Approche | Colonnes | Rég. logistique | kNN | Réseau de neurones | Forêt aléatoire | Gradient boosting |
|---|---|---|---|---|---|---|
| A · strict minimum | 365 | **0,853** | 0,817 | 0,854 | 0,870 | 0,873 |
| B · variables métier | 83 | 0,851 | **0,853** | **0,881** | **0,888** | **0,888** |
| C1 · interactions + ACP | 95 axes | 0,795 | 0,743 | 0,819 | 0,789 | 0,807 |
| C2 · interactions + filtre | 40 | 0,808 | 0,803 | 0,815 | 0,819 | 0,826 |
| C3 · interactions + L1 | 182 | 0,845 | 0,762 | 0,850 | 0,837 | 0,867 |
| D · arbres natifs | 25 | 0,786 | 0,719 | 0,792 | 0,852 | 0,870 |

Le modèle retenu, **B + gradient boosting**, obtient aussi la meilleure précision moyenne (0,853) et la meilleure exactitude au seuil 0,5 (0,797). Le notebook [05](notebooks/05_comparer_les_approches.ipynb) le détaille, avec les courbes ROC et les durées.

## Ce que disent les chiffres

1. **Le métier paie.** Les variables de B (historique à date, délai, dates cycliques, jointure, encodage par la cible) font gagner 0,015 au gradient boosting, 0,017 à la forêt, 0,026 au réseau et 0,036 au kNN, avec 83 colonnes au lieu de 365. La régression logistique, elle, ne gagne rien (0,851 contre 0,853) : les colonnes brutes, bien encodées, lui suffisaient déjà.
2. **Générer sans hypothèse ne suffit pas.** Aucune variante de C ne bat A. L'ACP, non supervisée, garde la variance et non l'information utile pour la cible : tous les modèles reculent. Le filtre univarié jette des colonnes utiles. La pénalité L1 s'en sort le mieux, mais reste en dessous de A.
3. **La bonne préparation dépend du modèle.** Avec des codes ordinaux et sans mise à l'échelle (D), le gradient boosting natif reste au niveau de A (0,870 contre 0,873), avec 25 colonnes et en quelques secondes ; la forêt, sans support natif, perd un peu (0,852 contre 0,870). La régression logistique, le kNN et le réseau, eux, chutent de 0,06 à 0,10.
4. **Le cadre compte autant que les variables.** Une fuite donne une AUC de 1 ; un découpage au hasard flatte le score ; un encodage par la cible appris sur train + test gagne deux points qui n'existeront jamais en production (notebooks 00 et 02).

## La fiche réflexe du cours 2, vérifiée sur les données

| Famille | Mise à l'échelle | Catégorielles | Sélection ou réduction | Ce qu'on a mesuré |
|---|---|---|---|---|
| Linéaires et logistiques | nécessaire | one-hot, ou encodage par la cible | utile, Lasso intégré | D (codes ordinaux, échelles brutes) : 0,853 → 0,786, et une convergence lente |
| kNN, SVM, k-means, ACP | indispensable | one-hot | très utile | le plus sensible : de 0,719 (D) à 0,853 (B) |
| Réseaux de neurones | indispensable | one-hot ou plongements | souvent apprise | meilleur avec B (0,881) |
| Arbres, forêts, boosting | inutile | ordinal ou support natif | pour le coût et la lisibilité | le boosting natif de D égale A (0,870 contre 0,873) avec 15 fois moins de colonnes ; la forêt perd 0,018 |

## Les limites de cette comparaison

- Un seul découpage dans le temps et un seul tirage : une autre graine déplace l'AUC de B d'environ 0,002, presque autant que l'écart entre A et D pour le boosting (0,003) : on ne départage pas de tels écarts. L'avance de B sur A (environ 0,015) résiste, elle, au bootstrap comme aux graines (notebook 05).
- Aucun réglage d'hyperparamètres : chaque modèle garde les mêmes réglages dans toutes les approches.
- Deux hôtels, une période : rien ne garantit que les mêmes choix gagneraient ailleurs.
