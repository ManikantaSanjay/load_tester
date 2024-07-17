import numpy as np

def calculate_and_display_results(results, errors, duration):
    """
    Calculate and display various statistics from a list of request times and errors.

    Parameters:
    results (list): A list of request times in seconds
    errors (list): A list of error messages (if any)
    duration (float): The total duration of the test in seconds

    Returns:
    None

    Example:
    >>> results = [0.1, 0.2, 0.3, 0.4, 0.5]
    >>> errors = []
    >>> duration = 10.0
    >>> calculate_and_display_results(results, errors, duration)
    -------- Results --------
    Total Requests: 5
    Total time: 1.5000s
    Average time per request / Latency: 0.3000s
    Fastest time: 0.1000s
    Slowest time: 0.5000s
    Amplitude: 0.4000s
    Standard deviation: 0.141421
    Requests Per Second: 0.50
    Error Rate: 0.00%
    Response Time Percentiles:
      50th Percentile: 0.3000s
      75th Percentile: 0.4000s
      90th Percentile: 0.5000s
    """

    total_requests = len(results)
    total_time = sum(results)
    avg_time = np.mean(results)
    min_time = min(results)
    max_time = max(results)
    std_dev = np.std(results)
    rps = total_requests / duration
    error_rate = (len(errors) / total_requests) * 100 if total_requests else 0
    percentiles = np.percentile(results, [50, 75, 90, 95, 99])

    print("-------- Results --------")
    print(f"Total Requests: {total_requests}")
    print(f"Total time: {total_time:.4f}s")
    print(f"Average time per request / Latency: {avg_time:.4f}s")
    print(f"Fastest time: {min_time:.4f}s")
    print(f"Slowest time: {max_time:.4f}s")
    print(f"Amplitude: {max_time - min_time:.4f}s")
    print(f"Standard deviation: {std_dev:.6f}")
    print(f"Requests Per Second: {rps:.2f}")
    print(f"Error Rate: {error_rate:.2f}%")
    print("Response Time Percentiles:")
    print(f"  50th Percentile: {percentiles[0]:.4f}s")
    print(f"  75th Percentile: {percentiles[1]:.4f}s")
    print(f"  90th Percentile: {percentiles[2]:.4f}s")
