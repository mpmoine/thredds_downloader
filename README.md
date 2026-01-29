CMIP6 THREDDS downloader
=========================

Cet outil construit un index des datasets disponibles dans un catalogue THREDDS,
filtre les chemins selon une configuration utilisateur et génère un script `wget`
pour télécharger les fichiers sélectionnés, ou, alternativement, télécharge directement les données (sans passer par un script wget)

## Guide d'utilisation

Si vous êtes très pressé, rendez-vous directement en section **6**, mais si vous voulez comprendre les étapes, la progression de 1 à 5 est indiquée et elle ne vous prendra pas tant de temps que ça...

Pour tester rapidement sur un simple exemple:

```bash
.venv/bin/python -m cmip.cli examples/config_example_cmip6.yaml --index-file examples/thredds_index_example_cmip6.json --download --dest-dir examples/output_cmip6  --workers 2
```

Pour exectuer cet exemple, vous n'avez qu'à faire l'étape 1, les étapes 2 et 3 ayant été préparées pour vous (sur un petit sous-catalogue CMIP6). La commande ci-dessus correpond à l'étape 4b (téléchargement direct par https-python). Si vous préférez la solution de téléchargement via wget (étape 4a) alors faire simplement:

```bash
.venv/bin/python -m cmip.cli examples/config_example_cmip6.yaml --index-file examples/thredds_index_example_cmip6.json
```

Puis: 

```bash
mv download_example_cmip6.sh examples/.
cd examples
./download_example_cmip6.sh
```

### 1 - Préparer un environnement virtuel Python et installer les dépendances

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Cette étape est à faire une fois pour toutes.

### 2 -  Préparer le fichier de configuration utilisateur

Dans le fichier ```config.yaml```, l'utilisateur fournit l'adresse du serveur Thredds qu'il souhaite interroger et précise sa demande de données (project, modeles, experiments, members, variable, tables) ainsi que le nom souhaité pour le script wget de téléchargement qui sera généré. Voici un exemple de fichier de configuration:

```yaml
project: CMIP6
mip: CMIP

models:
- CNRM-CM6-1
- CNRM-ESM2-1

experiments:
  - historical
  - piControl

members:
  - r1i1p1f2
  - r2i1p1f2

variables:
  - variable: tas
    table: Amon
  - variable: pr
    table: Amon

thredds:
  catalog_url: https://thredds-su.ipsl.fr/thredds/catalog/CNRM-WCRP-Data/CMIP6/catalog.xml
  #catalog_url: https://thredds-su.ipsl.fr/thredds/catalog/CNRM-WCRP-Data/CMIP6/CMIP/CNRM-CERFACS/CNRM-ESM2-1/historical/r1i1p1f2/catalog.xml
  http_base: https://thredds-su.ipsl.fr/thredds/fileServer/

output:
  wget_script: download_cmip6.sh
```

### 3 -  Construire l'index THREDDS la première fois (opération longue)

```bash
.venv/bin/python -m cmip.cli config.yaml --build-index --index-file thredds_index-cmip6.json
```
Ce que ça fait, c'est: interroger le catalogue distant, parcourrir les sous-catalogues et sauvegarder la liste des datasets dans `thredds_index_cmip6.json`.

Pour le téléchargement de données, 2 altrnatives sont proposées: générer un script wget que vous devrez exécuter (cf. **4a**) ou télécharger directement les données (cf. **4b**).

### 4a - Lancer la requête utilisateur et générer le script `wget` en utilisant l'index existant

```bash
.venv/bin/python -m cmip.cli config.yaml --index-file thredds_index_cmip6.json
```

Le script `download_cmip6.sh` sera généré et il suffira de l'exécuter. 

L'avantage de cette solution est qu'elle est simple, mais elle a comme incovénients de faire les téléchargements en séquentiels et de ne pas préserver l'arborescence DRS. 

### 4b - Lancer la requête utilisateur et télécharger directement

Ici une alternative à **4a** pour télécharger directement les données, tout en préservant l'arborescence DRS. 

```bash
.venv/bin/python -m cmip.cli config.yaml --index-file thredds_index_cmip6.json --download --dest-dir <DEST_DIR> --workers <WORKERS>
```
avec:
* `DEST_DIR` : le répertoire de destination (par défaut "data").
* `WORKERS` : le nombre de téléchargements concurrents (par défaut 4).

Un autre avantage de cette solution, en plus de la préservation de la DRS, est la possibilité de lancer les téléchargements en parallèle.


### 6 - Pour se simplifier la vie, le Makefile

Un `Makefile` est fourni pour simplifier les étapes courantes. Les cibles principales correspondent aux commandes Python équivalentes décrites précédemment:

- `make venv` : crée l'environnement virtuel `.venv` et met à jour pip.
- `make install` : installe les dépendances (équivalent à `pip install -r requirements.txt`).
- `make build-index` : construit l'index THREDDS (équivalent à `python -m cmip.cli --build-index ...`).
- `make generate` : génère le script wget de téléchargement (arborescence non préservée)
- `make download`: lance le téléchargement des données en parallèle (arboresence préservée)
- `make test` : exécute la suite de tests (`pytest`).
- `make run` : exécute le script `download_cmip6.sh` généré.

Vous pouvez continuer à utiliser directement les commandes Python si vous préférez, mais `make` regroupe les étapes et garantit l'usage du virtualenv `.venv` défini par le projet.


## Le coin des développeurs...

- Notes:
    - L'index local est pour l'instantlisté dans `.gitignore` afin de ne pas le versionner -> penser à le sortir du gitignore pour le mettre sur le repo et le fournir aux utilisateurs.
    - Si le catalogue THREDDS ajoute un préfixe (ex. `CNRM-WCRP-Data/CMIP6/...`), l'outil détecte automatiquement la position du token `CMIP6` et filtre
  correctement les chemins. Il sera possible d'ajouter plus tard une option de config pour un préfixe explicite si besoin (`thredds.prefix_to_strip`).
    - Les tests unitaires utilisent `pytest`; les tests  fournis couvrent le parsing DRS et le filtrage avec/sans préfixe. Pour lancer la suite de tests :

```bash
.venv/bin/python -m pytest -q
```

- Améliorations possibles:
    - Couvrir d'autres formats d'index comme CORDEX; pour cel il faut améliorer la détection de préfixes (chercher dynamiquement le token project dans la config ou permettre un champ thredds.prefix_to_strip).
    - Optionnel : normaliser les chemins lors de la construction de l'index (supprimer automatiquement un préfixe connu), plutôt que de rendre chaque composant tolérant.
    - Ajouter une option de logging détaillé (--debug) qui imprime quelques exemples de chemins rejetés et pourquoi.

