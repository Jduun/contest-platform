#!/bin/sh

# Uncomment this if you want to delete all data
# if [ -f .env ]; then
#   set -a
#   . ./.env
#   set +a
# fi
# sudo rm -r "${DB_PATH}" "${MINIO_PATH}"

docker compose down
docker compose up --build
