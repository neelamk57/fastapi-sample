# Use the official Python image
FROM python:3.10.12

# Set the working directory in the container
WORKDIR /app

RUN pip install --upgrade pip

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Expose the port that FastAPI will run on
EXPOSE 8001
# Expose the ports for both HTTP and HTTPS
# EXPOSE 80
# EXPOSE 443

# # Command to run the application with HTTPS
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "443", "--ssl-keyfile", "/app/ssl/key.pem", "--ssl-certfile", "/app/ssl/cert.pem"]

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--proxy-headers"]




# # Copy your SSL key and certificate files into the container (replace with your actual file names)
# COPY path/to/key.pem /app/key.pem
# COPY path/to/cert.pem /app/cert.pem

# # Run the application with Uvicorn over HTTPS
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--ssl-keyfile", "/app/key.pem", "--ssl-certfile", "/app/cert.pem"]