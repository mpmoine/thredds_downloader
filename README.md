CMIP6 THREDDS downloader
=========================

This tool builds an index of datasets available in a THREDDS catalog, filters the paths according to a user configuration, and either generates a `wget` script to download the selected files or downloads the data directly using HTTP (without generating a `wget` script).

## Usage guide

If you are in a hurry, skip to section **6**. Otherwise follow steps 1–5 — it won't take long and you'll understand how things work.

Quick example run:

```bash
.venv/bin/python -m cmip.cli examples/config_example_cmip6.yaml --index-file examples/thredds_index_example_cmip6.json --download --dest-dir examples/output_cmip6  --workers 2
```
```bash
.venv/bin/python -m cmip.cli examples/config_example_cmip6.yaml --index-file examples/thredds_index_example_cmip6.json
```

Then:

```bash
mv download_example_cmip6.sh examples/.
cd examples
./download_example_cmip6.sh
```

### 1 - Prepare a Python virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Do this once per machine.

### 2 - Prepare the user configuration file

In `config.yaml` the user provides the THREDDS server address to query and specifies the data request (project, models, experiments, members, variables, tables) as well as the desired name for the generated `wget` download script. Example configuration:

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

### 3 - Build the THREDDS index for the first time (long operation)

```bash
.venv/bin/python -m cmip.cli config.yaml --build-index --index-file thredds_index-cmip6.json
```

This queries the remote catalog, walks sub-catalogs and saves the dataset list to `thredds_index_cmip6.json`.

For downloading data there are two alternatives: generate a `wget` script to run manually (see **4a**) or download the data directly from Python (see **4b**).

### 4a - Generate a `wget` script using the existing index

```bash
.venv/bin/python -m cmip.cli config.yaml --index-file thredds_index_cmip6.json
```

This generates the `download_cmip6.sh` script which you can run.

The advantage is simplicity; drawbacks are that downloads are sequential and the DRS directory structure is not preserved.

### 4b - Query and download directly

This alternative downloads the data directly while preserving the DRS directory structure.

```bash
.venv/bin/python -m cmip.cli config.yaml --index-file thredds_index_cmip6.json --download --dest-dir <DEST_DIR> --workers <WORKERS>
```
where:
* `DEST_DIR` : destination directory (default: `data`).
* `WORKERS` : number of concurrent downloads (default: 4).

An additional advantage of this approach is the ability to run downloads in parallel while keeping the DRS layout.


### 6 - Use the Makefile to simplify common tasks

A `Makefile` is provided to simplify common steps. Primary targets map to the equivalent Python commands described above:

- `make venv` : create the `.venv` virtual environment and update pip.
- `make install` : install dependencies (equivalent to `pip install -r requirements.txt`).
- `make build-index` : build the THREDDS index (equivalent to `python -m cmip.cli --build-index ...`).
- `make generate` : generate the wget download script (does not preserve directory tree).
- `make download`: run parallel downloads preserving the DRS tree.
- `make test` : run the test suite (`pytest`).
- `make run` : execute the generated `download_cmip6.sh` script.

You can still use the Python commands directly if you prefer; `make` simply bundles steps and ensures the project virtualenv `.venv` is used.


## Developer notes

- Notes:
    - The local index is currently listed in `.gitignore` to avoid versioning; consider removing it from `.gitignore` and placing it in the repository if you want to ship a pre-built index to users.
    - If the THREDDS catalog adds a prefix (e.g. `CNRM-WCRP-Data/CMIP6/...`), the tool automatically detects the position of the `CMIP6` token and correctly filters paths. In the future we may add a configuration option to explicitly strip a prefix (`thredds.prefix_to_strip`).
    - Unit tests use `pytest`; provided tests cover DRS parsing and filtering with/without a prefix. To run the test suite:

```bash
.venv/bin/python -m pytest -q
```

- Possible improvements:
    - Support other index formats such as CORDEX; this requires improving prefix detection (dynamically searching for the project token in the config or allowing a `thredds.prefix_to_strip` field).
    - Optionally normalize paths when building the index (automatically remove a known prefix) instead of making each component tolerant.
    - Add a detailed logging option (`--debug`) that prints examples of rejected paths and the reasons why.


````

