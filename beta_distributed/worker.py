import asyncio
import json
from argparse import ArgumentParser
from types import SimpleNamespace

import sys
import os

sys.path.append(os.path.abspath('../'))
from http_client import fetch_server_info, send_request
from load_tester import run_load_test

async def worker(args):
    """
    Worker function to execute load tests based on given parameters.

    Args:
        args (SimpleNamespace): An object containing all necessary parameters including URL, method, QPS, duration,
                                concurrency, and additional parameters like data and load pattern specifics.
    """
    # Assuming args might contain another namespace or dict under 'args'
    additional_args = getattr(args, 'args', SimpleNamespace())
    if isinstance(additional_args, dict):
        additional_args = SimpleNamespace(**additional_args)
    
    # Access pattern and other optional parameters safely
    pattern = getattr(additional_args, 'pattern', 'steady')
    data = getattr(additional_args, 'data', None)
    method = getattr(additional_args, 'method','GET')

    print(f"Starting load test on {args.url} with {method} method under {pattern} pattern.")
    await run_load_test(args.url, args.qps, args.duration, args.concurrency, additional_args)

async def connect_to_master(host, port):
    """
    Connects to the master and receives configuration to run the load test.
    """
    reader, writer = await asyncio.open_connection(host, port)
    print(f"Connected to master at {host}:{port}")

    # Send ready message and wait for configuration
    writer.write(json.dumps({"status": "READY"}).encode())
    await writer.drain()

    data = await reader.read(1024)
    command_data = json.loads(data.decode())

    if command_data['command'] == 'START':
        params = SimpleNamespace(**command_data['params'])
        print('Received params:', params)
        await worker(params)

    writer.close()
    await writer.wait_closed()

if __name__ == "__main__":
    parser = ArgumentParser(description="Worker for Distributed HTTP Load Testing")
    parser.add_argument("--master-host", type=str, default="localhost", help="Host of the master server")
    parser.add_argument("--master-port", type=int, default=8888, help="Port on which the master server is listening")
    args = parser.parse_args()
    asyncio.run(connect_to_master(args.master_host, args.master_port))
