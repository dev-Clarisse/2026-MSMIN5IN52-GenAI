# Projet H1 : laboratoire red-team d'injection de prompt

Batterie reproductible d'attaques par injection de prompt contre un petit agent RAG outillé,
avec mesure de l'efficacité de deux défenses (D1, D2) et de leur coût en faux refus.

> Cadre éthique : les attaques visent uniquement notre propre agent. Les outils sont simulés,
> rien n'est envoyé et aucun système réel n'est touché.

Les choix communs (modèle, format des cas, règles de mesure) sont décrits dans [CONTRATS.md](CONTRATS.md).

## Installation
```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration
Copier `.env.example` en `.env` et renseigner : `MODEL_API_KEY`, `API_BASE_URL`, `MODEL_NAME`, `CANARI`.
Le fichier `.env` ne doit jamais être commité.

## Structure
```
agent/        agent cible (RAG, outils simulés, canari, traces, cache)
defenses/     D1 (séparation) et D2 (contrôle des outils)
cas/          attaques.json (50) et legitimes.json (30)
evaluation/   détection, métriques, script d'évaluation
resultats/    cache des traces, CSV et graphiques
tests/        tests unitaires (aucun appel API)
```

## Configurations comparées
| Configuration | Description |
|---|---|
| baseline | agent sans défense |
| D1 | séparation instructions / données : documents balisés, consigne de ne jamais leur obéir |
| D2 | contrôle des appels d'outils : liste blanche, destinataires autorisés, compte de l'utilisateur courant |
| D1+D2 | les deux défenses |

Corpus : 50 attaques en 5 classes (directe, indirecte, fuite, détournement, déguisement) et
30 requêtes légitimes. 10 attaques et 6 requêtes légitimes forment le jeu `dev`, utilisé pour
régler les défenses ; les autres forment le jeu `test`, réservé à la campagne finale.

## Tests
```bash
pytest
```
Les tests n'appellent jamais l'API (le modèle est remplacé par des traces inventées).

## Lancement de la campagne
```bash
python -m agent.campagne --cas cas/attaques.json cas/legitimes.json --jeu dev --dry-run   # nombre d'appels, sans rien dépenser
python -m agent.campagne --cas cas/attaques.json cas/legitimes.json --jeu dev             # réglage des défenses
python -m agent.campagne --cas cas/attaques.json cas/legitimes.json --jeu test --final    # campagne finale
python -m evaluation.evaluer --jeu test                                                   # mesures et graphiques
```
Sorties dans `resultats/` : `resultats.csv` (ASR et faux refus par configuration, intervalles
de confiance de Wilson à 95 %), `par_classe.csv`, `details.csv`, `a_verifier.csv`,
`asr_par_config.png`, `asr_par_classe.png`.

## Reproduction sans API
Toutes les réponses du modèle sont enregistrées dans `resultats/cache/`. Sans clé API :
```bash
python -m evaluation.evaluer --jeu test
```
recalcule toutes les mesures et les graphiques à partir du cache, sans aucun appel au modèle.

## Démonstration
1. Une attaque indirecte réussie sur la baseline, puis la même bloquée par D1 ou D2.
2. Tableau et graphiques de `resultats/`.

Plan B si l'API ou le réseau sont indisponibles : la démonstration rejoue les traces du cache
(`python -m evaluation.evaluer --jeu test`).

## Résultats
(à compléter après la campagne `test` : tableau de `resultats/resultats.csv`, graphiques et interprétation)

## Limites
- **Détection heuristique de la prise de contrôle** : un mot marqueur cité dans un refus peut être
  compté à tort ; les cas détectés sont listés dans `resultats/a_verifier.csv` et relus à la main.
- **Petit échantillon** : 40 attaques de test, d'où des intervalles de confiance larges.
- **Un seul modèle** testé (voir CONTRATS.md) : les résultats ne se généralisent pas automatiquement.
- **D2 ne protège que les actions** : une fuite vers un destinataire autorisé (cas `fui_10`) ou
  dans le texte de la réponse n'est pas bloquée.
- **Fuites encodées** (base64, acrostiche) non détectées automatiquement.

## Équipe et contributions
- @dev-Clarisse : agent cible (RAG, outils simulés, canari, traces, cache, campagne)
- @bbgeo1020 : défenses D1 et D2
- @leticiagaspar : corpus d'attaques et de requêtes légitimes, détection, évaluation

Un assistant IA (Claude, Anthropic) a été utilisé pendant le développement ; le code a été relu et validé par l'équipe.

## Hypothèses de conception et choix de la baseline
- **Vulnérabilité de la baseline** : Le prompt de base intègre le canari à protéger mais ne sépare pas explicitement les instructions système des données textuelles récupérées par le RAG. Ce choix volontaire simule un agent naïf classique, idéal pour mesurer l'impact réel des couches défensives (D1 et D2).
- **Complémentarité D1 / Baseline** : La défense D1 introduit explicitement le cloisonnement (ne jamais obéir aux instructions contenues dans les documents), créant un contraste mesurable entre la baseline vulnérable et le système durci.