# Use the official Python image from the Docker Hub
FROM python:3-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY ./api/requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app.py

# Copy the rest of your application code to the container
COPY ./api/web .

# Expose the port that the app runs on
EXPOSE 8080

# Command to run the Flask app using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]