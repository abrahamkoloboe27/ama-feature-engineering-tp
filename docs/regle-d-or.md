# La règle d'or et les fuites

> **Tout ce qui apprend s'ajuste sur le train, et seulement sur le train.**
> — cours 1, slide 7

## La question réflexe

Avant chaque variable : « **Cette valeur était-elle connue à l'instant de la réservation ?** » Le notebook 00 passe chaque colonne suspecte à ce crible.

| Colonne | Pourquoi elle triche | Indice dans les données |
|---|---|---|
| `reservation_status` | c'est l'issue elle-même : `Canceled`, `No-Show` ou `Check-Out` | un modèle qui la voit obtient une AUC de 1,0 |
| `reservation_status_date` | la date de ce statut | idem, à travers la date |
| `assigned_room_type` | la chambre est attribuée au check-in | 5 % d'annulations quand elle diffère de la chambre réservée, contre 42 % sinon |
| `booking_changes` | compte les modifications faites **après** la réservation | elle vaut 0 à l'instant de la réservation, par définition |
| `required_car_parking_spaces` | la place de parking se note à l'arrivée | **0 %** d'annulation sur les 7 409 réservations qui en ont une (7 416 dans le fichier brut, avant `charger()`) |

Deux colonnes surprenantes, mais **légitimes** :

- `deposit_type = "Non Refund"` : 99,4 % d'annulations pour un acompte non remboursable. C'est contre-intuitif, mais connu dès la réservation. Il s'agit surtout de réservations de groupes faites par quelques agences, qui bloquent des chambres puis les relâchent. Une variable étrange n'est pas forcément une fuite.
- `previous_cancellations` : connue à la réservation, puisqu'elle compte les annulations **antérieures** du client.

## Découper dans le temps

Les réservations sont datées, et le modèle servira sur les réservations de demain : on le teste donc sur l'avenir (cours 1, slide 9).

```python
from fe_tp.donnees import charger, decouper

df = charger()
train, test = decouper(df)   # 80 % des arrivées les plus anciennes, puis les 20 % suivantes
```

| Jeu | Arrivées | Réservations | Taux d'annulation |
|---|---|---|---|
| train | 1er juillet 2015 → 21 avril 2017 | 95 190 | 36,1 % |
| test | 22 avril 2017 → 31 août 2017 | 24 018 | 41,0 % |

On peut lire le découpage ainsi : le modèle est mis en service le 22 avril 2017. Il apprend sur les séjours dont l'issue est connue, puis prédit les arrivées suivantes.

## Le passé, rien que le passé

Pour l'historique d'un agent ou d'un pays (cours 1, slides 13 et 14), une réservation passée ne compte que si **son issue était connue** à la date de la nouvelle réservation. `fe_tp.donnees.historique_a_date` fait cette jointure à date avec `pd.merge_asof` sur la date de clôture. Le notebook 06 refait le même calcul en SQL, avec des fonctions de fenêtre, puis le sert avec un feature store.

## La contamination

Une statistique calculée sur **tout** le jeu avant le découpage contient un peu du test. Le notebook 02 le mesure avec un encodage par la cible : appris sur train + test, il fait gagner environ deux points d'AUC… qui n'existeront jamais en production.

La parade est toujours la même : un `Pipeline`, ajusté sur le train seulement (cours 2, slides 23 à 25).
