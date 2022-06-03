import argparse
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
    return parser


def main():
    """Main function"""
    parser = build_argparser()
    args = parser.parse_args()

    print(f"-----> Namespace: {args.namespace} | project: {args.project} | {args.path}")
    p = Project(args.path)
    print(f"-----> No. samples: {len(p.samples)}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Goodbye.")
