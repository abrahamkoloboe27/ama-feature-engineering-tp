"""Les cinq modèles du TD et une fonction qui les évalue tous sur le même découpage."""

import time

import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, average_precision_score, roc_auc_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline

from fe_tp.donnees import SORTIES

# Une famille de modèles par ligne de la fiche réflexe du cours 2.
FAMILLES = {
    "Régression logistique": "linéaire",
    "kNN": "distances",
    "Réseau de neurones": "réseau",
    "Forêt aléatoire": "arbres",
    "Gradient boosting": "arbres",
}


def modeles():
    """Les cinq modèles, avec des réglages fixes : seule la préparation change d'une approche à l'autre."""
    return {
        "Régression logistique": LogisticRegression(max_iter=2000),
        "kNN": KNeighborsClassifier(n_neighbors=50, n_jobs=-1),
        "Réseau de neurones": MLPClassifier(hidden_layer_sizes=(64, 32), batch_size=1000, early_stopping=True,
                                            random_state=0),
        "Forêt aléatoire": RandomForestClassifier(n_estimators=200, min_samples_leaf=5, n_jobs=-1, random_state=0),
        "Gradient boosting": HistGradientBoostingClassifier(random_state=0),
    }


def evaluer(approche, preparation, X_train, y_train, X_test, y_test, a_tester=None):
    """Entraîne préparation + modèle sur le train, mesure sur le test, enregistre les scores.

    `approche` commence par un code court suivi de « · » (« A · strict minimum », « C1 · ACP »…) :
    le code nomme les fichiers `output/resultats_<code>.csv` et `output/probas_<code>.parquet`.
    """
    code = approche.split(" · ")[0]
    lignes, pipelines = [], {}
    probas = pd.DataFrame({"y": y_test.to_numpy()})
    for nom, modele in (a_tester or modeles()).items():
        pipe = Pipeline([("prep", clone(preparation)), ("modele", modele)])
        debut = time.perf_counter()
        pipe.fit(X_train, y_train)
        proba = pipe.predict_proba(X_test)[:, 1]
        duree = time.perf_counter() - debut
        lignes.append({
            "approche": approche,
            "modele": nom,
            "famille": FAMILLES.get(nom, ""),
            "auc": roc_auc_score(y_test, proba),
            "precision_moyenne": average_precision_score(y_test, proba),
            "exactitude": accuracy_score(y_test, proba >= 0.5),
            "nb_variables": pipe[:-1].transform(X_test.head(5)).shape[1],
            "duree_s": duree,
        })
        probas[nom] = proba.astype("float32")
        pipelines[nom] = pipe
    resultats = pd.DataFrame(lignes)
    SORTIES.mkdir(exist_ok=True)
    resultats.to_csv(SORTIES / f"resultats_{code}.csv", index=False)
    probas.to_parquet(SORTIES / f"probas_{code}.parquet", index=False)
    return resultats.round(3), pipelines
