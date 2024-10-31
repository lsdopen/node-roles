# Use a lightweight Python base image
FROM python:3.9-slim

# Set environment variables to avoid buffering logs in Docker
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Specify the default command to run your application
CMD ["python", "app.py"]
