# HTTP Load Tester

The HTTP Load Tester is a Python-based tool designed to stress test web servers by simulating high traffic conditions. It allows you to measure server performance in terms of handling multiple requests per second and determine the average latency and error rates.

Project Files Overview

- http_client.py
  This module handles HTTP requests using the aiohttp library. It provides functions to fetch server information and send asynchronous HTTP requests with custom methods and data.

--> fetch_server_info(url): Fetches the server information such as server type from the response headers.

--> send_request(url, session, method, data): Sends HTTP requests using specified methods like GET, POST, and allows data payloads.

- async_worker.py
  Contains the asynchronous worker logic that utilizes http_client.py to send HTTP requests. It manages concurrency using semaphores and collects results and errors from HTTP responses.

--> worker(url, session, method, semaphore, results, errors, data): Sends requests and manages results within concurrency limits.

- load_patterns.py
  Defines various load patterns such as steady, spike, and periodic spike loads. These patterns dictate the load generation strategy during tests.

--> compute_load_schedule(pattern, qps, duration, concurrency, spike_duration, spike_load, spike_interval): Generates a load schedule based on the specified pattern.

- load_tester.py
  Orchestrates the entire load testing process by combining the components from other modules. It sets up the testing environment, executes the load test using the specified patterns, and calculates results.

--> execute_load_test(url, load_pattern, qps, duration, concurrency, semaphore, method, data): Executes the load test based on a predefined load schedule.
--> run_load_test(url, qps, duration, concurrency, args): Prepares and runs the load test using parameters specified via command line.

- main.py
  The entry point of the application. It parses command line arguments and initiates the load testing process.

main(): Sets up command-line argument parsing and runs the load test.

- parser.py
  Handles the creation and management of command-line arguments.

--> setup_parser(): Configures command-line arguments for the application, supporting different load patterns and HTTP methods.

- utils.py
  Provides utility functions to process and display the results from load tests.

--> calculate_and_display_results(results, errors, duration): Calculates and prints detailed statistics from the load test results, such as average latency, error rates, and response time percentiles.

## Basic Load Tester

### Features

- **Configurable Query Per Second (QPS):** Set the desired number of queries per second to test different levels of server load.
- **Adjustable Duration:** Specify the length of time the load test should run, accommodating everything from brief stress tests to extended stability tests.
- **Concurrency Management:** Uses threading to simulate multiple simultaneous users or connections hitting the server.
- **Performance Metrics:** Outputs total requests, average latency, and error rates to help evaluate server performance.

### Prerequisites

To use this tool, you need Python 3.10 or newer. Dependencies can be installed using pip:

pip install --no-cache-dir -r requirements.txt

Usage
Run the script by specifying the target URL along with optional parameters for QPS and duration:

bash

```
python basic_load_tester.py <url> --qps <queries_per_second> --duration <duration_in_seconds>
```

Parameters
url: Target URL for the load test.
--qps: Queries per second (default is 1).
--duration: Duration of the test in seconds (default is 10).
Example
To run a test against http://example.com with 10 queries per second for 60 seconds:

bash

```
python basic_load_tester.py http://example.com --qps 10 --duration 60
```

## Asynchronous Load Tester

### Running Tests

To run a test, use the main.py script with desired parameters. Here are the command-line options available for setup:

- URL: The endpoint URL to test.
- --qps (Queries Per Second): The rate at which requests are sent.
- --duration: Duration of the test in seconds.
- -c, --concurrency: Maximum number of concurrent requests.
- --method: HTTP method to be used, options include "GET", "POST", "PUT", "DELETE", "PATCH", "HEAD".
- --data: Data to be sent with the request in JSON format; applicable for POST, PUT, etc.
- --pattern: Load pattern type, options are 'steady', 'spike', 'periodic'.
- --spike_duration: Duration of the spike in seconds (applicable for spike and periodic patterns).
- --spike_load: Concurrency level during the spike.
- --spike_interval: Interval between spikes in seconds (only for periodic pattern).

### Example command:

bash

```
python main.py https://example.com --qps 10 --duration 60 -c 5 --method GET --pattern steady
```

## Running with Custom Load Testing Parameters

You can override the default CMD at runtime by providing your own command line arguments. Here's how to specify different load testing parameters:

### Example 1: Steady Load Test

bash

```
docker run manikantasanjay1999/loadtest:v3 \
    --url https://example.com \
    --qps 10 \
    --duration 60 \
    -c 5 \
    --method GET \
    --pattern steady
```

### Example 2: Spike Load Test

bash

```
docker run manikantasanjay1999/loadtest:v3 \
    --url https://example.com \
    --qps 10 \
    --duration 60 \
    -c 15 \
    --method GET \
    --pattern spike \
    --spike_duration 5 \
    --spike_load 30
```

### Example 3: Periodic Spike Load Test

bash

```
docker run manikantasanjay1999/loadtest:v3 \
    --url https://example.com \
    --qps 5 \
    --duration 120 \
    -c 10 \
    --method GET \
    --pattern periodic \
    --spike_interval 20 \
    --spike_duration 5 \
    --spike_load 20
```

## Additional Docker Commands

### Viewing Docker Logs

To view the logs of a running Docker container to monitor the output of your load tests, you can use:

bash

```
docker logs [container_id]
Replace [container_id] with the actual container ID of your running Docker container. You can find the container ID by running docker ps.
```

### Stopping a Container

To stop a running container:

bash

```
docker stop [container_id]
```

## Asynchronous Distributed Load Tester

### Overview

This project implements a distributed HTTP load testing tool using Python's asyncio. It's designed to allow testing under different load patterns by coordinating multiple worker nodes through a master node. The system is configurable via a JSON file, enabling dynamic distribution of testing parameters to various workers.

### Key Components

- Master Node (master.py): Coordinates the load testing by distributing configuration to worker nodes. It listens for connections from workers, sends them testing parameters, and manages available configurations.

- Worker Node (worker.py): Connects to the master node, receives configuration, and performs the load testing as per the received parameters.

- HTTP Client (http_client.py): Provides asynchronous HTTP request functionalities, supporting various methods like GET, POST, PUT, etc.

- Load Tester (load_tester.py): Orchestrates the setup and execution of load tests using the configurations provided by the master.

- Load Patterns (load_patterns.py): Defines various load patterns such as steady, spike, and periodic spikes.

- Utilities (utils.py): Contains utility functions like calculating and displaying results.

### Navigate to the Project Directory

Assuming your scripts are in a folder named beta_distributed within your main project directory, you can navigate to this folder using the following command:

bash

```
cd path/to/your/project/beta_distributed
```

Replace path/to/your/project/ with the actual path where your project is located on your system.

## Run the Master Node

Once inside the correct folder, you can start the master node with the appropriate command. If you're using a config.json file to specify the configurations for your load tests, make sure it's accessible within this directory or specify the correct path to it:

bash

```
python master.py --host 0.0.0.0 --port 8888 --config config.json
```

This command sets up the master to listen on all network interfaces (0.0.0.0) on port 8888, and it uses the config.json file located in the same directory.

### Run the Worker Node

To run a worker node that connects to this master, use the following command. Replace <master-ip-address> with the IP address of the machine where the master node is running if you are using different machines. If running locally on the same machine, you can use localhost:

bash

```
python worker.py --master-host <master-ip-address> --master-port 8888
If both the master and worker are running on the same machine and you are using localhost as the master host:
```

bash

```
python worker.py --master-host localhost --master-port 8888
```
