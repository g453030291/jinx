# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install opencv dependencies and any needed packages specified in requirements.txt
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg libgl1-mesa-glx libglib2.0-0 curl iputils-ping && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code into the container
COPY ./api ./api

# Expose the port the app runs on
EXPOSE 8000

# Start the FastAPI application
CMD ["python3", "-m", "uvicorn", "api.index:app", "--host", "0.0.0.0", "--port", "8000"]