from distutils.command.build import build
import pathlib
import yaml
import os
import warnings
import argparse

from tqdm import tqdm

PEP_VERSION = "2.0.0"
DELIM = ","
HEADER_COLS = ["sample_name", "namespace", "project", "cfg_path"]


def build_argparser():
    parser = argparse.ArgumentParser(description="Generate a POP.")
    parser.add_argument("path", metavar="path", type=str, help="path to PEPs")
    parser.add_argument("-o", "--out", type=str, default=".", help="path to POP output")
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        dest="config_file_name",
        default="pop.yaml",
        help="name of POP configuration file",
    )
    parser.add_argument(
        "-s",
        "--samples",
        type=str,
        dest="samples_file_name",
        default="peps.csv",
        help="name of sample table file",
    )
    return parser


def _extract_project_file_name(path_to_proj: str) -> str:
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
                warnings.warn(
                    f"Specified pep config file '{_pephub_yaml['config_file']}'\
                    not found in directory, '{path_to_proj}'. This pep will be unloadable by pephub. "
                )
        return _pephub_yaml["config_file"]

    # catch no .pep.yaml exists
    except FileNotFoundError:
        if not os.path.exists(f"{path_to_proj}/project_config.yaml"):
            warnings.warn(
                f"No project config file found for {path_to_proj}.\
                This project will not be accessible by pephub. "
            )
        return "project_config.yaml"


def _is_valid_namespace(path: str) -> bool:
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


def _is_valid_project(path: str) -> bool:
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


def _write_pop_cfg(cfg_path: str, sample_table_path: str):
    """
    Create the pop confgiuration file
    """
    cfg = {"pep_version": PEP_VERSION, "sample_table": sample_table_path}
    with open(cfg_path, "w") as fh:
        yaml.dump(cfg, fh)


def generate_pop(
    path: str, cfg_name: str = "pop.yaml", sample_table_path: str = "peps.csv"
):
    """
    Given a directory of PEPs in the namespace/project format, generate one unifying PEP of PEPs (POP)
    to be used as input to looper for indexing.
    """
    # check path exists ... make if not
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path to PEPs does not exist: '{path}'")

    # create a path to cfg if necessary
    if not os.path.exists(cfg_name):
        filepath = pathlib.Path(cfg_name)
        filepath.parent.mkdir(parents=True, exist_ok=True)

    # create a path to the sample table if necessary
    if not os.path.exists(sample_table_path):
        filepath = pathlib.Path(sample_table_path)
        filepath.parent.mkdir(parents=True, exist_ok=True)

    # init the cfg file
    _write_pop_cfg(cfg_name, sample_table_path)

    with open(sample_table_path, "w") as fh:
        # write the csv header
        fh.write(DELIM.join(HEADER_COLS) + "\n")
        # traverse directory
        for name in tqdm(os.listdir(path), desc="Analyzing repository", leave=True):
            # build a path to the namespace
            path_to_namespace = f"{path}/{name}"
            name = name.lower()

            if _is_valid_namespace(path_to_namespace):
                # traverse projects
                for proj in tqdm(
                    os.listdir(path_to_namespace), desc=f"Analyzing {name}", leave=True
                ):
                    # build path to project
                    path_to_proj = f"{path_to_namespace}/{proj}"
                    proj = proj.lower()

                    if _is_valid_project(path_to_proj):
                        # build cfg file
                        cfg_file = (
                            f"{path_to_proj}/{_extract_project_file_name(path_to_proj)}"
                        )

                        sample_table_row = DELIM.join(
                            [f"{name}-{proj}", name, proj, cfg_file]
                        )
                        fh.write(sample_table_row + "\n")


def main():
    parser = build_argparser()
    args = parser.parse_args()

    if not os.path.exists(args.out):
        filepath = pathlib.Path(args.out)
        filepath.parent.mkdir(exist_ok=True)

    cfg_file_name = f"{args.out}/{args.config_file_name}"
    samples_file_name = f"{args.out}/{args.samples_file_name}"
    
    generate_pop(args.path, cfg_file_name, samples_file_name)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Goodbye.")
