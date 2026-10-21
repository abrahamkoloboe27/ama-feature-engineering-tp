# Installer et lancer

!!! tip "Sans rien installer"
    Tous les notebooks sont publiés **exécutés** dans ce site (menu *Notebooks*) : on peut suivre la séance en lecture seule.

## Avec uv (recommandé)

```bash
git clone https://github.com/abrahamkoloboe27/ama-feature-engineering-tp.git
cd ama-feature-engineering-tp
uv sync
uv run jupyter lab
```

`uv sync` installe Python 3.12 et toutes les dépendances dans `.venv/`, dont le petit paquet du TD, `fe_tp`.

## Sans uv

Python 3.11, 3.12 ou 3.13 :

```bash
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

La dernière ligne de `requirements.txt`, `-e .`, installe le paquet `fe_tp` en mode éditable.

## Exécuter les notebooks

Ouvrez-les dans l'ordre, de `00` à `06` : les notebooks `01` à `04` écrivent leurs scores dans `output/`, et le notebook `05` les rassemble. Pour tout réexécuter d'un coup :

```bash
uv run python scripts/executer_notebooks.py
```

Comptez une quinzaine de minutes sur un portable récent (8 cœurs). Le plus long : le réseau de neurones et le kNN, qui calculent des distances sur 95 000 réservations.

!!! warning "pandas 2, et non 3"
    Feast, utilisé dans le notebook 06, exige `pandas<3`. Tout le TD tourne donc sous **pandas 2.3**, contrairement aux modules 12 et 13. La syntaxe utilisée est la même.

## Les versions

| Outil | Version |
|---|---|
| Python | 3.12 |
| pandas | 2.3 |
| scikit-learn | 1.9 |
| Feast | 0.67 |
| DuckDB | 1.5 |
