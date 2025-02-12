#!/bin/sh

sudo rm -r "${DB_PATH}" "${MINIO_PATH}"
docker compose down
docker compose up --build
