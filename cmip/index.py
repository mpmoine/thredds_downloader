import json
from datetime import datetime
from pathlib import Path

class DatasetIndex:
    def __init__(self, index_path):
        self.path = Path(index_path)

    def exists(self):
        return self.path.exists()

    def write(self, catalog_url, datasets):
        payload = {
            "catalog_url": catalog_url,
            "generated": f"{datetime.utcnow().isoformat()}Z",
            "datasets": sorted(set(datasets)),
        }
        with open(self.path, "w") as f:
            json.dump(payload, f, indent=2)

    def read(self):
        with open(self.path) as f:
            payload = json.load(f)
        return payload["datasets"]
