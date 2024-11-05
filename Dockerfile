FROM python:3.13.0-slim

ENV PYTHONUNBUFFERED=1

# Working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# default command to run your application
CMD ["python", "app.py"]
