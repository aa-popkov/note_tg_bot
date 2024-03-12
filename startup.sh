#!/bin/bash

echo "Start up!"

echo "Start Docker Containers"
docker-compose up -d

echo "Start Bot"
./.venv/bin/python3 ./run.py
