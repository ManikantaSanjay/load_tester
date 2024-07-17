from http_client import send_request

async def worker(url, session, method, semaphore, results, errors, data=None):
    """
    Asynchronous worker function to send an HTTP request to a given URL.

    Args:
        url (str): The URL to send the request to.
        session (aiohttp.ClientSession): The aiohttp client session to use for the request.
        method (str): The HTTP method to use (e.g. "GET", "POST", etc.).
        semaphore (asyncio.Semaphore): A semaphore to limit the number of concurrent requests.
        results (list): A list to store the response times of successful requests.
        errors (list): A list to store the status codes of failed requests.
        data (dict, optional): The data to send with the request (e.g. for POST requests).

    Returns:
        tuple: A tuple containing the response time and status code of the request.
    """
    async with semaphore:
        response_time, status = await send_request(url, session, method=method, data=data)
        print(f"Request completed in {response_time} seconds with status {status}")
        results.append(response_time)
        
        if not isinstance(status, int) or status >= 400:  # Consider any 400+ status as error
            errors.append(status)
        
        return response_time, status




