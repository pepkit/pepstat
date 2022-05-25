import os
import pytest

from pepstat.pepstat import PEPIndexer


@pytest.fixture
def data_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

@pytest.fixture
def result_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "result_index.yaml")

@pytest.fixture(scope="module", autouse=True)
def pep_indxr():
    indxr = PEPIndexer()
    indxr.index(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"), "index.yaml")
    yield indxr