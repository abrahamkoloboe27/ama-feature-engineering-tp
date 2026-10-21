# Les données du TD

## `raw/hotels.csv` : les réservations (fichier source, à ne pas modifier)

**Hotel booking demand**, 119 390 réservations × 32 colonnes. Deux hôtels portugais : le « City Hotel » à Lisbonne et le « Resort Hotel » en Algarve. Les arrivées vont du 1er juillet 2015 au 31 août 2017.

- Source : N. Antonio, A. de Almeida et L. Nunes, « Hotel booking demand datasets », *Data in Brief*, vol. 22, 2019, p. 41-49, [doi:10.1016/j.dib.2018.11.126](https://doi.org/10.1016/j.dib.2018.11.126).
- Licence : [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Le fichier est redistribué ici sans modification.
- Version utilisée : la fusion des deux fichiers H1 et H2 publiée par [TidyTuesday](https://github.com/rfordatascience/tidytuesday/tree/master/data/2020/2020-02-11) le 11 février 2020.
- Empreinte SHA-256 : `7c2ae42a7353905ea136e5c2287f17c92c5435826598bfbb8491c6f0c7b1fc06` (voir `SHA256SUMS.txt`).

| Colonne | Signification | Connue à la réservation ? |
|---|---|---|
| `hotel` | « City Hotel » (Lisbonne) ou « Resort Hotel » (Algarve) | oui |
| `is_canceled` | **la cible** : 1 si la réservation a été annulée (y compris les absences), 0 sinon | — |
| `lead_time` | nombre de jours entre la réservation et l'arrivée | oui |
| `arrival_date_year`, `arrival_date_month`, `arrival_date_week_number`, `arrival_date_day_of_month` | date d'arrivée prévue | oui |
| `stays_in_weekend_nights`, `stays_in_week_nights` | nuits de week-end (samedi, dimanche) et de semaine réservées | oui |
| `adults`, `children`, `babies` | nombre de personnes | oui |
| `meal` | formule : `BB` petit-déjeuner, `HB` demi-pension, `FB` pension complète, `SC` ou `Undefined` sans repas | oui |
| `country` | pays d'origine du client (code ISO à trois lettres) | oui |
| `market_segment`, `distribution_channel` | segment de marché et canal de vente (`TA` agence de voyages, `TO` voyagiste) | oui |
| `is_repeated_guest`, `previous_cancellations`, `previous_bookings_not_canceled` | historique du client avant cette réservation | oui |
| `reserved_room_type` | type de chambre réservé (code anonymisé) | oui |
| `assigned_room_type` | type de chambre attribué | **non** : attribué au check-in |
| `booking_changes` | nombre de modifications entre la saisie et l'arrivée (ou l'annulation) | **non** : vaut 0 au moment de la réservation |
| `deposit_type` | `No Deposit`, `Non Refund` (acompte non remboursable), `Refundable` | oui |
| `agent`, `company` | identifiant de l'agence de voyages, de l'entreprise qui paie (`NULL` si aucune) | oui |
| `days_in_waiting_list` | jours passés en liste d'attente avant la confirmation | oui, à la confirmation |
| `customer_type` | `Transient`, `Transient-Party`, `Contract`, `Group` | oui |
| `adr` | tarif moyen par nuit (*average daily rate*), en euros | oui |
| `required_car_parking_spaces` | places de parking demandées | **non** : 0 % d'annulation dès qu'elle vaut 1, saisie à l'arrivée |
| `total_of_special_requests` | nombre de demandes particulières (étage, lit…) | en grande partie, à discuter |
| `reservation_status`, `reservation_status_date` | dernier statut (`Canceled`, `Check-Out`, `No-Show`) et sa date | **non** : c'est l'issue elle-même |

## `referentiels/pays.csv` : le référentiel des pays (écrit pour le TD)

Les 177 codes pays du fichier, avec `continent` et `membre_ue_2017` (1 si le pays était membre de l'Union européenne en 2017, Royaume-Uni compris). Il sert à la jointure du notebook 02 (cours 1, slide 18). Deux codes sont particuliers : `CN`, un doublon non standard de `CHN`, et `TMP`, l'ancien code du Timor oriental.
