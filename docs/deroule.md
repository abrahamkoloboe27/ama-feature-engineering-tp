# Déroulé de la séance (3 h)

Les notebooks sont **déjà exécutés** : on les lit, on commente les sorties et on discute les questions 💬. On ne relance en direct que les cellules légères. Les cellules d'évaluation des cinq modèles prennent de 1 à 4 minutes chacune.

| Début | Durée | Notebook | Ce qu'il faut faire passer |
|---|---|---|---|
| 0:00 | 10 min | accueil | la question (annulation au moment de la réservation), les données, le principe : seule la préparation change |
| 0:10 | 25 min | 00 · cadrer | la question réflexe des fuites, le découpage dans le temps, « le hasard flatte », le score à battre |
| 0:35 | 20 min | 01 · A | classer avant de transformer, le piège de `get_dummies`, la colonne « autres » ; le score de référence |
| 0:55 | 45 min | 02 · B | **le cœur** : une variable = une hypothèse ; le passé, rien que le passé (taux « sur toute la période » contre « à date ») ; la contamination mesurée |
| 1:40 | 10 min | pause | |
| 1:50 | 30 min | 03 · C | la combinatoire des interactions, l'ACP qui fait perdre, le piège de la sélection avant validation, la L1 |
| 2:20 | 15 min | 04 · D | numéroter, c'est inventer un ordre ; les arbres ignorent l'échelle ; le support natif |
| 2:35 | 20 min | 05 · comparer | le tableau croisé, lu famille par famille ; la fiche réflexe ; le modèle face à un pays inconnu |
| 2:55 | 5 min | clôture | les quatre leçons de la page [Résultats](resultats.md) |

**Le notebook 06 (Feast)** est optionnel. S'il reste du temps, ou pour une séance d'approfondissement, comptez 25 minutes. Pour le caser dans les 3 h, raccourcissez le 03 (sautez le wrapper et l'information mutuelle) et le 04 (sautez l'importance par permutation).

## Avant la séance

- [ ] `uv sync` sur le poste de démonstration, puis `uv run jupyter lab`.
- [ ] Ouvrir les notebooks dans le navigateur à l'avance ; garder ce site ouvert en secours.
- [ ] Projeter la [fiche réflexe](resultats.md) à la fin du 05.

## Pièges à annoncer

- `pd.get_dummies` sur le train et sur le test ne donne pas les mêmes colonnes (notebook 01).
- `TargetEncoder.fit_transform(X, y)` n'est pas `fit(X, y).transform(X)` : c'est voulu, à cause de la validation croisée interne (notebook 02).
- `OrdinalEncoder` range les mois par ordre alphabétique : *April* = 0, *August* = 1 (notebook 04).
- Feast tourne sous pandas 2, d'où pandas 2.3 dans tout le TD (page [Installer](installation.md)).
