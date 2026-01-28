.PHONY: all venv install build-index generate test run clean help

PY=.venv/bin/python
PIP=.venv/bin/pip

# variables for download target (can be overridden on the make command line)
DEST_DIR ?= data
WORKERS ?= 4

all: install

venv:
	python3 -m venv .venv
	$(PY) -m pip install --upgrade pip

install: venv
	$(PIP) install -r requirements.txt

build-index:
	$(PY) -m cmip.cli config.yaml --build-index --index-file thredds_index.json

generate:
	$(PY) -m cmip.cli config.yaml --index-file thredds_index.json

test:
	$(PY) -m pytest -q

download:
	$(PY) -m cmip.cli config.yaml --index-file thredds_index.json --download --dest-dir $(DEST_DIR) --workers $(WORKERS)

run:
	@if [ -f download_cmip6.sh ]; then \
		bash download_cmip6.sh; \
	else \
		echo "download_cmip6.sh not found — run 'make generate' first"; \
	fi

clean:
	rm -rf .venv
	rm -f download_cmip6.sh thredds_index.json

help:
	@echo "Makefile targets:"
	@echo "  make venv         -> create virtualenv and upgrade pip"
	@echo "  make install      -> install dependencies from requirements.txt"
	@echo "  make build-index  -> build thredds index (first time, network)"
	@echo "  make generate     -> filter using local index and generate wget script (does not preserve the tree directory structure)"
	@echo "  make download     -> download files using Python downloader (preserve the tree directory structure)"
	@echo "  make test         -> run pytest"
	@echo "  make run          -> execute generated download script (download_cmip6.sh)"
	@echo "  make clean        -> remove .venv and generated files"
