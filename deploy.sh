#!/bin/bash

git pull --rebase

# Network name
NETWORK_NAME="flix_network"

# Check if the network already exists
if ! docker network inspect "$NETWORK_NAME" >/dev/null 2>&1; then
  echo "Creating network $NETWORK_NAME..."
  docker network create "$NETWORK_NAME"
else
  echo "Network $NETWORK_NAME already exists."
fi

# Container name
CONTAINER_NAME="flix-api"

# Function to check if a container is running
is_container_running() {
  container_name=$1
  if [ "$(docker ps -q -f name=$container_name)" ]; then
    return 0
  else
    return 1
  fi
}

# Build the image from the Dockerfile
docker build -t $CONTAINER_NAME -f Dockerfile .

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

# Start the db container if it's not running
if ! is_container_running "db"; then
  echo "Starting db container..."
  docker run -d \
    --name db \
    --restart always \
    --env-file .env \
    -p 5432:5432 \
    --expose 5432 \
    -v $(pwd)/data:/var/lib/postgresql/data \
    --network $NETWORK_NAME \
    postgres
else
  echo "db container is already running."
fi

# Start the redis container if it's not running
if ! is_container_running "redis"; then
  echo "Starting redis container..."
  docker run -d \
    --name redis \
    --restart always \
    -p 6379:6379 \
    --network $NETWORK_NAME \
    redis
else
  echo "redis container is already running."
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
  --network $NETWORK_NAME \
  $CONTAINER_NAME

echo "Container $CONTAINER_NAME has been successfully started."
