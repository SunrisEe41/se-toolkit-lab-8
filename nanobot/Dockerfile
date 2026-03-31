# nanobot Dockerfile - multi-stage build with uv
# Runs as root for simplicity (HOST_UID/GID handled by docker-compose user setting)

# ---
# Stage 1: Build the application in the /app directory
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Omit development dependencies
ENV UV_NO_DEV=1

# Disable Python downloads
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Copy nanobot files
COPY pyproject.toml ./pyproject.toml
COPY entrypoint.py ./entrypoint.py

# Copy mcp-lms for the editable install (from workspace context)
COPY --from=workspace mcp/mcp-lms ./mcp/mcp-lms

# Rewrite mcp-lms workspace source to direct path for Docker build
RUN sed -i 's|mcp-lms = { workspace = true, editable = true }|mcp-lms = { path = "mcp/mcp-lms", editable = true }|' pyproject.toml

# Sync nanobot dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# ---
# Stage 2: Final image without uv
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm

# Set environment variables for Python and application
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

WORKDIR /app

# Copy the application from the builder
COPY --from=builder /app /app

# Create writable directories for nanobot runtime (writable by any user for docker-compose volume mounts)
RUN mkdir -p /app/nanobot/workspace/memory \
    && mkdir -p /app/nanobot/workspace/sessions \
    && mkdir -p /app/nanobot/workspace/cron \
    && chmod -R 777 /app/nanobot/workspace

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:18790/health')" || exit 1

# Run the entrypoint
CMD ["python", "/app/nanobot/entrypoint.py"]
