import os
from unittest import result
from peppy import Project
from pepstat import PEPIndexer


class TestPOPCreation:
    def test_create_pop(self, data_path):
        TOT_PEPS = 176
        indxr = PEPIndexer()
        indxr.generate_pop(
            data_path,
            "pop.yaml",
            "peps.csv"
        )
        p = Project("pop.yaml")
        assert len(p.samples) == TOT_PEPS