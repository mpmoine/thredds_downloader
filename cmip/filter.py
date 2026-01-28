class CMIP6Filter:
    def __init__(self, config):
        self.cfg = config

    def match(self, path):
        parts = path.split("/")
        # Some THREDDS indexes include a leading collection/institution
        # prefix (e.g. "CNRM-WCRP-Data/CMIP6/..."). Locate where the
        # project (e.g. "CMIP6") appears and use that as the base
        # offset. This makes the filter tolerant to an optional prefix.

        if len(parts) < 8:
            return False

        # find index where project appears
        try:
            base = parts.index(self.cfg.data["project"])
        except ValueError:
            # project not found in path
            return False

        # need at least project + mip + institution + model + experiment + member + table + variable
        if len(parts) <= base + 7:
            return False

        project = parts[base]
        mip = parts[base + 1]
        model = parts[base + 3]
        experiment = parts[base + 4]
        member = parts[base + 5]
        table = parts[base + 6]
        variable = parts[base + 7]

        if project != self.cfg.data["project"]:
            return False
        if mip != self.cfg.data["mip"]:
            return False
        if model not in self.cfg.data["models"]:
            return False
        if experiment not in self.cfg.data["experiments"]:
            return False
        if member not in self.cfg.data["members"]:
            return False
        if (variable, table) not in self.cfg.variables:
            return False

        return True
