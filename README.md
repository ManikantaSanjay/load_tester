# HTTP Load Tester

The HTTP Load Tester is a sophisticated Python-based tool designed for stress testing web servers under high traffic conditions to measure server performance, average latency, and error rates.

## Project Files Overview

### **http_client.py**
- **Purpose**: Manages HTTP requests using `aiohttp`.
- **Functions**:
  - `fetch_server_info(url)`: Fetches server type from the response headers.
  - `send_request(url, session, method, data)`: Sends HTTP requests with methods like GET, POST and supports data payloads.

### **async_worker.py**
- **Description**: Manages asynchronous task execution using `http_client.py` to send HTTP requests, handling concurrency and result collection.
- **Main Function**: `worker(url, session, method, semaphore, results, errors, data)`

### **load_patterns.py**
- **Description**: Defines load patterns such as steady, spike, and periodic spikes.
- **Function**: `compute_load_schedule(pattern, qps, duration, concurrency, spike_duration, spike_load, spike_interval)`

### **load_tester.py**
- **Description**: Orchestrates the load testing process by utilizing other modules to setup the environment, execute the load test, and compute results.
- **Functions**:
  - `execute_load_test(...)`: Executes the load test based on a predefined load schedule.
  - `run_load_test(...)`: Initiates the testing process using parameters from the command line.

### **main.py**
- **Description**: Entry point for the application, handles command line arguments and initiates load testing.
- **Function**: `main()`

### **parser.py**
- **Description**: Manages command line arguments for the application, supporting different load patterns and methods.
- **Function**: `setup_parser()`

### **utils.py**
- **Description**: Provides utilities to calculate and display results.
- **Function**: `calculate_and_display_results(results, errors, duration)`

## Features

- **Configurable QPS**: Set desired queries per second to test server load levels.
- **Adjustable Duration**: Specify test length from brief stress tests to extended stability tests.
- **Concurrency Management**: Simulates multiple users or connections using threading.
- **Performance Metrics**: Outputs total requests, average latency, error rates.

## Prerequisites

Requires Python 3.10+. Install dependencies with:

```bash
pip install --no-cache-dir -r requirements.txt
```

## Basic Usage
Run the script by specifying the target URL along with optional parameters for QPS and duration:

```
python basic_load_tester.py <url> --qps <queries_per_second> --duration <duration_in_seconds>
```

Parameters
url: Target URL for the load test.
--qps: Queries per second (default is 1).
--duration: Duration of the test in seconds (default is 10).
Example
To run a test against http://example.com with 10 queries per second for 60 seconds:

#### Example Command
```
python basic_load_tester.py http://example.com --qps 10 --duration 60
```

## Advanced Usage with Asynchronous Load Tester

### Docker Setup and Usage - Pulling the Docker Image

To get started with the HTTP Load Tester Docker image, first pull the image from Docker Hub:

```
docker pull manikantasanjay1999/loadtest:v3
```

### Running the Default Command
After pulling the image, you can run the default load test configuration directly:
```
docker run manikantasanjay1999/loadtest:v3
```

This command executes the load tester with predefined parameters set within the Dockerfile. It's useful for quickly starting a test with the standard configuration.

### Running Tests

To run a test, use the main.py script with desired parameters. Here are the command-line options available for setup:

#### Command-line Options
* **URL**: Endpoint to test.
* **--qps**: Queries per second.
* **--duration**: Test duration in seconds.
* **-c, --concurrency**: Max concurrent requests.
* **--method**: HTTP method (GET, POST, etc.).
* **--data**: JSON formatted data for requests.
* **--pattern**: Load pattern ('steady', 'spike', 'periodic').
* **--spike_duration**: Duration in seconds for spike.
* **--spike_load**: Concurrency level during spikes.
* **--spike_interval**: Seconds between periodic spikes

#### Example command:

```
python main.py https://example.com --qps 10 --duration 60 -c 5 --method GET --pattern steady
```



### Running with Custom Load Testing Parameters

You can override the default CMD at runtime by providing your own command line arguments. Here's how to specify different load testing parameters:

#### Example 1: Steady Load Test
Run a steady load test with customized parameters:

```
docker run manikantasanjay1999/loadtest:v3 \
    https://example.com \
    --qps 10 \
    --duration 60 \
    -c 5 \
    --method GET \
    --pattern steady
```

#### Example 2: Spike Load Test
Configure a spike load test to see how the server handles sudden increases in traffic:

```
docker run manikantasanjay1999/loadtest:v3 \
    https://example.com \
    --qps 10 \
    --duration 60 \
    -c 15 \
    --method GET \
    --pattern spike \
    --spike_duration 5 \
    --spike_load 30
```

#### Example 3: Periodic Spike Load Test
Test the server's resilience to periodic spikes in traffic:

```
docker run manikantasanjay1999/loadtest:v3 \
    https://example.com \
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

```
docker logs [container_id]
Replace [container_id] with the actual container ID of your running Docker container. You can find the container ID by running docker ps.
```

### Stopping a Container

To stop a running container:

```
docker stop [container_id]
```

## Asynchronous Distributed Load Tester - (Beta Version -- Work In Progress!!!!!!! 👷)

### Overview

This part of project implements a distributed HTTP load testing tool using Python's asyncio. It's designed to allow testing under different load patterns by coordinating multiple worker nodes through a master node. The system is configurable via a JSON file, enabling dynamic distribution of testing parameters to various workers.

### Key Components

- Master Node (master.py): Coordinates the load testing by distributing configuration to worker nodes. It listens for connections from workers, sends them testing parameters, and manages available configurations.

- Worker Node (worker.py): Connects to the master node, receives configuration, and performs the load testing as per the received parameters.

- Config.json: This file contains the different load distributions that the http connection needs to be tested upon. 


### Navigate to the Project Directory

Assuming your scripts are in a folder named beta_distributed within your main project directory, you can navigate to this folder using the following command:


```
cd ./beta_distributed
```

### Run the Master Node

Once inside the correct folder, you can start the master node with the appropriate command. If you're using a config.json file to specify the configurations for your load tests, make sure it's accessible within this directory or specify the correct path to it:


```
python master.py --host 0.0.0.0 --port 8888 --config config.json
```

This command sets up the master to listen on all network interfaces (0.0.0.0) on port 8888, and it uses the config.json file located in the same directory.

### Run the Worker Node

To run a worker node that connects to this master, use the following command. Replace <master-ip-address> with the IP address of the machine where the master node is running if you are using different machines. If running locally on the same machine, you can use localhost:

bash

```
python worker.py --master-host <master-ip-address> --master-port 8888
```

If both the master and worker are running on the same machine and you are using localhost as the master host:

```
python worker.py --master-host localhost --master-port 8888
```
