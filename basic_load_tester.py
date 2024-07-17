import requests
import threading
import time
from queue import Queue
from argparse import ArgumentParser

def send_request(url, results):
    """
    Send a GET request to the specified URL and store the result in the results queue.

    Args:
        url (str): The URL to send the request to.
        results (Queue): The queue to store the result in.

    Returns:
        None
    """
    start_time = time.time()
    try:
        response = requests.get(url)
        elapsed_time = time.time() - start_time
        if response.status_code == 200:
            results.put((elapsed_time, None))
        else:
            results.put((elapsed_time, f"Error: Status {response.status_code}"))
    except Exception as e:
        elapsed_time = time.time() - start_time
        results.put((elapsed_time, str(e)))

def worker(url, qps, duration, results):
    """
    Worker function that sends requests to the specified URL at a specified rate.

    Args:
        url (str): The URL to send requests to.
        qps (int): The number of queries per second.
        duration (int): The duration of the test in seconds.
        results (Queue): The queue to store the results in.

    Returns:
        None
    """
    interval = 1 / qps
    next_time = time.time() + interval
    stop_time = time.time() + duration
    while time.time() < stop_time:
        send_request(url, results)
        next_time += interval
        sleep_time = next_time - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time) 

def main(url, qps, duration):
    """
    Main function that runs the load test.

    Args:
        url (str): The URL to test.
        qps (int): The number of queries per second.
        duration (int): The duration of the test in seconds.

    Returns:
        None
    """
    results = Queue()
    thread = threading.Thread(target=worker, args=(url, qps, duration, results))
    thread.start()
    thread.join()

    total_requests = 0
    total_time = 0
    errors = 0

    while not results.empty():
        elapsed_time, error = results.get()
        total_requests += 1
        total_time += elapsed_time
        if error:
            errors += 1
    
    if total_requests == 0:  # Added check for division by zero
        avg_latency = 0
    else:
        avg_latency = total_time / total_requests
    print(f"Total Requests: {total_requests}")
    print(f"Average Latency: {avg_latency:.2f} seconds")
    if total_requests == 0:  # Added check for division by zero
        error_rate = 0
    else:
        error_rate = errors / total_requests * 100
    print(f"Error Rate: {error_rate:.2f}%")

if __name__ == "__main__":
    parser = ArgumentParser(description="HTTP Load Tester")
    parser.add_argument("url", type=str, help="URL to test")
    parser.add_argument("--qps", type=int, default=1, help="Queries per second")
    parser.add_argument("--duration", type=int, default=10, help="Duration of test in seconds")
    args = parser.parse_args()
    
    main(args.url, args.qps, args.duration)
