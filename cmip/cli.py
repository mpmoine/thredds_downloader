import argparse

from cmip.config import CMIPConfig
from cmip.catalog import ThreddsCatalog
from cmip.filter import CMIP6Filter
from cmip.downloader import WgetDownloader
from cmip.manifest import ManifestWriter
from cmip.index import DatasetIndex

def main():
    parser = argparse.ArgumentParser(
        description="CMIP6 THREDDS downloader (wget generator)"
    )
    parser.add_argument("config", help="Fichier YAML de configuration")
    parser.add_argument("--manifest-csv", help="Manifeste CSV")
    parser.add_argument("--manifest-yaml", help="Manifeste YAML")
    parser.add_argument("--build-index", action="store_true",
                    help="Reconstruire l'index local du catalogue THREDDS")
    parser.add_argument("--index-file", default="thredds_index.json",
                    help="Fichier d'index local")

    args = parser.parse_args()

    # Chargement de la configuration utilisateur
    cfg = CMIPConfig(args.config)

    # Récupération de la liste des datasets disponibles sur le THREDDS catalog
    catalog = ThreddsCatalog(cfg.data["thredds"]["catalog_url"])
    index = DatasetIndex(args.index_file)
    if args.build_index or not index.exists():
        print("Construction de l'index THREDDS (opération longue)...")
        datasets = catalog.list_datasets()
        index.write(cfg.data["thredds"]["catalog_url"], datasets)
    else:
        print("Chargement de l'index THREDDS local")
        datasets = index.read()
    print(f"{len(datasets)} fichiers disponibles dans le catalogue THREDDS")

    # Filtrage des datasets selon les choix faits par l'utilisateur
    filt = CMIP6Filter(cfg)
    selected = [p for p in datasets if filt.match(p)]
    print(f"{len(selected)} fichiers sélectionnés")

    # Génération du manifeste
    writer = ManifestWriter(cfg.data["thredds"]["http_base"])
    entries = writer.build_entries(selected)

    if(len(entries) == 0):
        print("Aucun fichier ne correspond aux critères spécifiés dans la configuration.")
        return

    if args.manifest_csv:
        writer.to_csv(entries, args.manifest_csv)

    if args.manifest_yaml:
        writer.to_yaml(entries, args.manifest_yaml)

    # Génération du script wget
    downloader = WgetDownloader(
        cfg.data["thredds"]["http_base"],
        cfg.data["output"]["wget_script"]
    )
    downloader.generate(selected)

    print(f"Script wget généré : {cfg.data['output']['wget_script']}")

if __name__ == "__main__":
    main()
