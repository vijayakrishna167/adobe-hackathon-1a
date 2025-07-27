# Step 1: Base Image
# Use a slim, official Python image to keep the size down.
# Specify the platform as required by the hackathon rules.
FROM --platform=linux/amd64 python:3.11-slim

# Step 2: Set Working Directory
# This creates a directory inside the container for our application.
WORKDIR /app

# Step 3: Copy requirements file
# Copy the list of dependencies first for better Docker layer caching.
COPY requirements.txt .

# Step 4: Install Dependencies
# This step requires internet access during the 'docker build' process.
# We only need PyMuPDF for this project.
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy Application Code
# Copy our source code into the container's working directory.
COPY src/ ./src/
COPY run.py .

# Step 6: Set Default Command
# This command runs automatically when the container starts.
# It executes our main script to process all PDFs in the /app/input directory.
CMD ["python", "run.py"]
