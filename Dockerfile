# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the entry point to the Python interpreter
ENTRYPOINT ["python", "main.py"]

# Set default arguments for the entry point (these can be overridden)
CMD ["https://www.facebook.com/", "--qps", "10", "--duration", "60", "-c", "5", "--method", "GET", "steady"]
