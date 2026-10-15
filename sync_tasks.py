#!/usr/bin/env python3
"""Génère tasks.json à partir d'un export du Carnet Idem.

Usage : python3 sync_tasks.py DOSSIER_EXPORT
DOSSIER_EXPORT contient tasks/*.json et categories/*.json (documents de la base du Carnet).
Le fichier tasks.json n'est réécrit que si son contenu a changé (la date « maj » est ignorée).
Affiche CHANGED ou UNCHANGED.
"""
import glob, json, os, sys
from datetime import datetime
from zoneinfo import ZoneInfo

SRC = sys.argv[1]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")
COULEURS = {"Perso": "#c0709a", "Pro": "#4f8bd0", "Internet": "#3aa58c", "Domiciliation": "#d99a2b",
            "Comptabilité": "#8a7bd6", "Marketing": "#e07a4b", "Laverie": "#4aa3b5"}
EXCLURE = set()  # ex. {"perso"} pour ne pas publier une catégorie

def slug(n):
    return {"Comptabilité": "compta", "Domiciliation": "domic"}.get(n, n.lower())

cats, cat_key = {}, {}
for f in glob.glob(os.path.join(SRC, "categories", "*.json")):
    c = json.load(open(f, encoding="utf8"))
    cat_key[c["id"]] = slug(c["name"])
    cats[slug(c["name"])] = {"n": c["name"], "c": COULEURS.get(c["name"], "#7c8a84")}

taches = []
for f in sorted(glob.glob(os.path.join(SRC, "tasks", "*.json"))):
    t = json.load(open(f, encoding="utf8"))
    if t.get("archived"):
        continue
    k = cat_key.get(t.get("categoryId"), "pro")
    if k in EXCLURE:
        continue
    o = {"i": t["id"][:8], "t": t["title"].replace("déclarion", "déclaration").replace("SIte", "Site"),
         "k": k, "f": t["frequency"]}
    if t["frequency"] == "single":
        o["due"] = t.get("dueDate")
        if t.get("done"): o["d"] = 1
        o["p"] = t.get("progress") or 0
    elif t["frequency"] == "weekly":
        o["wd"] = t.get("dueWeekday") or 0
    elif t["frequency"] == "monthly":
        r = t["monthlyRule"]; o["n"] = r["nth"]; o["wd"] = r["weekday"]
    elif t["frequency"] == "quarterly":
        r = t["quarterlyRule"]; o["mo"] = r.get("monthOffset", 0); o["n"] = r["nth"]; o["wd"] = r["weekday"]
    if t["frequency"] != "single":
        o["c"] = sorted(d for d, v in (t.get("completions") or {}).items() if v)
    if t.get("priority"): o["pr"] = 1
    taches.append(o)

if not taches:
    sys.exit("Aucune tâche trouvée : export vide, tasks.json non modifié.")

new = {"cats": cats, "taches": taches}
old = {}
if os.path.exists(OUT):
    old = json.load(open(OUT, encoding="utf8")); old.pop("maj", None)
if old == new:
    print("UNCHANGED")
else:
    new = {"maj": datetime.now(ZoneInfo("Europe/Paris")).isoformat(timespec="minutes"), **new}
    json.dump(new, open(OUT, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    print("CHANGED")
