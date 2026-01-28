import yaml
from pathlib import Path

class CMIPConfig:
    def __init__(self, path):
        self.path = Path(path)
        self.data = self._load()

    def _load(self):
        with open(self.path) as f:
            data = yaml.safe_load(f)

        required = ["project", "mip", "models", "experiments", "members", "variables"]
        for key in required:
            if key not in data:
                raise ValueError(f"Champ manquant dans la config: {key}")

        return data

    @property
    def variables(self):
        return {
            (v["variable"], v["table"])
            for v in self.data["variables"]
        }
