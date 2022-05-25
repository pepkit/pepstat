from logging import getLogger
import peppy
import yaml
import os
import pathlib
from tqdm import tqdm
from .const import PKG_NAME
from .exceptions import PEPstatError

_LOGGER = getLogger(PKG_NAME)


class PEPIndexer():
    """Class to parse a pephub repository and preoduce an index file."""
    def __init__(self):
        self.index_store = None

    def _is_valid_namespace(self, path: str) -> bool:
        """
        Check if a given path is a valid namespace directory. Function
        Will check a given path for the following criteria:
            1. Is a folder
            2. Is not a "dot" file (e.g. .git)
        
        :param str path - path to potential namespace
        """
        name = pathlib.Path(path).name
        criteria = [os.path.isdir(path), not name.startswith(".")]
        return all(criteria)

    def _is_valid_project(self, path: str) -> bool:
        """
        Check if a given project name is a valid project
        directory. Will check a given project for the following
        criteria:
            1. Is a folder
            2. Is not a "dot" file (e.g. .git)
        
        :param str path - path potential project
        """
        name = pathlib.Path(path).name
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


    def index(self, path: str, output: str, reset=False) -> None:
        """
        Load the storage tree into memory by traversing
        the folder structure and storing locations to
        configuration files into the dictonary.

        :param str path - path to repository
        :param str output - path to the output file of the index
        :param boolean reset - flag to reset the index if one has already been created
        """
        # check path exists ... make if not
        if not os.path.exists(output):
            filepath = pathlib.Path(output)
            filepath.parent.mkdir(parents=True, exist_ok=True)

        # init datastore dict if it doesn't already exist
        if any([self.index_store is None, reset]):
            self.index_store = {}

        # traverse directory
        for name in tqdm(os.listdir(path), desc="Indexing repository", leave=True):
            # build a path to the namespace
            path_to_namespace = f"{path}/{name}"
            if self._is_valid_namespace(path_to_namespace):
                # init sub-dict
                self.index_store[name.lower()] = {}

                # traverse projects
                for proj in tqdm(os.listdir(path_to_namespace), desc=f"Indexing {name}", leave=True):
                    # build path to project
                    path_to_proj = f"{path_to_namespace}/{proj}"
                    if self._is_valid_project(path_to_proj):
                        self.index_store[name.lower()][
                            proj.lower()
                        ] = {
                            'name': proj,
                            'cfg': f"{path_to_proj}/{self._extract_project_file_name(path_to_proj)}"
                        }

                        # store number of samples in project by loading project into memory
                        p = peppy.Project(self.index_store[name.lower()][proj.lower()]['cfg'])
                        self.index_store[name.lower()][proj.lower()]['n_samples'] = len(p.samples)

                        # store href
                        self.index_store[name.lower()][proj.lower()]['href'] = f"/pep/{name.lower()}/{proj.lower()}"

        # dump to yaml
        with open(output, 'w') as fh:
            yaml.dump(self.index_store, fh)
        
        return self.index_store
    
    def get_index(self) -> dict:
        """Return dict representation of the index"""
        return self.index_store
    
    def load_index(self, path: str):
        """
        Load a previously created index file.

        :param str path - path to the file.
        """
        with open(path, 'r') as fh:
            self.index_store = yaml.safe_load(fh)
        return



