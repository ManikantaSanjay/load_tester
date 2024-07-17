from argparse import ArgumentParser
import json
from load_tester import run_load_test

def setup_parser():
    """
    Sets up an ArgumentParser for the Asynchronous HTTP Load Tester.

    Returns:
        ArgumentParser: The parser object.

    Example:
        >>> parser = setup_parser()
        >>> args = parser.parse_args(["https://example.com", "--qps", "5", "--concurrency", "20", "steady"])
        >>> args.url
        'https://example.com'
        >>> args.qps
        5
        >>> args.concurrency
        20
        >>> args.pattern
        'steady'
    """
    parser = ArgumentParser(description="Asynchronous HTTP Load Tester")
    parser.add_argument("url", type=str, help="URL to test")
    parser.add_argument("--qps", type=int, default=1, help="Queries per second")
    parser.add_argument("--method", type=str, default="GET", choices=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"],
                    help="HTTP method to use for the requests")
    parser.add_argument("--data", type=json.loads, default={}, help="Data to send with the request; expected JSON format")
    parser.add_argument("--duration", type=int, default=10, help="Duration of test in seconds")
    parser.add_argument("-c", "--concurrency", type=int, default=10, help="Maximum number of concurrent requests")

    # Subparsers for each load pattern
    subparsers = parser.add_subparsers(dest='pattern', required=True, help='Load pattern configurations', title='load patterns')

    # Common options for spike-related patterns
    spike_parent = ArgumentParser(add_help=False)
    spike_parent.add_argument("--spike_duration", type=int, default=10, help="Duration of the spike in seconds")
    spike_parent.add_argument("--spike_load", type=int, default=20, help="Concurrency level during the spike")

    # Steady load pattern
    steady_parser = subparsers.add_parser('steady', help='Steady load pattern')
    steady_parser.set_defaults(func=run_load_test, pattern='steady')

    # Spike load pattern
    spike_parser = subparsers.add_parser('spike', help='Spike load pattern')
    spike_parser.add_argument("--spike_duration", type=int, default=10, help="Duration of the spike in seconds")
    spike_parser.add_argument("--spike_load", type=int, default=20, help="Concurrency level during the spike")
    spike_parser.set_defaults(func=run_load_test, pattern='spike')

    # Periodic spike pattern
    periodic_parser = subparsers.add_parser('periodic', help='Periodic spike pattern')
    periodic_parser.add_argument("--spike_interval", type=int, default=30, help="Interval between spikes in seconds")
    periodic_parser.add_argument("--spike_duration", type=int, default=5, help="Duration of each spike in seconds")
    periodic_parser.add_argument("--spike_load", type=int, default=20, help="Concurrency level during each spike")
    periodic_parser.set_defaults(func=run_load_test, pattern='periodic')
    
    return parser