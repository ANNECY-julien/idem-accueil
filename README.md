# idem-accueil

Données publiques de la page d'accueil Idem.

- `tasks.json` : copie des tâches du Carnet Idem, lue par la page d'accueil toutes les 10 minutes.
- `menu.json` : copie du menu de la semaine (semaines du vendredi au jeudi), lue par la page d'accueil toutes les 10 minutes.
- `sync_menu.py` : régénère `menu.json` à partir de la page HTML de l'artefact « Menu de la Semaine ».
- `sync_tasks.py` : régénère `tasks.json` à partir d'un export du Carnet (voir l'en-tête du script).

Le fichier est public : n'y mettre que des intitulés de tâches dont la publication ne pose pas de problème.
