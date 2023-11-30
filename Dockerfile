# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /market-stream

# Copy the current directory contents into the container at /app
COPY . /market-stream

# Install any needed packages specified in requirements.txt
# Assuming you have a requirements.txt file with grpcio and other dependencies
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/market-stream

# Make port 50051 available to the world outside this container
EXPOSE 50051

# Run the gRPC server when the container launches
CMD ["python", "main.py"]