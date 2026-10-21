"""Exécute les notebooks en place, dans l'ordre, et s'arrête à la première erreur.

    uv run python scripts/executer_notebooks.py                     # tous les notebooks
    uv run python scripts/executer_notebooks.py notebooks/02_*.ipynb  # un seul
"""

import sys
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient

RACINE = Path(__file__).resolve().parents[1]
DOSSIER = RACINE / "notebooks"

chemins = [Path(p).resolve() for p in sys.argv[1:]] or sorted(DOSSIER.glob("[0-9][0-9]_*.ipynb"))
for chemin in chemins:
    debut = time.perf_counter()
    nb = nbformat.read(chemin, as_version=4)
    NotebookClient(nb, timeout=1200, kernel_name="python3", resources={"metadata": {"path": str(DOSSIER)}}).execute()
    nbformat.write(nb, chemin)
    alertes = [
        sortie.get("text", "")
        for cellule in nb.cells if cellule.cell_type == "code"
        for sortie in cellule.get("outputs", [])
        if sortie.get("name") == "stderr"
    ]
    print(f"{chemin.name} : {time.perf_counter() - debut:.0f} s", "· ⚠ sorties stderr" if alertes else "")
    for texte in alertes:
        print("   ", texte.strip()[:300])
