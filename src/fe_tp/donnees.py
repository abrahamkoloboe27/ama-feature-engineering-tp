"""Chargement des réservations, découpage dans le temps et historique « à date »."""

from pathlib import Path

import numpy as np
import pandas as pd

RACINE = Path(__file__).resolve().parents[2]
FICHIER = RACINE / "data" / "raw" / "hotels.csv"
REFERENTIEL_PAYS = RACINE / "data" / "referentiels" / "pays.csv"
SORTIES = RACINE / "output"

CIBLE = "is_canceled"

MOIS = {
    "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
    "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12,
}

# Connues seulement après l'issue de la réservation (ou à l'arrivée à l'hôtel) : interdites.
FUITES = [
    "reservation_status",
    "reservation_status_date",
    "assigned_room_type",
    "booking_changes",
    "required_car_parking_spaces",
]

# Connue à la réservation, mais elle ne se répète jamais : un modèle mis en service en 2017 ne reverra pas 2015.
ECARTEES = ["arrival_date_year"]

# Les colonnes autorisées, telles qu'elles arrivent dans le fichier.
NUMERIQUES = [
    "lead_time", "arrival_date_week_number", "arrival_date_day_of_month",
    "stays_in_weekend_nights", "stays_in_week_nights", "adults", "children", "babies",
    "is_repeated_guest", "previous_cancellations", "previous_bookings_not_canceled",
    "days_in_waiting_list", "adr", "total_of_special_requests",
]
CATEGORIELLES = [
    "hotel", "arrival_date_month", "meal", "country", "market_segment", "distribution_channel",
    "reserved_room_type", "deposit_type", "customer_type", "agent", "company",
]


def charger():
    """Lit le fichier, ajoute les trois dates utiles et retire les quelques lignes impossibles."""
    df = pd.read_csv(FICHIER, na_values=["NULL"], dtype={"agent": object, "company": object})
    df.insert(0, "reservation_id", np.arange(1, len(df) + 1))
    df["date_arrivee"] = pd.to_datetime(
        {"year": df["arrival_date_year"], "month": df["arrival_date_month"].map(MOIS),
         "day": df["arrival_date_day_of_month"]}
    )
    df["date_reservation"] = df["date_arrivee"] - pd.to_timedelta(df["lead_time"], unit="D")
    df["date_cloture"] = pd.to_datetime(df["reservation_status_date"])
    personnes = df["adults"] + df["children"].fillna(0) + df["babies"]
    df = df[(personnes > 0) & df["adr"].between(0, 1000)]
    return df.sort_values(["date_arrivee", "reservation_id"]).reset_index(drop=True)


def decouper(df, part_train=0.8):
    """Entraîner sur les arrivées les plus anciennes, tester sur les suivantes (sans couper une journée)."""
    df = df.sort_values(["date_arrivee", "reservation_id"])
    coupure = df["date_arrivee"].iloc[int(len(df) * part_train)]
    return df[df["date_arrivee"] < coupure], df[df["date_arrivee"] >= coupure]


def historique_a_date(df, cle):
    """Pour chaque réservation, ce qu'on savait de sa `cle` (agent, pays…) la veille de la réservation.

    Une réservation passée ne compte que si son issue était connue : sa date de clôture
    (départ, annulation ou absence) est antérieure à la date de la nouvelle réservation.
    """
    connues = df.dropna(subset=[cle]).groupby([cle, "date_cloture"])[CIBLE].agg(["size", "sum"])
    connues = connues.groupby(level=0).cumsum().reset_index().sort_values("date_cloture")
    faites = df.dropna(subset=[cle]).groupby([cle, "date_reservation"]).size().rename("nb")
    faites = faites.groupby(level=0).cumsum().reset_index().sort_values("date_reservation")

    gauche = df[["reservation_id", cle, "date_reservation"]].dropna(subset=[cle])
    gauche = gauche.sort_values("date_reservation")
    res = pd.merge_asof(gauche, connues, left_on="date_reservation", right_on="date_cloture",
                        by=cle, allow_exact_matches=False)
    res = pd.merge_asof(res, faites.rename(columns={"date_reservation": "date"}),
                        left_on="date_reservation", right_on="date", by=cle, allow_exact_matches=False)
    sortie = pd.DataFrame({
        "reservation_id": res["reservation_id"],
        f"nb_resa_passees_{cle}": res["nb"].fillna(0),
        f"nb_issues_connues_{cle}": res["size"].fillna(0),
        f"taux_annul_passe_{cle}": res["sum"] / res["size"],
    })
    sortie = df[["reservation_id"]].merge(sortie, on="reservation_id", how="left")
    sortie.index = df.index
    return sortie.drop(columns="reservation_id")
