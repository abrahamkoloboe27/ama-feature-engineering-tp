# Le feature store du TD (Feast)

Ce dossier est un dépôt [Feast](https://docs.feast.dev/) local, utilisé par le notebook
`notebooks/06_feature_store_feast.ipynb` (optionnel). Il range les variables d'historique « à date »
de l'approche B : pour chaque agent et chaque pays, le nombre de réservations passées, le nombre
d'issues connues et le taux d'annulation connu, datés.

| Fichier | Rôle |
|---|---|
| `feature_store.yaml` | la configuration : projet `hotel_annulations`, registre, magasin en ligne SQLite, magasin hors ligne en fichiers parquet |
| `definitions.py` | les définitions, en code : entités `agent` et `pays`, vues `historique_agent` et `historique_pays`, service `modele_annulation_v1` |
| `data/` | tout ce qui est généré (photos parquet, registre, magasin en ligne, jeux enregistrés) ; ignoré par Git |

## Utiliser le dépôt

Le plus simple : exécuter le notebook 06. Il vide `data/`, calcule les photos en SQL (DuckDB),
enregistre les définitions, sert les variables à l'entraînement et en production, puis montre ce que le
registre a gardé.

En ligne de commande, une fois les fichiers parquet écrits par le notebook (section 3) :

```bash
cd feature_store
uv run feast apply                                  # enregistrer les définitions dans le registre
uv run feast feature-views list                     # le catalogue
uv run feast materialize 2013-06-01T00:00:00 2017-10-01T00:00:00
uv run feast ui --port 8889                         # le catalogue dans le navigateur (8888 est le port de Jupyter)
```

Les dates de `feast materialize` sont explicites : les données s'arrêtent en 2017, et
`feast materialize-incremental` partirait de « maintenant − TTL ».

## Une règle à garder en tête

La photo du jour J est horodatée **J + 1 jour** : elle ne sert qu'aux réservations faites après J.
Les valeurs servies par Feast sont ainsi identiques à celles de `fe_tp.donnees.historique_a_date`
(le notebook 06 le vérifie, sans aucune tolérance).
