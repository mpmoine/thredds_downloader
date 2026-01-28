import pytest

from cmip.drs import CMIP6DRS
from cmip.filter import CMIP6Filter


class DummyConfig:
    def __init__(self):
        self.data = {
            "project": "CMIP6",
            "mip": "CMIP",
            "models": ["CNRM-ESM2-1"],
            "experiments": ["historical"],
            "members": ["r1i1p1f2"],
            "thredds": {"http_base": "", "catalog_url": ""},
            "output": {"wget_script": "download.sh"},
        }

    @property
    def variables(self):
        return {("tas", "Amon")}


def test_drs_parse_with_prefix():
    path = (
        "CNRM-WCRP-Data/CMIP6/CMIP/CNRM-CERFACS/CNRM-ESM2-1/"
        "historical/r1i1p1f2/Amon/tas/gr/latest/"
        "tas_Amon_CNRM-ESM2-1_historical_r1i1p1f2_gr_185001-201412.nc"
    )
    meta = CMIP6DRS.parse(path)
    assert meta["project"] == "CMIP6"
    assert meta["mip"] == "CMIP"
    assert meta["institution"] == "CNRM-CERFACS"
    assert meta["model"] == "CNRM-ESM2-1"
    assert meta["experiment"] == "historical"
    assert meta["member"] == "r1i1p1f2"
    assert meta["table"] == "Amon"
    assert meta["variable"] == "tas"


def test_drs_parse_without_prefix():
    path = (
        "CMIP6/CMIP/CNRM-CERFACS/CNRM-ESM2-1/"
        "historical/r1i1p1f2/Amon/tas/gr/latest/tas.nc"
    )
    meta = CMIP6DRS.parse(path)
    assert meta["project"] == "CMIP6"
    assert meta["model"] == "CNRM-ESM2-1"


def test_filter_match_with_prefix():
    cfg = DummyConfig()
    filt = CMIP6Filter(cfg)
    path = (
        "CNRM-WCRP-Data/CMIP6/CMIP/CNRM-CERFACS/CNRM-ESM2-1/"
        "historical/r1i1p1f2/Amon/tas/gr/latest/"
        "tas_Amon_CNRM-ESM2-1_historical_r1i1p1f2_gr_185001-201412.nc"
    )
    assert filt.match(path) is True


def test_filter_reject_wrong_variable():
    cfg = DummyConfig()
    filt = CMIP6Filter(cfg)
    path = (
        "CNRM-WCRP-Data/CMIP6/CMIP/CNRM-CERFACS/CNRM-ESM2-1/"
        "historical/r1i1p1f2/Amon/pr/gr/latest/pr_Amon.nc"
    )
    assert filt.match(path) is False
