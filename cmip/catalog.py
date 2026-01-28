import requests
from lxml import etree
from urllib.parse import urljoin

class ThreddsCatalog:
    NS = {
        "t": "http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0",
        "xlink": "http://www.w3.org/1999/xlink",
    }

    def __init__(self, catalog_url):
        self.catalog_url = catalog_url
        self._visited = set()

    def list_datasets(self):
        return self._walk_catalog(self.catalog_url)

    def _walk_catalog(self, url):
        if url in self._visited:
            return []

        self._visited.add(url)

        r = requests.get(url)
        r.raise_for_status()

        root = etree.fromstring(r.content)

        datasets = []

        # 1) datasets terminaux
        for ds in root.findall(".//t:dataset[@urlPath]", self.NS):
            datasets.append(ds.attrib["urlPath"])

        # 2) sous-catalogues
        for cref in root.findall(".//t:catalogRef", self.NS):
            href = cref.attrib.get("{http://www.w3.org/1999/xlink}href")
            if href:
                sub_url = urljoin(url, href)
                datasets.extend(self._walk_catalog(sub_url))

        return datasets

