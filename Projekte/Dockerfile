# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Environment variables (to be set in Coolify)
ENV AIRTABLE_API_KEY=""
ENV AIRTABLE_BASE_ID=""

# Run the script
CMD ["python", "track_projects.py"]
