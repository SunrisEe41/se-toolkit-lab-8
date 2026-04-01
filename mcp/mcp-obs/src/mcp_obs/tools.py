"""Tool schemas, handlers, and registry for the Observability MCP server."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from mcp.types import Tool
from pydantic import BaseModel, Field

from mcp_obs.client import ObsClient


class LogSearchQuery(BaseModel):
    query: str = Field(
        description="LogsQL query string, e.g. 'severity:ERROR service.name:\"backend\"'"
    )
    limit: int = Field(default=100, ge=1, le=1000, description="Max results to return")
    time_range: str = Field(
        default="1h", description="Time range like '1h', '10m', '24h'"
    )


class LogErrorCountQuery(BaseModel):
    service: str | None = Field(
        default=None, description="Service name to filter (optional)"
    )
    time_range: str = Field(
        default="1h", description="Time window like '1h', '10m', '24h'"
    )


class TracesListQuery(BaseModel):
    service: str | None = Field(
        default=None, description="Service name to filter (optional)"
    )
    limit: int = Field(default=20, ge=1, le=100, description="Max traces to return")


class TraceByIdQuery(BaseModel):
    trace_id: str = Field(description="Trace ID (UUID format)")


ToolPayload = BaseModel | list[BaseModel]
ToolHandler = Callable[[ObsClient, BaseModel], Awaitable[ToolPayload]]


@dataclass(frozen=True, slots=True)
class ToolSpec:
    name: str
    description: str
    model: type[BaseModel]
    handler: ToolHandler

    def as_tool(self) -> Tool:
        schema = self.model.model_json_schema()
        schema.pop("$defs", None)
        schema.pop("title", None)
        return Tool(name=self.name, description=self.description, inputSchema=schema)


async def _logs_search(client: ObsClient, args: BaseModel) -> ToolPayload:
    query = args if isinstance(args, LogSearchQuery) else LogSearchQuery.model_validate(
        args
    )
    return await client.logs_search(query.query, query.limit, query.time_range)


async def _logs_error_count(client: ObsClient, args: BaseModel) -> ToolPayload:
    query = (
        args if isinstance(args, LogErrorCountQuery) else LogErrorCountQuery.model_validate(args)
    )
    return await client.logs_error_count(query.service, query.time_range)


async def _traces_list(client: ObsClient, args: BaseModel) -> ToolPayload:
    query = (
        args if isinstance(args, TracesListQuery) else TracesListQuery.model_validate(args)
    )
    return await client.traces_list(query.service, query.limit)


async def _traces_get(client: ObsClient, args: BaseModel) -> ToolPayload:
    query = (
        args if isinstance(args, TraceByIdQuery) else TraceByIdQuery.model_validate(args)
    )
    result = await client.traces_get(query.trace_id)
    return result if result else {"error": "Trace not found"}


TOOL_SPECS = (
    ToolSpec(
        "obs_logs_search",
        "Search VictoriaLogs using LogsQL query. Use severity:ERROR for errors, service.name for filtering by service.",
        LogSearchQuery,
        _logs_search,
    ),
    ToolSpec(
        "obs_logs_error_count",
        "Count errors in VictoriaLogs over a time window. Optionally filter by service name.",
        LogErrorCountQuery,
        _logs_error_count,
    ),
    ToolSpec(
        "obs_traces_list",
        "List recent traces from VictoriaTraces. Optionally filter by service name.",
        TracesListQuery,
        _traces_list,
    ),
    ToolSpec(
        "obs_traces_get",
        "Fetch a specific trace by ID from VictoriaTraces. Shows full span timeline.",
        TraceByIdQuery,
        _traces_get,
    ),
)
TOOLS_BY_NAME = {spec.name: spec for spec in TOOL_SPECS}
