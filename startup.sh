#!/bin/bash

echo "Start up!"

echo "Start Docker Containers"
docker compose up -d

sed -i.bak 's/from models/#from models/g' ./utils/scheduler/hbd.py
./.venv/bin/python3 -m alembic upgrade head
mv ./utils/scheduler/hbd.py.bak ./utils/scheduler/hbd.py

echo "Start Bot"
./.venv/bin/python3 ./run.py
