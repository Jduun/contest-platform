#!/bin/sh

sudo rm -r "${DB_PATH}"
docker compose down
docker compose up --build
