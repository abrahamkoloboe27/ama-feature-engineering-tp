# TD · Feature engineering & transformation

**AMA · UE Ingénierie des données · Module 14** — TD du mercredi 21 octobre 2026 (3 h) · Abraham Zacharie Koloboe

> **Au moment où le client réserve, la réservation sera-t-elle annulée ?**

On répond à cette question sur **119 208 réservations réelles** de deux hôtels portugais, et on la pose **six fois** : même fichier, même découpage dans le temps, mêmes cinq modèles. Seul le *feature engineering* change. À la fin, on compare, on choisit, puis on range les variables dans un **feature store**.

## Le TD en un tableau

| Notebook | Ce qu'on y fait | Cours |
|---|---|---|
| [00 · Cadrer le problème](notebooks/00_cadrer_le_probleme.ipynb) | la cible, les fuites, le découpage dans le temps, le score à battre | cours 1, slides 7 à 10 |
| [01 · A · Le strict minimum](notebooks/01_approche_A_strict_minimum.ipynb) | colonnes brutes, one-hot et standardisation, rien de plus | cours 1, slides 19 à 21 |
| [02 · B · Le métier d'abord](notebooks/02_approche_B_variables_metier.ipynb) | variables métier, dates cycliques, historique à date, jointure, encodage par la cible | cours 1, slides 11 à 22 ; cours 2, slides 7 et 8 |
| [03 · C · Générer puis réduire](notebooks/03_approche_C_generer_puis_reduire.ipynb) | interactions automatiques, puis ACP, filtre, wrapper et L1 | cours 1, slide 17 ; cours 2, slides 11 à 23 |
| [04 · D · Laisser faire les arbres](notebooks/04_approche_D_arbres.ipynb) | encodage ordinal, sans mise à l'échelle, catégorielles natives | cours 1, slide 19 ; cours 2, slides 3 et 28 |
| [05 · Comparer les approches](notebooks/05_comparer_les_approches.ipynb) | le tableau final et le modèle retenu, face à des réservations nouvelles | cours 2, slides 24, 25 et 28 |
| [06 · Feature store avec Feast](notebooks/06_feature_store_feast.ipynb) | **optionnel** : calculer en SQL, enregistrer, servir et tracer les variables | cours 1, slide 14 |

## Le résultat, en une phrase

Les **variables métier** (B) donnent le meilleur score pour quatre modèles sur cinq : le gradient boosting atteint une **AUC de 0,888**, contre 0,873 avec les colonnes brutes. Générer des variables sans hypothèse (C) ne bat jamais la référence, et la bonne préparation **dépend du modèle** : les arbres se contentent d'un encodage ordinal, alors que le kNN et le réseau de neurones en souffrent. Le détail est sur la page [Résultats et fiche réflexe](resultats.md).

## Par où commencer

1. [Installer et lancer](installation.md) le dépôt, ou lire directement les notebooks exécutés dans le menu.
2. [Les données](donnees.md) et [la règle d'or](regle-d-or.md) : la question, les colonnes, les fuites et le découpage.
3. [Les quatre approches](approches.md) : le tableau des choix de chacune.

Le code est sur GitHub : [abrahamkoloboe27/ama-feature-engineering-tp](https://github.com/abrahamkoloboe27/ama-feature-engineering-tp).

!!! info "Les données"
    *Hotel booking demand* : N. Antonio, A. de Almeida et L. Nunes, *Data in Brief* 22 (2019), [doi:10.1016/j.dib.2018.11.126](https://doi.org/10.1016/j.dib.2018.11.126), licence CC BY 4.0.
