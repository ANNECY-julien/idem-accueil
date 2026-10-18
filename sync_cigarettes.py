#!/usr/bin/env python3
"""Génère cigarettes.json (nombre de cigarettes par jour) à partir d'un export du Carnet Idem.

Usage : python3 sync_cigarettes.py DOSSIER_EXPORT
DOSSIER_EXPORT contient entries/*.json (documents « entries » de la base du Carnet).
Seul l'indicateur « cigarettes » est publié (ni poids, ni pas).
Le fichier n'est réécrit que si son contenu a changé (la date « maj » est ignorée).
Affiche CHANGED ou UNCHANGED.
"""
import glob, json, os, sys
from datetime import datetime
from zoneinfo import ZoneInfo

SRC = sys.argv[1]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cigarettes.json")
# mêmes réglages que le Carnet Idem : départ du suivi, consommation d'avant par jour, prix d'une cigarette
DEPART, BASE, PRIX = "2026-09-09", 30, 0.56

jours = {}
for f in sorted(glob.glob(os.path.join(SRC, "entries", "*.json"))):
    e = json.load(open(f, encoding="utf8"))
    e = e.get("data", e)
    n = (e.get("values") or {}).get("cigarettes")
    if isinstance(n, (int, float)) and e.get("date", "") >= DEPART:
        jours[e["date"]] = n
if not jours:
    sys.exit("Aucune saisie de cigarettes trouvée : cigarettes.json non modifié.")

new = {"depart": DEPART, "base": BASE, "prix": PRIX, "jours": jours}
old = {}
if os.path.exists(OUT):
    old = json.load(open(OUT, encoding="utf8")); old.pop("maj", None)
if old == new:
    print("UNCHANGED")
else:
    new = {"maj": datetime.now(ZoneInfo("Europe/Paris")).isoformat(timespec="minutes"), **new}
    json.dump(new, open(OUT, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    print("CHANGED")
