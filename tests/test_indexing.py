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

    def test_index_complete(self, pep_indxr):
        assert isinstance(pep_indxr, dict)

    @pytest.mark.parametrize("namespace", [
        # ground truths below.
        {
            'name': 'changlab',
            'nprojects': 2
        }, 
        {
            'name': 'demo',
            'nprojects': 24
        },
        {
            'name': 'geo',
            'nprojects': 150
        }
    ])
    def test_index_success(self, pep_indxr, namespace):
        assert len(pep_indxr.get_projects(namespace['name'])) == namespace['nprojects']
    
<<<<<<< HEAD
    def test_read_index(self, data_path):
        indxr = PEPIndexer()
        indxr.load_index(f"{data_path}/index.yaml")

        assert isinstance(indxr.get_index(), dict)
    
=======
    def test_get_namespaces(self, pep_indxr):
        valid_nspaces = [
            "demo", "changlab", "geo"
        ]
        assert all(
            nspace in pep_indxr.get_namespaces() for nspace in valid_nspaces
        )
        assert len(valid_nspaces) == len(pep_indxr.get_namespaces())
>>>>>>> refs/remotes/origin/master
