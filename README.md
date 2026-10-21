# TD · Feature engineering & transformation

**AMA · UE Ingénierie des données · Module 14** — TD du mercredi 21 octobre 2026 (3 h) · Abraham Zacharie Koloboe

📖 **Documentation en ligne : <https://abrahamkoloboe27.github.io/ama-feature-engineering-tp/>** (les notebooks exécutés s'y lisent sans rien installer).

On veut prédire, **au moment de la réservation**, si une réservation d'hôtel sera annulée. Les données, les modèles et le découpage restent les mêmes d'un notebook à l'autre : seul le *feature engineering* change. On compare **quatre approches** sur **cinq modèles**, puis on range les variables dans un **feature store** (Feast).

| Notebook | Contenu | Cours |
|---|---|---|
| `00_cadrer_le_probleme` | la cible, les fuites, le découpage dans le temps, le score à battre | cours 1, slides 7 à 10 |
| `01_approche_A_strict_minimum` | **A** · colonnes brutes, one-hot et standardisation, rien de plus | cours 1, slides 19 à 21 ; cours 2, slide 5 |
| `02_approche_B_variables_metier` | **B** · variables métier, dates cycliques, historique « à date », jointure, encodage par la cible, Yeo-Johnson | cours 1, slides 11 à 22 ; cours 2, slides 7 et 8 |
| `03_approche_C_generer_puis_reduire` | **C** · interactions automatiques, puis ACP, filtre, wrapper et embedded | cours 1, slide 17 ; cours 2, slides 11 à 23 |
| `04_approche_D_arbres` | **D** · encodage ordinal, pas de mise à l'échelle, catégorielles natives | cours 1, slides 19 et 23 ; cours 2, slides 3 et 28 |
| `05_comparer_les_approches` | le tableau final, approche par approche et modèle par modèle, et le modèle retenu | cours 2, slides 24, 25 et 28 |
| `06_feature_store_feast` | **optionnel** · enregistrer, servir et tracer les variables avec Feast | cours 1, slide 14 |

## Installer

Avec [uv](https://docs.astral.sh/uv/) (recommandé) :

```bash
git clone https://github.com/abrahamkoloboe27/ama-feature-engineering-tp.git
cd ama-feature-engineering-tp
uv sync
uv run jupyter lab
```

Sans uv (Python 3.11 à 3.13) :

```bash
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

Ouvrez ensuite les notebooks dans l'ordre, de `00` à `06`. Pour tout réexécuter d'un coup (environ 15 minutes) :

```bash
uv run python scripts/executer_notebooks.py
```

> **pandas 2, et non 3.** Feast exige `pandas<3` : tout le TD tourne donc sous pandas 2.3, contrairement aux modules 12 et 13.

## Le dépôt

```text
data/raw/hotels.csv          le fichier source (CC BY 4.0), à ne pas modifier
data/referentiels/pays.csv   continent et appartenance à l'UE de chaque pays (pour la jointure)
src/fe_tp/                   le code partagé : chargement, découpage, historique à date, évaluation des 5 modèles
notebooks/                   les 7 notebooks, exécutés
feature_store/               le dépôt Feast du notebook 06 (définitions des entités et des vues de variables)
output/                      les sorties des notebooks 01 à 04, lues par le 05 : scores (resultats_*.csv), probabilités (probas_*.parquet), modèle retenu (modele_B.joblib)
docs/                        la documentation publiée sur GitHub Pages (MkDocs Material)
```

## Les données

*Hotel booking demand* : 119 390 réservations de deux hôtels portugais, avec des arrivées de juillet 2015 à août 2017. N. Antonio, A. de Almeida et L. Nunes, *Data in Brief* 22 (2019), [doi:10.1016/j.dib.2018.11.126](https://doi.org/10.1016/j.dib.2018.11.126), licence CC BY 4.0. Le détail des colonnes est dans [`data/README.md`](data/README.md).
