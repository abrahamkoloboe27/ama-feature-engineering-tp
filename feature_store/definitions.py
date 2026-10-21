"""Les définitions du feature store du TD : deux entités, deux vues de variables, un service.

Ce fichier est du code : il se relit, se versionne avec Git et s'enregistre dans le registre
avec `feast apply` (ou `FeatureStore.apply` dans le notebook 06).

Chaque ligne des fichiers parquet est une « photo » : ce qu'on savait d'un agent (ou d'un pays)
à l'instant `date_photo`. La photo du jour J est horodatée J + 1 jour : elle ne sert qu'aux
réservations faites après J, comme `fe_tp.donnees.historique_a_date`.
"""

from datetime import timedelta

from feast import Entity, FeatureService, FeatureView, Field, FileSource, ValueType
from feast.types import Float64, Int64, String

PROPRIETAIRE = "AMA · module 14"
DIX_ANS = timedelta(days=3650)  # une photo reste valable longtemps : les données vont de 2013 à 2017

# Les entités : les clés sur lesquelles on joint les variables
agent = Entity(
    name="agent",
    join_keys=["agent"],
    value_type=ValueType.STRING,
    description="Agence de voyages qui a saisi la réservation (identifiant anonymisé du fichier).",
    tags={"domaine": "réservations hôtelières"},
    owner=PROPRIETAIRE,
)
pays = Entity(
    name="pays",
    join_keys=["country"],
    value_type=ValueType.STRING,
    description="Pays d'origine du client (code ISO 3166-1 à trois lettres).",
    tags={"domaine": "réservations hôtelières"},
    owner=PROPRIETAIRE,
)

# Les sources : les photos calculées dans l'entrepôt (DuckDB) et écrites en parquet
photos_agent = FileSource(
    name="photos_agent",
    path="data/historique_agent.parquet",
    timestamp_field="date_photo",
    description="Une photo par agent et par jour où son historique change.",
)
photos_pays = FileSource(
    name="photos_pays",
    path="data/historique_pays.parquet",
    timestamp_field="date_photo",
    description="Une photo par pays et par jour où son historique change.",
)


def variables(cle):
    """Les trois variables d'historique à date d'une clé, avec les mêmes noms que dans `fe_tp`."""
    return [
        Field(name=f"nb_resa_passees_{cle}", dtype=Int64,
              description="Réservations faites avant le jour de la réservation."),
        Field(name=f"nb_issues_connues_{cle}", dtype=Int64,
              description="Réservations closes (séjour, annulation ou absence) avant ce jour."),
        Field(name=f"taux_annul_passe_{cle}", dtype=Float64,
              description="Part d'annulations parmi les issues connues ; vide s'il n'y en a aucune."),
    ]


# Les vues : quelles variables, pour quelle entité, depuis quelle source
historique_agent = FeatureView(
    name="historique_agent",
    entities=[agent],
    ttl=DIX_ANS,
    schema=[Field(name="agent", dtype=String)] + variables("agent"),
    source=photos_agent,
    online=True,
    description="Le passé de l'agent, rien que le passé : volume et taux d'annulation connus à date.",
    tags={"cours": "module 14, cours 1, slide 14", "calcul": "SQL (fonctions de fenêtre)", "fuite": "aucune"},
    owner=PROPRIETAIRE,
)
historique_pays = FeatureView(
    name="historique_pays",
    entities=[pays],
    ttl=DIX_ANS,
    schema=[Field(name="country", dtype=String)] + variables("country"),
    source=photos_pays,
    online=True,
    description="Le passé du pays d'origine : volume et taux d'annulation connus à date.",
    tags={"cours": "module 14, cours 1, slide 14", "calcul": "SQL (fonctions de fenêtre)", "fuite": "aucune"},
    owner=PROPRIETAIRE,
)

# Le service : l'ensemble des variables qu'un modèle consomme, sous un nom versionné
modele_annulation_v1 = FeatureService(
    name="modele_annulation_v1",
    features=[historique_agent, historique_pays],
    description="Variables d'historique à date du modèle d'annulation (approche B du TD).",
    tags={"modele": "approche B · gradient boosting", "version": "1"},
    owner=PROPRIETAIRE,
)
