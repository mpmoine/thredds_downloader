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
pip install -r requirements.txt
```

Makefile
-------
Un `Makefile` est fourni pour simplifier les étapes courantes. Les cibles
principales correspondent aux commandes Python équivalentes ci-dessus :

- `make venv` : crée l'environnement virtuel `.venv` et met à jour pip.
- `make install` : installe les dépendances (équivalent à `pip install -r requirements.txt`).
- `make build-index` : construit l'index THREDDS (équivalent à `python -m cmip.cli --build-index ...`).
- `make generate` : génère le script wget à partir de l'index local.
- `make test` : exécute la suite de tests (`pytest`).
- `make run` : exécute le script `download_cmip6.sh` généré.

Vous pouvez continuer à utiliser directement les commandes Python si
vous préférez, mais `make` regroupe les étapes et garantit l'usage du
virtualenv `.venv` défini par le projet.
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

Exemple d'utilisation complète
------------------------------
Ci-dessous un exemple pas-à-pas — supposons que vous êtes dans la racine du
projet et que `config.yaml` contient vos choix (exemples: `project: CMIP6`,
`variables: - variable: tas / table: Amon`, etc.).

1) Créer l'environnement et installer les dépendances:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Construire l'index THREDDS la première fois (opération longue):

```bash
.venv/bin/python -m cmip.cli config.yaml --build-index --index-file thredds_index.json
# Ce qui fait : interroger le catalogue distant, parcourir les sous-catalogues
# et sauvegarder la liste des datasets dans `thredds_index.json`.
```

3) Lancer la requête utilisateur (filtrage local à partir de l'index) et
générer le script `wget`:

```bash
.venv/bin/python -m cmip.cli config.yaml --index-file thredds_index.json
# Le script (par défaut `download_cmip6.sh`) sera généré et rendu exécutable.
```

4) Vérifier puis exécuter le script `wget` pour démarrer les téléchargements:

```bash
less download_cmip6.sh   # vérifier les URLs
bash download_cmip6.sh   # ou sh download_cmip6.sh
```

Remarques pratiques
-------------------
- Si vous ne voulez pas versionner l'index local, il est listé dans `.gitignore`.
- Si votre catalogue THREDDS ajoute un préfixe (ex. `CNRM-WCRP-Data/CMIP6/...`),
  l'outil détecte automatiquement la position du token `CMIP6` et filtre
  correctement les chemins. Vous pouvez aussi ajouter une option de config
  pour un préfixe explicite si besoin (`thredds.prefix_to_strip`).

Support & tests
---------------
Les tests unitaires fournis couvrent le parsing DRS et le filtrage avec/sans
préfixe. Pour lancer la suite de tests :

```bash
.venv/bin/python -m pytest -q
```

