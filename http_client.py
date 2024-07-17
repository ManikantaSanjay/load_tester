import aiohttp
import time
import json

async def fetch_server_info(url):
    """
    Fetches the server information from the given URL.

    Args:
        url (str): The URL to fetch the server information from.

    Returns:
        str: The server information, or 'Unknown' if not found.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            server = response.headers.get('Server', 'Unknown')
    return server

async def send_request(url, session, method="GET", data=None):
    """
    Sends a request to the given URL using the specified HTTP method and returns the elapsed time and response status.

    Args:
        url (str): The URL to send the request to.
        session (aiohttp.ClientSession): The client session to use for the request.
        method (str): HTTP method to use for the request (e.g., "GET", "POST", "PUT", "DELETE", "PATCH").
        data (dict or None): The data to send with the request (for methods that allow a body).

    Returns:
        tuple: A tuple containing the elapsed time (in seconds) and the response status (or error message).
    """
    start_time = time.time()
    try:
        # Prepare headers and data if necessary
        headers = {'Content-Type': 'application/json'} if data else {}
        # Convert data to JSON if it's provided
        json_data = json.dumps(data) if data else None

        # Select the correct method and send the request
        async with session.request(method, url, json=data, headers=headers) as response:
            elapsed_time = time.time() - start_time
            return elapsed_time, response.status
    except Exception as e:
        elapsed_time = time.time() - start_time
        return elapsed_time, str(e)


