# Start from a slim Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your server code into the container
COPY server.py .

# This is the command that will run when the container starts
CMD ["python", "server.py"]
