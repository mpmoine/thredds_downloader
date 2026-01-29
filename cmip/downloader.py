from pathlib import Path
import logging

# minimal logging configuration; will be ignored if the application
# already configures logging handlers
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class WgetDownloader:
    def __init__(self, http_base, output_script):
        self.http_base = http_base
        self.output_script = Path(output_script)

    def generate(self, paths):
        # Keep only entries that contain '/gr/files/' (strict: no fallback)
        write_paths = [p for p in paths if ('/gr/files/' in p) or p.startswith('gr/files/')]

        # Avoid writing duplicate URLs
        seen = set()
        # If no matching paths, write a small script with a warning comment
        if len(write_paths) == 0:
            with open(self.output_script, "w") as f:
                f.write("#!/bin/bash\n\n")
                f.write("# WARNING: no entries with '/gr/files/' were found; no downloads written.\n")
            self.output_script.chmod(0o755)
            logger.warning(f"Avertissement: aucun chemin '/gr/files/' trouvé — script wget \"{self.output_script}\" créé avec un avertissement.")
            return

        with open(self.output_script, "w") as f:
            f.write("#!/bin/bash\n\n")
            for p in write_paths:
                if p in seen:
                    continue
                seen.add(p)
                url = self.http_base + p
                f.write(f"wget -c {url}\n")

        self.output_script.chmod(0o755)


import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable


class HTTPDownloader:
    """Downloader HTTP en Python.

    Télécharge une liste d'objets ManifestEntry (voir `cmip.manifest.ManifestEntry`)
    et recrée l'arborescence DRS localement sous un répertoire de destination.

    - resume: support basique de reprise en utilisant des fichiers .part
    - workers: nombre de téléchargements concurrents
    """

    def __init__(self, workers: int = 4, chunk_size: int = 1024 * 1024, session=None):
        self.workers = workers
        self.chunk_size = chunk_size
        self.session = session or requests.Session()

    def _local_path(self, entry, dest_dir: str):
        # ManifestEntry already exposes DRS fields (project, mip, institution, ...)
        base = Path(dest_dir) / entry.project / entry.mip / entry.institution / entry.model / entry.experiment / entry.member / entry.table / entry.variable / entry.grid / entry.version
        base.mkdir(parents=True, exist_ok=True)
        return base / entry.filename

    def _download_one(self, entry, dest_dir: str, resume: bool = True):
        out_path = self._local_path(entry, dest_dir)
        part_path = out_path.with_suffix(out_path.suffix + ".part")

        # Si le fichier final existe, on considère le fichier déjà téléchargé
        if out_path.exists():
            return (entry, "skipped", out_path)

        headers = {}
        mode = "wb"
        if resume and part_path.exists():
            existing = part_path.stat().st_size
            if existing > 0:
                headers["Range"] = f"bytes={existing}-"
                mode = "ab"

        try:
            with self.session.get(entry.http_url, stream=True, headers=headers, timeout=60) as r:
                r.raise_for_status()
                # If server returns 200 for a Range request, we overwrite
                with open(part_path, mode) as f:
                    for chunk in r.iter_content(chunk_size=self.chunk_size):
                        if chunk:
                            f.write(chunk)
            # rename .part to final
            part_path.replace(out_path)
            return (entry, "downloaded", out_path)
        except Exception as e:
            return (entry, f"error: {e}", None)

    def download(self, entries: Iterable, dest_dir: str = "data", resume: bool = True):
        # Only download entries whose thredds_path contains '/gr/files/'
        entries_list = list(entries)
        filtered = [e for e in entries_list if ("/gr/files/" in e.thredds_path) or e.thredds_path.startswith("gr/files/")]

        if len(filtered) == 0:
            logger.warning("Avertissement: aucun chemin '/gr/files/' trouvé parmi les entrées fournies ; aucun fichier ne sera téléchargé.")
            return {"downloaded": 0, "skipped": 0, "error": 0}

        results = []
        with ThreadPoolExecutor(max_workers=self.workers) as ex:
            futures = {ex.submit(self._download_one, e, dest_dir, resume): e for e in filtered}
            for fut in as_completed(futures):
                res = fut.result()
                results.append(res)

        # résumé simple
        summary = {"downloaded": 0, "skipped": 0, "error": 0}
        for _, status, _ in results:
            if status == "downloaded":
                summary["downloaded"] += 1
            elif status == "skipped":
                summary["skipped"] += 1
            else:
                summary["error"] += 1

        return summary
