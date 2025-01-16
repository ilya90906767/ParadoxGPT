# Use an official Python image as a base
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file
COPY ../requirements.txt .

RUN pip install --upgrade pip
# Install dependencies
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose the port
EXPOSE 8000