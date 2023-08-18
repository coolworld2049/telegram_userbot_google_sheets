#!/usr/bin/env bash

source ./.env

startup() {
  echo "$(openssl rand -hex 64)" > api_key.txt
  echo "API key generated and saved to api_key.txt"

  docker build -t telegram_userbot_google_sheets .
  docker run -it -d \
    --name telegram_userbot_google_sheets \
    --hostname telegram_userbot_google_sheets \
    --env-file .env \
    -p 80:80 \
    -e MAX_WORKERS=1 \
    -e HOST=0.0.0.0 \
    -e PORT=80 \
    -e SESSION_STRING_FILE=./session_maker/my.txt \
    telegram_userbot_google_sheets:latest
}

dev() {
  echo "NotImplemented"
}
shutdown() {
  rm api_key.txt
  docker kill telegram_userbot_google_sheets
  docker rm telegram_userbot_google_sheets
  docker rmi telegram_userbot_google_sheets
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