# Le feature store, avec Feast

> « Il sert les mêmes valeurs, datées, à l'entraînement et en production. »
> — cours 1, slide 14

Le notebook [06](notebooks/06_feature_store_feast.ipynb) met en place un petit feature store **local** avec [Feast](https://feast.dev), l'outil open source le plus répandu. Il ne demande ni serveur ni compte : tout tient dans le dossier `feature_store/` du dépôt.

## Le problème qu'il résout

Les variables d'historique de l'approche B, comme `taux_annul_passe_agent`, ne se calculent pas à partir d'une seule réservation : il faut tout le passé de l'agent. Trois difficultés apparaissent alors.

| Difficulté | Sans feature store | Avec un feature store |
|---|---|---|
| **Le passé, rien que le passé** | chaque projet réécrit son `merge_asof`, avec le risque d'y faire entrer le futur | la **jointure à date** (*point-in-time join*) est faite par l'outil, à partir de l'horodatage de chaque valeur |
| **Le décalage entraînement / production** (*training-serving skew*) | la production recalcule les variables avec un autre code, et les valeurs divergent | le même calcul alimente l'entraînement (magasin hors ligne) et la production (magasin en ligne) |
| **Le partage et la traçabilité** | personne ne sait quelles variables existent, qui les calcule ni quel modèle les utilise | un **catalogue** (le registre) décrit chaque variable, sa source, son propriétaire et les modèles qui la consomment |

## Le vocabulaire de Feast

| Terme | Dans le TD | Rôle |
|---|---|---|
| **Entité** (*entity*) | `agent`, `pays` | la clé sur laquelle on joint les variables |
| **Source** (*data source*) | les fichiers parquet `historique_agent.parquet` et `historique_pays.parquet` | où sont stockées les valeurs datées |
| **Vue de variables** (*feature view*) | `historique_agent`, `historique_pays` | un groupe de variables, avec son entité, sa source, son horodatage et sa durée de validité (TTL) |
| **Service de variables** (*feature service*) | `modele_annulation_v1` | la liste des variables consommées par un modèle : c'est ce qui permet de tracer « quel modèle utilise quoi » |
| **Registre** (*registry*) | `feature_store/data/registry.db` | le catalogue de toutes les définitions |
| **Magasin hors ligne** (*offline store*) | les fichiers parquet | l'historique complet, pour **entraîner** |
| **Magasin en ligne** (*online store*) | `feature_store/data/online_store.db` (SQLite) | la dernière valeur de chaque entité, pour **prédire** en quelques millisecondes |
| **Matérialisation** | `store.materialize(...)` | la copie des dernières valeurs du magasin hors ligne vers le magasin en ligne |

## Le cycle de vie, en cinq commandes

```bash
cd feature_store
uv run feast apply                 # enregistre (ou met à jour) les définitions de definitions.py dans le registre
uv run feast feature-views list    # le catalogue : les vues de variables enregistrées
uv run feast materialize 2013-06-01T00:00:00 2017-10-01T00:00:00   # remplit le magasin en ligne (données de juin 2013 à septembre 2017)
uv run feast ui                    # une interface web pour parcourir entités, vues et services
```

Le notebook fait la même chose avec l'API Python (`FeatureStore(repo_path=...)`, `store.apply(...)`, `store.get_historical_features(...)`, `store.materialize(...)`, `store.get_online_features(...)`).

## Où se calculent les variables ?

Feast **sert** les variables ; il ne les calcule pas. Dans le TD, comme souvent en entreprise, elles se calculent **dans l'entrepôt, en SQL**, avec des fonctions de fenêtre (cours 1, slide 14). Ici, DuckDB joue le rôle de l'entrepôt :

```sql
SUM(nb_annulees) OVER (
    PARTITION BY agent ORDER BY jour
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
```

Chaque ligne est une **photo** de l'agent, prise le lendemain du jour où quelque chose a changé : une nouvelle réservation, ou une issue devenue connue. La photo du jour J ne sert donc qu'aux réservations faites **après** J. C'est la règle « le passé, rien que le passé » écrite une fois pour toutes.

## Tracer et versionner

- Les définitions (`feature_store/definitions.py`) sont du **code** : elles se versionnent avec Git, se relisent en revue et se déploient avec `feast apply`.
- Le registre garde, pour chaque vue, sa source, son entité, son TTL, ses étiquettes (`tags`), sa description, sa date de création et celle de sa dernière mise à jour.
- Le service `modele_annulation_v1` fige la liste des variables du modèle. Une version 2 du modèle avec d'autres variables se déclare comme `modele_annulation_v2`, et les deux coexistent.

## Pour aller plus loin

- La [documentation de Feast](https://docs.feast.dev) : magasins en ligne Redis ou PostgreSQL, magasins hors ligne BigQuery, Snowflake ou Spark.
- Les équivalents gérés : Vertex AI Feature Store (Google Cloud), SageMaker Feature Store (AWS), Databricks Feature Store.
