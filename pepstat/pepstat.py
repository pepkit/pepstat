import argparse
import pipestat
from peppy import Project

def build_argparser():
    parser = argparse.ArgumentParser(description="Generate a POP.")
    parser.add_argument(
        "path", metavar="path", type=str, help="path to PEP"
    )
    parser.add_argument(
        "-n",
        "--namespace",
        type=str,
        dest="namespace",
        required=True,
        help="namespace to store PEP info.",
    )
    parser.add_argument(
        "-p",
        "--project",
        type=str,
        dest="project",
        required=True,
        help="name of project to store the PEP info.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        dest="out_file",
        default="index.yaml",
        help="path to file to report results."
    )
    return parser


def main():
    """Main function"""
    parser = build_argparser()
    args = parser.parse_args()

    psm = pipestat.PipestatManager(
        namespace=args.namespace,
        record_identifier=args.project,
        results_file_path=args.out_file,
        schema_path="pepstat/pipestat_schema.yaml"
    )
    p = Project(args.path)
    psm.report(values={
        'n_samples': len(p.samples)
    })

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Goodbye.")
