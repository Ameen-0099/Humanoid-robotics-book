# Stage 1: Build the FastAPI application
FROM python:3.9-slim-buster as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app ./app

# Stage 2: Create a smaller runtime image
FROM python:3.9-slim-buster

WORKDIR /app

# Copy only the installed packages and application code from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /app/app ./app

# Expose the port the app runs on
EXPOSE 8000

# Run the application using Uvicorn
# Command to run on container startup
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
