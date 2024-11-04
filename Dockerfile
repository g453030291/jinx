# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && apt-get update && apt-get install -y curl

# Copy the rest of the application code into the container
COPY ./api ./api

# Expose the port the app runs on
EXPOSE 8000

# Start the FastAPI application
CMD ["python3", "-m", "uvicorn", "api.index:app", "--host", "0.0.0.0", "--port", "8000"]
