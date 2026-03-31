# nanobot Dockerfile - multi-stage build with uv (Task 2 Part A only)
# Pattern: backend/Dockerfile

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

# Copy root workspace files for dependency resolution
COPY --from=workspace pyproject.toml uv.lock ./

# Copy mcp-lms source (required for editable install)
COPY --from=workspace mcp/mcp-lms ./mcp/mcp-lms

# Copy nanobot package files
COPY nanobot/pyproject.toml ./nanobot/pyproject.toml
COPY nanobot/entrypoint.py ./nanobot/entrypoint.py

# Sync dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --package nanobot

# Copy the rest of nanobot package
COPY nanobot/ ./nanobot/

# ---
# Stage 2: Final image without uv
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm

# Set environment variables for Python and application
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Accept build args for non-root user
ARG APP_UID=1000
ARG APP_GID=1000

# Setup a non-root user with configurable UID/GID
RUN groupadd --system --gid ${APP_GID} appgroup \
    && useradd --system --gid ${APP_GID} --uid ${APP_UID} --create-home appuser

# Copy the application from the builder
COPY --from=builder --chown=appuser:appgroup /app /app

# Create writable workspace directories for cron and other runtime data
RUN mkdir -p /app/nanobot/workspace/cron /app/nanobot/workspace/memory \
    && chmod -R 777 /app/nanobot/workspace

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Use the non-root user to run our application
USER appuser

WORKDIR /app

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:18790/health')" || exit 1

# Run the entrypoint
CMD ["python", "/app/nanobot/entrypoint.py"]
