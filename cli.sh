#!/usr/bin/env bash

source ./.env

startup() {
  docker build -t telegram-bot .
  docker run -it --rm -d \
    --name telegram-bot \
    --hostname telegram-bot \
    --env-file .env \
    -e MAX_WORKERS=1 \
    -e CONFIRM_CODE
    -p 8000:80 \
    --restart no \
    telegram-bot:latest
}

dev() {
  docker-compose -f docker-compose.dev.yml up -d
}
shutdown() {
  docker-compose down --rmi local --remove-orphans
}

print_usage() {
  echo "Usage: $0 [OPTION]"
  echo "Options:"
  echo "  startup           Bring up containers using Docker Compose"
  echo "  shutdown          Remove containers, images"
  echo "  dev               development mode"
  echo "  --help            Display this help message"
}

# Parse command-line options
if [[ $# -eq 0 ]]; then
  print_usage
  exit 1
fi

case $1 in
startup)
  startup
  ;;
shutdown)
  shutdown
  ;;
dev)
  dev
  ;;
--help)
  print_usage
  ;;
*)
  echo "Invalid option: $1"
  print_usage
  exit 1
  ;;
esac

cd ..