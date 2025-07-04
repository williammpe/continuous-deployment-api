#!/bin/bash

CONTAINER="api"

echo "Reiniciando ${CONTAINER}..."

docker compose -f "/app/projects/${CONTAINER}/docker-compose.yaml" up --force-recreate --no-deps -d

echo "${CONTAINER} iniciado!"
