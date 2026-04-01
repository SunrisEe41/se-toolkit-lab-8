"""HTTP client for VictoriaLogs and VictoriaTraces APIs."""

from __future__ import annotations

import httpx


class ObsClient:
    """Client for VictoriaLogs and VictoriaTraces APIs."""

    def __init__(self, victorialogs_url: str, victoriatraces_url: str) -> None:
        self.victorialogs_url = victorialogs_url.rstrip("/")
        self.victoriatraces_url = victoriatraces_url.rstrip("/")
        self._http_client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._http_client is None or self._http_client.is_closed:
            self._http_client = httpx.AsyncClient(timeout=30.0)
        return self._http_client

    async def close(self) -> None:
        if self._http_client is not None and not self._http_client.is_closed:
            await self._http_client.aclose()
            self._http_client = None

    async def __aenter__(self) -> ObsClient:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def logs_search(
        self, query: str, limit: int = 100, time_range: str = "1h"
    ) -> list[dict]:
        """Search VictoriaLogs using LogsQL query."""
        client = await self._get_client()
        url = f"{self.victorialogs_url}/select/logsql/query"
        params = {"query": query, "limit": limit}
        if time_range:
            params["_time"] = time_range
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    async def logs_error_count(
        self, service: str | None = None, time_range: str = "1h"
    ) -> dict:
        """Count errors in VictoriaLogs over a time window."""
        client = await self._get_client()
        # VictoriaLogs requires time filter in the query itself for stats
        query = f"_time:{time_range} severity:ERROR | stats count()"
        if service:
            query = f'_time:{time_range} service.name:"{service}" severity:ERROR | stats count()'
        url = f"{self.victorialogs_url}/select/logsql/stats_query"
        params = {"query": query}
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    async def traces_list(
        self, service: str | None = None, limit: int = 20
    ) -> list[dict]:
        """List recent traces from VictoriaTraces."""
        client = await self._get_client()
        url = f"{self.victoriatraces_url}/select/jaeger/api/traces"
        params = {"limit": limit}
        # VictoriaTraces requires service parameter
        if service:
            params["service"] = service
        else:
            # Use a common service if none specified
            params["service"] = "Learning Management Service"
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("data", []) if isinstance(data, dict) else data

    async def traces_get(self, trace_id: str) -> dict | None:
        """Fetch a specific trace by ID from VictoriaTraces."""
        client = await self._get_client()
        url = f"{self.victoriatraces_url}/select/jaeger/api/traces/{trace_id}"
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict):
            return data.get("data", {})
        return None
