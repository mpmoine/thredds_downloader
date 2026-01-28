CMIP6 THREDDS downloader
=========================

Ce petit outil construit un index des datasets disponibles dans un catalogue THREDDS,
filtre les chemins selon une configuration utilisateur et génère un script `wget`
pour télécharger les fichiers sélectionnés.

Note sur les chemins THREDDS
----------------------------
Certains catalogues THREDDS préfixent les `urlPath` par un nom de collection ou
institution (par exemple `CNRM-WCRP-Data/CMIP6/...`). Le code prend désormais en
compte ce cas : il recherche dynamiquement la position du token `CMIP6` dans le
chemin et extrait les champs DRS en conséquence.

Si vous préférez contrôler explicitement ce comportement, vous pouvez
ajouter une clé (ex. `thredds.prefix_to_strip`) dans la configuration pour
indiquer un préfixe à ignorer lors du filtrage.

Usage rapide
-----------
1. Préparer un environnement virtuel Python et installer les dépendances :

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt   # si vous fournissez un fichier requirements
# ou: pip install pyyaml requests lxml
```

2. Générer le script wget en utilisant l'index existant :

```bash
.venv/bin/python -m cmip.cli config.yaml --index-file thredds_index.json
```

Tests
-----
Les tests unitaires utilisent `pytest`. Lancez `pytest` dans la racine du
projet pour exécuter la suite.

Licence
-------
Fichier temporaire de documentation.
