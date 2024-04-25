# Dockerfile for productmgmt microservice

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV FLASK_APP=productmgmt.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5002

# Set the working directory
WORKDIR /app/productmgmt

# Copy the current directory contents into the container at /app/productmgmt
COPY . /app/productmgmt

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r /app/productmgmt/requirements.txt

# Expose port 5002
EXPOSE 5002

# Define the command to run your Flask application
CMD ["python", "productmgmt.py"]
