class CMIP6DRS:
    @staticmethod
    def parse(path):
        parts = path.split("/")
        # Accept an optional leading collection/institution prefix in the
        # path (e.g. "CNRM-WCRP-Data/CMIP6/..."). Locate the project
        # index then map DRS fields relative to it.

        if len(parts) < 10:
            raise ValueError(f"Chemin DRS invalide: {path}")

        # find index where project (e.g. "CMIP6") appears
        # project is expected to be the value like "CMIP6" used in user config
        # but we don't have access to config here; be tolerant: if the path
        # looks like it starts with a collection name, we assume project is
        # at index 1 (common pattern). Otherwise project is at 0.
        if parts[0].startswith("CMIP"):
            base = 0
        else:
            base = 1 if len(parts) > 1 and parts[1].startswith("CMIP") else 0

        if len(parts) <= base + 9:
            raise ValueError(f"Chemin DRS invalide: {path}")

        return {
            "project": parts[base],
            "mip": parts[base + 1],
            "institution": parts[base + 2],
            "model": parts[base + 3],
            "experiment": parts[base + 4],
            "member": parts[base + 5],
            "table": parts[base + 6],
            "variable": parts[base + 7],
            "grid": parts[base + 8],
            "version": parts[base + 9],
            "filename": parts[-1],
        }
