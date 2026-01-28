from pathlib import Path

class WgetDownloader:
    def __init__(self, http_base, output_script):
        self.http_base = http_base
        self.output_script = Path(output_script)

    def generate(self, paths):
        with open(self.output_script, "w") as f:
            f.write("#!/bin/bash\n\n")
            for p in paths:
                url = self.http_base + p
                f.write(f"wget -c {url}\n")

        self.output_script.chmod(0o755)
