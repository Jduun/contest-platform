#!/bin/sh

chmod -R a+w ./migrations
chmod a+w ./alembic.ini
alembic upgrade head
uvicorn src.main:app --host 0.0.0.0 --port "${BACKEND_PORT}" --root-path /api --reload
