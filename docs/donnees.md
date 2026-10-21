# Les données

## Une réservation, une ligne

On travaille sur **Hotel booking demand** : 119 390 réservations de deux hôtels portugais, le « City Hotel » à Lisbonne et le « Resort Hotel » en Algarve, pour des arrivées du 1er juillet 2015 au 31 août 2017. C'est un jeu **réel**, extrait des systèmes de réservation des deux hôtels et anonymisé.

> N. Antonio, A. de Almeida et L. Nunes, « Hotel booking demand datasets », *Data in Brief*, vol. 22, 2019, p. 41-49, [doi:10.1016/j.dib.2018.11.126](https://doi.org/10.1016/j.dib.2018.11.126). Licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Le fichier, `data/raw/hotels.csv`, est la version publiée par TidyTuesday en février 2020. Il est redistribué sans modification ; son empreinte SHA-256 est dans `data/SHA256SUMS.txt`.

## La question posée

> **Au moment où le client réserve, la réservation sera-t-elle annulée ?**

La cible est `is_canceled`. Elle vaut 1 pour 37 % des réservations, en comptant les absences (*no-show*). C'est la même question que l'annulation des commandes du cours, posée à un hôtel : un hôtel qui sait quelles réservations risquent d'être annulées peut surréserver, relancer le client ou demander un acompte.

## Les colonnes

| Groupe | Colonnes | Connues à la réservation ? |
|---|---|---|
| Le séjour | `hotel`, dates d'arrivée, `stays_in_weekend_nights`, `stays_in_week_nights`, `adults`, `children`, `babies`, `meal`, `reserved_room_type` | oui |
| Le délai | `lead_time` : jours entre la réservation et l'arrivée | oui |
| Le prix | `adr` : tarif moyen par nuit, en euros ; `deposit_type` | oui |
| Le canal | `market_segment`, `distribution_channel`, `agent`, `company` | oui |
| Le client | `country`, `customer_type`, `is_repeated_guest`, `previous_cancellations`, `previous_bookings_not_canceled` | oui |
| Le suivi | `days_in_waiting_list`, `total_of_special_requests` | à la confirmation, ou en grande partie |
| **L'issue** | `reservation_status`, `reservation_status_date`, `assigned_room_type`, `booking_changes`, `required_car_parking_spaces` | **non** : voir [la règle d'or](regle-d-or.md) |

Le dictionnaire complet est dans [`data/README.md`](https://github.com/abrahamkoloboe27/ama-feature-engineering-tp/blob/main/data/README.md).

## Les trois dates

La fonction `fe_tp.donnees.charger()` ajoute trois dates, qui servent tout au long du TD :

| Date | Calcul | Sert à |
|---|---|---|
| `date_arrivee` | année, mois et jour d'arrivée | découper dans le temps |
| `date_reservation` | arrivée − `lead_time` jours | l'instant de la prédiction |
| `date_cloture` | `reservation_status_date` : départ, annulation ou absence | savoir **quand** l'issue est devenue connue (historique à date) |

Elle retire aussi 182 lignes impossibles : 180 réservations sans aucune personne, et 2 tarifs hors de [0, 1 000 €]. Il reste **119 208** réservations.

## Le référentiel des pays

`data/referentiels/pays.csv` associe chacun des 177 codes pays du fichier à son continent et à son appartenance à l'Union européenne en 2017. Il a été écrit pour le TD, et il sert à **enrichir par jointure** (cours 1, slide 18) : un pays rare, ou jamais vu, garde au moins son continent.
