import os
import pytest

@pytest.fixture
def data_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

@pytest.fixture
def result_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "result_index.yaml")