"""Les variables métier de l'approche B, rangées dans une fonction pour les notebooks suivants.

Le notebook 02 les construit une à une, avec l'hypothèse de chacune, puis vérifie qu'il obtient
exactement le même tableau que `variables_metier`.
"""

import numpy as np
import pandas as pd

from fe_tp.donnees import REFERENTIEL_PAYS, historique_a_date

TRANCHES_DELAI = ["< 1 sem.", "< 1 mois", "< 3 mois", "< 6 mois", "> 6 mois"]

# Les groupes de colonnes, et la préparation que chacun reçoit dans le notebook 02.
ASYMETRIQUES = [
    "delai", "adr", "prix_total", "prix_par_personne", "nuits", "days_in_waiting_list",
    "nb_resa_passees_client", "nb_resa_passees_agent", "nb_issues_connues_agent",
    "nb_resa_passees_country", "nb_issues_connues_country",
]
NUMERIQUES_B = [
    "part_nuits_week_end", "personnes", "enfants", "famille", "total_of_special_requests", "is_repeated_guest",
    "mois_sin", "mois_cos", "jour_arrivee_sin", "jour_arrivee_cos", "arrivee_week_end",
    "jour_resa_sin", "jour_resa_cos", "client_connu", "taux_annul_client",
    "taux_annul_passe_agent", "taux_annul_passe_country",
    "agent_absent", "societe_absente", "membre_ue", "domestique",
]
CATEGORIELLES_B = [
    "hotel", "meal", "market_segment", "distribution_channel", "reserved_room_type", "deposit_type",
    "customer_type", "continent",
]
FORTE_CARDINALITE = ["country", "agent", "company"]
ORDINALES = ["tranche_delai"]


def variables_metier(df):
    """Construit les variables de l'approche B. Toutes sont connues à l'instant de la réservation."""
    v = pd.DataFrame(index=df.index)
    arrivee, reservation = df["date_arrivee"], df["date_reservation"]

    # Le séjour et le prix
    v["nuits"] = df["stays_in_weekend_nights"] + df["stays_in_week_nights"]
    v["part_nuits_week_end"] = (df["stays_in_weekend_nights"] / v["nuits"]).fillna(0)
    v["personnes"] = df["adults"] + df["children"].fillna(0) + df["babies"]
    v["enfants"] = df["children"].fillna(0) + df["babies"]
    v["famille"] = (v["enfants"] > 0).astype(int)
    v["prix_total"] = df["adr"] * v["nuits"]
    v["prix_par_personne"] = df["adr"] / v["personnes"]

    # Les dates : des cycles, pas des numéros
    v["mois_sin"] = np.sin(2 * np.pi * arrivee.dt.month / 12)
    v["mois_cos"] = np.cos(2 * np.pi * arrivee.dt.month / 12)
    v["jour_arrivee_sin"] = np.sin(2 * np.pi * arrivee.dt.dayofweek / 7)
    v["jour_arrivee_cos"] = np.cos(2 * np.pi * arrivee.dt.dayofweek / 7)
    v["arrivee_week_end"] = (arrivee.dt.dayofweek >= 5).astype(int)
    v["jour_resa_sin"] = np.sin(2 * np.pi * reservation.dt.dayofweek / 7)
    v["jour_resa_cos"] = np.cos(2 * np.pi * reservation.dt.dayofweek / 7)

    # Le délai entre la réservation et l'arrivée, brut et en tranches métier
    v["delai"] = df["lead_time"]
    v["tranche_delai"] = pd.cut(
        df["lead_time"], bins=[-1, 7, 30, 90, 180, np.inf], labels=TRANCHES_DELAI
    ).astype(str)

    # L'historique du client, fourni par l'hôtel
    passees = df["previous_cancellations"] + df["previous_bookings_not_canceled"]
    v["nb_resa_passees_client"] = passees
    v["client_connu"] = ((passees > 0) | (df["is_repeated_guest"] == 1)).astype(int)
    v["taux_annul_client"] = df["previous_cancellations"] / passees.replace(0, np.nan)

    # L'historique « à date » de l'agent et du pays : le passé, rien que le passé
    v = v.join(historique_a_date(df, "agent")).join(historique_a_date(df, "country"))

    # L'absence est une information
    v["agent_absent"] = df["agent"].isna().astype(int)
    v["societe_absente"] = df["company"].isna().astype(int)

    # Une jointure avec le référentiel des pays
    pays = pd.read_csv(REFERENTIEL_PAYS)
    jointure = df[["country"]].merge(pays, left_on="country", right_on="code_pays", how="left")
    v["continent"] = jointure["continent"].fillna("inconnu").to_numpy()
    v["membre_ue"] = jointure["membre_ue_2017"].fillna(0).astype(int).to_numpy()
    v["domestique"] = (df["country"] == "PRT").astype(int)

    # Les colonnes brutes que l'on garde telles quelles
    for colonne in CATEGORIELLES_B[:-1] + FORTE_CARDINALITE + [
        "adr", "days_in_waiting_list", "total_of_special_requests", "is_repeated_guest"
    ]:
        v[colonne] = df[colonne]
    return v
