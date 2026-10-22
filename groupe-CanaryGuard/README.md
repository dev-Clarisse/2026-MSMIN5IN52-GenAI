# Projet H1 : laboratoire red-team d'injection de prompt

Batterie reproductible d'attaques par injection de prompt contre un petit agent RAG outillé,
avec mesure de l'efficacité de deux défenses (D1, D2) et de leur coût en faux refus.

> Cadre éthique : les attaques visent uniquement notre propre agent. Les outils sont simulés,
> rien n'est envoyé et aucun système réel n'est touché.

## Installation
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt

## Configuration
Copier `.env.example` en `.env` et renseigner : API_KEY, API_BASE_URL, MODEL_NAME, CANARI.
Le fichier `.env` ne doit jamais être commité.

## Structure
agent/        agent cible (RAG, outils simulés, canari, traces, cache)
defenses/     D1 (séparation) et D2 (contrôle des outils)
cas/          attaques.json (50) et legitimes.json (30)
evaluation/   détection, métriques, script d'évaluation
resultats/    cache des traces, resultats.csv, graphiques
rapport/      rapport final

## Lancement
(à compléter samedi : commande de la campagne)

## Reproduction sans API
(à compléter dimanche : rejouer les résultats depuis resultats/cache/)

## Équipe
Clarisse (agent cible), Georgette (défenses), Leticia (attaques et évaluation)