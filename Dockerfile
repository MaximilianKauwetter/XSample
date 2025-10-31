# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file first to leverage Docker layer caching
COPY requirements.txt .

# Install the dependencies
# --no-cache-dir: Disables the pip cache, keeping the image layer smaller.
# -r requirements.txt: Installs all packages listed in the file.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY src/ .

# Expose port 5000. This is the port Gunicorn will run on.
EXPOSE 5000

# Define the command to run the app when the container starts.
# We use Gunicorn, a production-ready WSGI server.
# --bind 0.0.0.0:5000: Binds to all network interfaces on port 5000.
# --timeout 300: Sets the worker timeout to 300 seconds (default is 30).
# --access-logfile -: Logs all access requests to stdout (visible in 'docker logs').
# app:app: Tells Gunicorn to run the 'app' object (our Flask app)
#          found in the 'main.py' module.
CMD ["gunicorn", "--bind", "0.0.0.0:5000","--timeout", "300","--access-logfile", "-", "main:app"]