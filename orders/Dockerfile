# Dockerfile for orderMgmt microservice

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV FLASK_APP=ordermgmt.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5001

# Set the working directory
WORKDIR /app/ordermgmt

# Copy the current directory contents into the container at /app/ordermgmt
COPY . /app/ordermgmt

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r /app/ordermgmt/requirements.txt

# Expose port 5001
EXPOSE 5001

# Define the command to run your Flask application
CMD ["python", "orderMgmt.py"]
