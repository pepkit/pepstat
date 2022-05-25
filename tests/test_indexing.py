import os
from unittest import result
import pytest
from pepstat import PEPIndexer

class TestIndexing:

    @pytest.mark.parametrize("namespace", [".test_namespace", "some/random/path"])
    def test_invalid_namespace(self, namespace):
        indxr = PEPIndexer()
        assert not indxr._is_valid_namespace(namespace)
    
    @pytest.mark.parametrize("project", [".project", "some/random/path"])
    def test_invalid_project(self, project):
        indxr = PEPIndexer()
        assert not indxr._is_valid_project(project)
    
    def test_indexing(self, data_path, result_path):
        indxr = PEPIndexer()
        indxr.index(data_path, result_path)

        assert os.path.exists(result_path)
    
    def test_read_index(self, data_path):
        indxr = PEPIndexer()
        indxr.load_index(f"{data_path}/index.yaml")

        assert isinstance(indxr.get_index(), dict)
    
