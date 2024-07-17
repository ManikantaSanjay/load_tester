import asyncio
from parser import setup_parser

def main():
    """
    Main entry point of the async worker script to perform load testing.

    This script takes in command-line arguments to configure a load test.
    It uses the `setup_parser` function to create a parser, parses the arguments,
    and then runs the specified load test function with the provided arguments.

    Args:
        None

    Returns:
        None
    """
    # Create the top-level parser
    parser = setup_parser()
    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.error("No load pattern selected!")

    asyncio.run(args.func(args.url, args.qps, args.duration, args.concurrency, args))

if __name__ == "__main__":
    main()