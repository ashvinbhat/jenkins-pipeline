# Dockerfile for usermgmt microservice

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV FLASK_APP=userMgmt.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5003

# Set the working directory
WORKDIR /app/usermgmt

# Copy the current directory contents into the container at /app/usermgmt
COPY . /app/usermgmt

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r /app/usermgmt/requirements.txt

# Expose port 5000
EXPOSE 5003

# Define the command to run your Flask application
CMD ["python", "userMgmt.py"]
