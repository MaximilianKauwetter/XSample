# Stock Stats API

A simple Flask API to fetch stock statistics using yfinance, containerized with Docker.
Prerequisites
Before you begin, ensure you have Docker installed on your system.
You must have the following files in your directory:
app.py (the Python Flask app)
requirements.txt (the Python dependencies)
Dockerfile (provided in this repository)
Installation and Startup
Follow these steps to build the Docker image and run the container.

## 1. Build the Docker Image

Open your terminal in the directory containing the Dockerfile and other app files. Run the following command to build the image:

> docker build -t stock-api .
- 'docker build' creates an image
- '-t stock-api' tags the image with the name 'stock-api'
- '.' specifies that the Dockerfile is in the current directory

## 2. Run the Docker Container

Once the image is built, you can run it as a container:
> docker run -d -p 5000:5000 --name stock-api-container stock-api
- 'docker run' starts a container from an image
- '-d' runs the container in detached mode (in the background)
- '-p 5000:5000' maps port 5000 on your local machine to port 5000 in the container
- '--name stock-api-container' gives your container a friendly name
- 'stock-api' is the name of the image to run

The API is now running and accessible on your local machine.

## How to Use the API:
### Example Request:

Use curl or your web browser to access the endpoint.
> curl "http://localhost:5000/api/stats?ticker=MSFT&start=2023-01-01&end=2023-12-31"


### Example Response:
> {
  "average_close_price": 320.53,
  "last_close_price": 376.04,
  "period_high": 384.3,
  "period_low": 221.39
}

### Stop the container
> docker stop stock-api-container

### (Optional) Remove the container
> docker rm stock-api-container
