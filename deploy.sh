#!/bin/bash

# Container name
CONTAINER_NAME="api"

# Build the image from the Dockerfile
docker build -t api-image -f Dockerfile .

# Check if the container is running
if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    echo "The container $CONTAINER_NAME is running. Stopping and removing the container..."
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
elif [ "$(docker ps -aq -f status=exited -f name=$CONTAINER_NAME)" ]; then
    # Check if the container exists but is stopped
    echo "The container $CONTAINER_NAME exists but is stopped. Removing the container..."
    docker rm $CONTAINER_NAME
fi

# Run the new container with the same configuration as in docker-compose
echo "Starting a new container..."
docker run -d \
  --name $CONTAINER_NAME \
  --restart always \
  -p 8000:8000 \
  -v $(pwd):/app \
  --env-file .env \
  --log-driver json-file \
  --log-opt max-file=1 \
  --log-opt max-size=10m \
  api-image

echo "Container $CONTAINER_NAME has been successfully started."
