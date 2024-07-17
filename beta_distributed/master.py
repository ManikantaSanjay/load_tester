import asyncio
import json
from argparse import ArgumentParser

async def handle_worker(reader, writer, config):
    """
    Handle incoming messages from a worker node.

    This function reads messages from the worker, processes them, and sends a response back.
    If the worker sends a 'READY' message, it sends the configuration to the worker and closes the connection.

    Args:
        reader (asyncio.StreamReader): The reader object for the incoming connection.
        writer (asyncio.StreamWriter): The writer object for the outgoing connection.
        config (dict): The configuration to send to the worker.
    """
    while True:
        data = await reader.read(1024)
        if not data:
            break
        message = json.loads(data.decode())
        print(f"Received from worker: {message['status']}")

        if message['status'] == 'READY':
            # Send the configuration to the worker
            writer.write(json.dumps({"command": "START", "params": config}).encode())
            await writer.drain()
            print("Configuration sent, closing connection.")
            writer.close()
            return  # Close this handler to prevent handling further messages from the same worker

async def run_master(host, port, configs):
    """
    Run the master node that accepts incoming connections from worker nodes.

    Args:
        host (str): The host to bind to.
        port (int): The port to listen on.
        configs (list[dict]): A list of configurations to send to worker nodes.

    Example:
        >>> configs = [{'concurrency': 10, 'duration': 60}, {'concurrency': 20, 'duration': 30}]
        >>> asyncio.run(run_master('localhost', 8888, configs))
    """
    async def start_server_callback(reader, writer):
        # Assign each worker a unique configuration from the list, remove it once assigned
        if configs:
            config = configs.pop(0)
            await handle_worker(reader, writer, config)
        else:
            print("No more configurations available.")
            writer.close()

    server = await asyncio.start_server(start_server_callback, host, port)
    print(f"Master running on {host}:{port}")
    async with server:
        await server.serve_forever()

def load_configurations(file_path):
    """
    Load configurations from a JSON file.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        list[dict]: A list of configurations.

    """
    with open(file_path, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    parser = ArgumentParser(description="Start HTTP load testing master node for distributed load testing")
    parser.add_argument('--host', type=str, default='0.0.0.0', help="Host for the master to bind")
    parser.add_argument('--port', type=int, default=8888, help="Port for the master to listen on")
    parser.add_argument('--config', type=str, default='config.json', help="Path to configuration file")
    args = parser.parse_args()

    configurations = load_configurations(args.config)
    asyncio.run(run_master(args.host, args.port, configurations))
