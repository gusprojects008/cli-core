#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

def main():
    parser = argparse.ArgumentParser(
        description="",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging and save logs to file"
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    argcomplete.autocomplete(parser)
    
    args = parser.parse_args()

    log_path = setup_logging(verbose=args.verbose)

if __name__ == "__main__":
    main()
