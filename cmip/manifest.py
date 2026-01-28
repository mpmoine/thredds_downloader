from dataclasses import dataclass
from pathlib import Path
import csv
import yaml
from cmip.drs import CMIP6DRS
#from cmip.manifest import ManifestEntry

@dataclass
class ManifestEntry:
    project: str
    mip: str
    institution: str
    model: str
    experiment: str
    member: str
    table: str
    variable: str
    grid: str
    version: str
    filename: str
    thredds_path: str
    http_url: str

class ManifestWriter:
    def __init__(self, http_base):
        self.http_base = http_base

    def build_entries(self, paths):
        entries = []
        for p in paths:
            meta = CMIP6DRS.parse(p)
            entries.append(
                ManifestEntry(
                    **meta,
                    thredds_path=p,
                    http_url=self.http_base + p,
                )
            )
        return entries

    def to_csv(self, entries, filename):
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=entries[0].__dict__.keys()
            )
            writer.writeheader()
            for e in entries:
                writer.writerow(e.__dict__)

    def to_yaml(self, entries, filename):
        with open(filename, "w") as f:
            yaml.safe_dump(
                [e.__dict__ for e in entries],
                f,
                sort_keys=False
            )
 
