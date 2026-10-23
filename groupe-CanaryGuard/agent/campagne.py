import argparse
import json
from pathlib import Path

from agent.executer import chemin_cache, empreinte, executer
from agent.trace import charger_trace

CONFIGS = [
    {"d1": False, "d2": False},
    {"d1": True, "d2": False},
    {"d1": False, "d2": True},
    {"d1": True, "d2": True},
]


def etiquette(config: dict) -> str:
    return {(False, False): "baseline", (True, False): "D1",
            (False, True): "D2", (True, True): "D1+D2"}[(config["d1"], config["d2"])]


def defenses_disponibles(config: dict) -> bool:
    try:
        if config["d1"]:
            import defenses.d1_separation  # noqa: F401
        if config["d2"]:
            import defenses.d2_outils  # noqa: F401
    except ImportError:
        return False
    return True


def en_cache(cas: dict, config: dict) -> bool:
    chemin = chemin_cache(cas, config)
    if not chemin.exists():
        return False
    return charger_trace(chemin).get("_cle") == empreinte(cas, config)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--cas", nargs="+", required=True, help="fichiers JSON de cas")
    p.add_argument("--jeu", choices=["dev", "test", "tous"], default="dev")
    p.add_argument("--dry-run", action="store_true", help="compte les appels API sans les faire")
    p.add_argument("--force", action="store_true")
    args = p.parse_args()

    cas_list = []
    for f in args.cas:
        cas_list += json.loads(Path(f).read_text(encoding="utf-8"))
    if args.jeu != "tous":
        cas_list = [c for c in cas_list if c["jeu"] == args.jeu]

    a_jouer = 0
    for config in CONFIGS:
        if not defenses_disponibles(config):
            print(f"[{etiquette(config)}] défenses pas encore disponibles : ignorée")
            continue
        for cas in cas_list:
            if not args.force and en_cache(cas, config):
                continue
            a_jouer += 1
            if args.dry_run:
                continue
            try:
                t = executer(cas, config, force=args.force)
                print(f"[{etiquette(config)}] {cas['id']}: {t['tokens']} tokens, {t['latence_ms']} ms")
            except Exception as e:  # on continue la campagne
                print(f"[{etiquette(config)}] {cas['id']}: ERREUR {e}")
    print(f"{'À jouer' if args.dry_run else 'Joués'} : {a_jouer} appels d'agent")


if __name__ == "__main__":
    main()