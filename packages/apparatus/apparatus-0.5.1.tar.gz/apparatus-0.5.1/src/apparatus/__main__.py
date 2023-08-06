import sys
from apparatus.utils import dissoc
from apparatus.base import Command


def main():
    parser = Command.create_parser()
    args, remainder = parser.parse_known_args()
    if not hasattr(args, "cls"):
        parser.print_usage()
        sys.exit(1)
    command = args.cls(**dissoc(vars(args), "cls"))
    command.run(remainder)

if __name__ == "__main__":
    main()
