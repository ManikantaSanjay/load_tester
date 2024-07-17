# load_tester.py
import asyncio
import aiohttp
from tqdm import tqdm
from async_worker import worker
from utils import calculate_and_display_results
from load_patterns import compute_load_schedule
from http_client import fetch_server_info
import time

async def execute_load_test(url, load_pattern, qps, duration, concurrency, semaphore, method, data=None):
    """
    Execute a load test on a given URL with a specified load pattern.

    Args:
        url (str): The URL to test.
        load_pattern (list): A list of integers representing the load schedule.
        qps (int): The target queries per second.
        duration (int): The duration of the test in seconds.
        concurrency (int): The maximum number of concurrent requests.
        semaphore (asyncio.Semaphore): A semaphore to limit concurrency.
        method (str): The HTTP method to use (e.g. "GET", "POST").
        data (dict): Optional data to send with the request.

    Returns:
        tuple: A tuple containing the results and errors of the test.
    """
    results = []
    errors = []
    pbar = tqdm(total=qps * duration, desc="Progress", unit="req")
    
    # Use a proper async context manager for session
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        for second, current_load in enumerate(load_pattern):
            if current_load == 0:
                await asyncio.sleep(1)
                continue
            tasks = [asyncio.create_task(worker(url, session, method, semaphore, results, errors, data)) for _ in range(current_load)]
            await asyncio.gather(*tasks)
            pbar.update(len(tasks))  # Update for all tasks started

            # Ensure correct pacing by sleeping until the end of the second
            await asyncio.sleep(max(0, 1 - (time.time() - start_time - second)))

        pbar.close()

    return results, errors


async def run_load_test(url, qps, duration, concurrency, args):
    """
    Run a load test on a given URL with specified parameters.

    Args:
        url (str): The URL to test.
        qps (int): The target queries per second.
        duration (int): The duration of the test in seconds.
        concurrency (int): The maximum number of concurrent requests.
        args (object): An object containing additional arguments, such as pattern, spike_duration, spike_load, and spike_interval.
    """
    semaphore = await prepare_test(url, concurrency)
    # Check the pattern and set up accordingly
    if args.pattern == "periodic":
        load_schedule = compute_load_schedule(args.pattern, qps, duration, concurrency,
                                              spike_duration=args.spike_duration,
                                              spike_load=args.spike_load,
                                              spike_interval=args.spike_interval)
    elif args.pattern == "spike":
        load_schedule = compute_load_schedule(args.pattern, qps, duration, concurrency,
                                              spike_duration=args.spike_duration,
                                              spike_load=args.spike_load)
    else:
        load_schedule = compute_load_schedule(args.pattern, qps, duration, concurrency)
    
    print(f"Load Schedule: {load_schedule}")  # Debugging output

    results, errors = await execute_load_test(url, load_schedule, qps, duration, concurrency, semaphore, args.method, args.data)
    calculate_and_display_results(results, errors, duration)

async def prepare_test(url, concurrency):
    """
    Prepare the load test by fetching server information and setting up the semaphore.

    Args:
        url (str): The URL to test.
        concurrency (int): The maximum number of concurrent requests.

    Returns:
        asyncio.Semaphore: A semaphore to limit concurrency.
    """

    server_info = await fetch_server_info(url)
    print("-------- Server info --------")
    print(f"Server Software: {server_info}")
    print(f"Host: {url}\n")
    semaphore = asyncio.Semaphore(concurrency)
    return semaphore