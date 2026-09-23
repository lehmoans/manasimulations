import argparse

from .config.configuration import CaseConfigurationManager
from .core.simulation import AutoFluent


def build_parser():
    parser = argparse.ArgumentParser(
        prog="autofluent",
        description="Config-driven ANSYS Fluent automation.",
    )
    subparsers = parser.add_subparsers(dest="command")

    run = subparsers.add_parser("run", help="Run a case configuration.")
    run.add_argument(
        "--case",
        default=None,
        help="YAML path or saved case configuration name.",
    )
    run.add_argument(
        "--environment",
        required=True,
        choices=("local", "m3", "mock"),
        help="Execution environment.",
    )

    saved = subparsers.add_parser(
        "saved-cases",
        help="List saved case configurations.",
    )

    subparsers.add_parser("gui", help="Open the case configuration GUI.")

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "gui":
        from .gui import launch_gui

        launch_gui()
        return 0

    manager = CaseConfigurationManager()

    if args.command == "saved-cases":
        for name in manager.list_saved():
            print(name)
        return 0

    if args.command == "run":
        case_path = manager.resolve_case(args.case)
        result = AutoFluent(
            {
                "case_path": str(case_path),
                "environment_type": args.environment,
            }
        ).run()
        print(result)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
