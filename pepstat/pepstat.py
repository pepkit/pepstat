from logging import getLogger
import yaml
import os
from .const import PKG_NAME
from .exceptions import PipstatError

_LOGGER = getLogger(PKG_NAME)


class PEPIndexer():
    """Class to parse a pephub repository and preoduce an index file."""
    def __init__(self):
        pass

    def _is_valid_namespace(self, path: str, name: str) -> bool:
        """
        Check if a given path is a valid namespace directory. Function
        Will check a given path for the following criteria:
            1. Is a folder
            2. Is not a "dot" file (e.g. .git)
        
        :param str path - path to potential namespace
        :param str name - name of namespace
        """
        criteria = [os.path.isdir(path), not name.startswith(".")]
        return all(criteria)

    def _is_valid_project(self, path: str, name: str) -> bool:
        """
        Check if a given project name is a valid project
        directory. Will check a given project for the following
        criteria:
            1. Is a folder
            2. Is not a "dot" file (e.g. .git)
        
        :param str path - path potential project
        :param str name - name of project
        """
        criteria = [os.path.isdir(path), not name.startswith(".")]
        return all(criteria)


    def _extract_project_file_name(self, path_to_proj: str) -> str:
        """
        Take a given path to a PEP/project inside a namespace and
        return the name of the PEP configuration file. The process
        is completed in the following steps:
            1. Look for a .pep.yaml file
                if exists -> check for config_file attribute
                else step two
            2. Look for project_config.yaml
                if exists -> return path
                else step 3
            3. If no .pep.yaml file with config_file attribute exists AND
            no porject_config.yaml file exists, then return None.
        
        :param str path_to_proj - path to the project
        """
        try:
            with open(f"{path_to_proj}/.pep.yaml", "r") as stream:
                _pephub_yaml = yaml.safe_load(stream)

            # check for config_file attribute
            if "config_file" in _pephub_yaml:
                # check that the config file exists
                if not os.path.exists(f"{path_to_proj}/{_pephub_yaml['config_file']}"):
                    _LOGGER.warn(
                        f"Specified pep config file '{_pephub_yaml['config_file']}'\
                        not found in directory, '{path_to_proj}'. This pep will be unloadable by pephub. "
                    )
            return _pephub_yaml["config_file"]

        # catch no .pep.yaml exists
        except FileNotFoundError:
            if not os.path.exists(f"{path_to_proj}/project_config.yaml"):
                _LOGGER.warn(
                    f"No project config file found for {path_to_proj}.\
                    This project will not be accessible by pephub. "
                )
            return "project_config.yaml"


    def index(self, path: str, data_store: dict) -> None:
        """
        Load the storage tree into memory by traversing
        the folder structure and storing locations to
        configuration files into the dictonary.

        :param str path - path to repository
        """

        # traverse directory
        for name in os.listdir(path):
            # build a path to the namespace
            path_to_namespace = f"{path}/{name}"
            if self._is_valid_namespace(path_to_namespace, name):
                # init sub-dict
                data_store[name.lower()] = {}

                # traverse projects
                for proj in os.listdir(path_to_namespace):
                    # build path to project
                    path_to_proj = f"{path_to_namespace}/{proj}"
                    if self._is_valid_project(path_to_proj, proj):
                        data_store[name.lower()][
                            proj.lower()
                        ] = f"{path_to_proj}/{self._extract_project_file_name(path_to_proj)}"

        return data_store

