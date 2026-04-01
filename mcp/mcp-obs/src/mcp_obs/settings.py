"""Settings for MCP observability server."""

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ObsSettings:
    """Observability service settings."""

    victorialogs_url: str
    victoriatraces_url: str


def resolve_settings() -> ObsSettings:
    """Resolve settings from environment variables."""
    victorialogs_url = os.environ.get(
        "NANOBOT_VICTORIALOGS_URL", "http://localhost:9428"
    )
    victoriatraces_url = os.environ.get(
        "NANOBOT_VICTORIATRACES_URL", "http://localhost:10428"
    )
    return ObsSettings(
        victorialogs_url=victorialogs_url,
        victoriatraces_url=victoriatraces_url,
    )
