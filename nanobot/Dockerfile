# nanobot Dockerfile - multi-stage build with uv

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

# Install gosu for user switching
RUN apt-get update && apt-get install -y --no-install-recommends gosu && rm -rf /var/lib/apt/lists/*

# Accept build args for user IDs
ARG APP_UID=1000
ARG APP_GID=1000

# Create user with specified IDs
RUN groupadd --system --gid "${APP_GID}" appuser \
    && useradd --system --gid "${APP_GID}" --uid "${APP_UID}" --create-home appuser

# Copy the application from the builder
COPY --from=builder --chown=appuser:appuser /app /app

# Create writable directories for nanobot runtime
RUN mkdir -p /app/nanobot/workspace/memory \
    && mkdir -p /app/nanobot/workspace/sessions \
    && chown -R appuser:appuser /app/nanobot

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Use /app as working directory
WORKDIR /app

# Switch to non-root user
USER appuser

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:18790/health')" || exit 1

# Run the entrypoint
CMD ["python", "/app/nanobot/entrypoint.py"]