# Start your image with a node base image
FROM python:3.9-slim

# The /app directory should act as the main application directory
WORKDIR /app


# Copy local directories to the current local directory of our docker image (/app)
COPY requirements.txt ./
COPY app/ ./app
COPY configs/ ./configs
COPY database/ ./database
COPY models/ ./models
COPY RAG/ ./RAG
COPY vectorstores/ ./vectorstores

# Install node packages, install serve, build the app, and remove dependencies at the end
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000

# Start the app using serve command
CMD ["python", "app/main.py"]