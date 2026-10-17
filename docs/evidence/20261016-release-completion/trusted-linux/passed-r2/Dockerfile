FROM node:22-bookworm-slim AS node
FROM python:3.13-bookworm
COPY --from=node /usr/local/bin/node /usr/local/bin/node
RUN apt-get update && apt-get install -y --no-install-recommends \
 libgl1 libegl1 libxrender1 libxi6 libxfixes3 libxkbcommon0 \
 libsm6 libice6 libwayland-client0 && rm -rf /var/lib/apt/lists/*
RUN python -m pip install --no-cache-dir pytest jsonschema bpy==5.2.1
RUN python -I -c 'import bpy, pytest, jsonschema; assert bpy.app.version == (5, 2, 1)'
RUN node --version && python --version && python -m pip freeze
