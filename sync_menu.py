#!/usr/bin/env python3
"""Génère menu.json à partir de la page HTML de l'artefact « Menu de la Semaine ».

Usage : python3 sync_menu.py FICHIER_HTML_DU_MENU
Le fichier contient un bloc <script type="application/json" id="appStateData"> avec les semaines.
Ne garde que les semaines commençant au plus tôt 21 jours avant aujourd'hui.
menu.json n'est réécrit que si son contenu a changé (la date « maj » est ignorée).
Affiche CHANGED ou UNCHANGED.
"""
import json, os, re, sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

SRC = sys.argv[1]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "menu.json")
html = open(SRC, encoding="utf8").read()
m = re.search(r'<script type="application/json" id="appStateData">(.*?)</script>', html, re.S)
if not m:
    sys.exit("Données du menu introuvables : menu.json non modifié.")
etat = json.loads(m.group(1))
coupe = (datetime.now(ZoneInfo("Europe/Paris")) - timedelta(days=21)).strftime("%Y-%m-%d")
semaines, menus = [], {}
for wk, w in sorted(etat["weeks"].items()):
    if wk < coupe:
        continue
    semaines.append(wk)
    for d, r in w["meals"].items():
        x = {"m": [r["midi"]["entree"], r["midi"]["plat"]], "s": [r["soir"]["entree"], r["soir"]["plat"]]}
        if any(x["m"] + x["s"]):
            menus[d] = x
if not semaines:
    sys.exit("Aucune semaine récente : menu.json non modifié.")

new = {"semaines": semaines, "menus": menus}
old = {}
if os.path.exists(OUT):
    old = json.load(open(OUT, encoding="utf8")); old.pop("maj", None)
if old == new:
    print("UNCHANGED")
else:
    new = {"maj": datetime.now(ZoneInfo("Europe/Paris")).isoformat(timespec="minutes"), **new}
    json.dump(new, open(OUT, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    print("CHANGED")
