---
name: observability
description: Use VictoriaLogs and VictoriaTraces MCP tools for observability data
always: true
---

# Observability Skill

You have access to VictoriaLogs and VictoriaTraces via MCP tools. Use these tools to investigate errors, trace request flows, and diagnose issues.

## Available Tools

| Tool                   | Parameters                                                                        | Description                            |
| ---------------------- | --------------------------------------------------------------------------------- | -------------------------------------- |
| `obs_logs_search`      | `query` (string), `limit` (int, default 100), `time_range` (string, default "1h") | Search VictoriaLogs using LogsQL query |
| `obs_logs_error_count` | `service` (string, optional), `time_range` (string, default "1h")                 | Count errors over a time window        |
| `obs_traces_list`      | `service` (string, optional), `limit` (int, default 20)                           | List recent traces                     |
| `obs_traces_get`       | `trace_id` (string)                                                               | Fetch a specific trace by ID           |

## Strategy Rules

### When the user asks "What went wrong?" or "Check system health" or "Diagnose the issue"

Follow this **investigation flow** in order:

1. **Check error count** in a fresh recent window:

   ```
   obs_logs_error_count(time_range="10m")
   ```

2. **Search recent error logs** to find the actual error:

   ```
   obs_logs_search(query="severity:ERROR", time_range="10m", limit=10)
   ```

3. **Extract trace_id** from the error log results — look for the `trace_id` field in any error entry.

4. **Fetch the full trace** using that trace_id:

   ```
   obs_traces_get(trace_id="<extracted_trace_id>")
   ```

5. **Summarize findings** in a single coherent explanation that includes:
   - **Log evidence**: What the error logs show (error type, message, timestamp)
   - **Trace evidence**: What the trace reveals (which spans failed, duration, affected operations)
   - **Affected service**: Name the service that failed (e.g., "Learning Management Service")
   - **Root failing operation**: The specific operation that failed (e.g., "PostgreSQL connection", "SELECT query")
   - **Key discrepancy** (if any): Note if HTTP response status doesn't match the actual error (e.g., "404 returned but root cause is DB connection failure")

**Important:** Do NOT dump raw JSON. Synthesize the evidence into a clear narrative.

### When the user asks about errors or failures (general)

1. **First**, search logs for errors:

   ```
   obs_logs_search(query="severity:ERROR", time_range="1h", limit=20)
   ```

2. **If you find errors with trace_id**, fetch the full trace:

   ```
   obs_traces_get(trace_id="...")
   ```

3. **Summarize findings** — don't dump raw JSON. Explain:
   - What went wrong
   - Which service was affected
   - When it happened
   - The request flow (from trace)

### When the user asks about a specific trace

1. **Fetch the trace**:

   ```
   obs_traces_get(trace_id="<provided_id>")
   ```

2. **Explain the span timeline**:
   - Total duration
   - Which services were involved
   - Where errors occurred (if any)

### When the user asks "what's happening" or "any issues"

1. **Check error count**:

   ```
   obs_logs_error_count(time_range="1h")
   ```

2. **If errors exist**, search for recent ones:

   ```
   obs_logs_search(query="severity:ERROR", time_range="10m", limit=10)
   ```

3. **List recent traces** to see activity:
   ```
   obs_traces_list(limit=10)
   ```

## LogsQL Query Examples

| Goal                      | Query                                                       |
| ------------------------- | ----------------------------------------------------------- |
| All errors                | `severity:ERROR`                                            |
| Errors in last 10 minutes | `_time:10m severity:ERROR`                                  |
| Errors by service         | `service.name:"Learning Management Service" severity:ERROR` |
| Specific event            | `event:"request_started"`                                   |
| By trace ID               | `trace_id:"e1ddbe285f4a879582f8f2fdd72c4e01"`               |
| Logs with exception       | `error:*`                                                   |

**Field names in this stack:**

- `severity` — log level (`ERROR`, `INFO`, `WARN`)
- `service.name` — service name (e.g., `"Learning Management Service"`)
- `trace_id` — trace ID (hex string, no dashes)
- `event` — event name (e.g., `"db_query"`, `"request_started"`)
- `_time` — timestamp
- `_msg` — short message
- `error` — error message if present

## Response Style

- **Be concise**: Lead with the key finding
- **Summarize, don't dump**: Explain what the data means
- **Use tables**: For multi-row results (top errors, trace spans)
- **Include timestamps**: When relevant
- **Highlight errors**: Make problems obvious

## Example Flows

### User: "What went wrong?" (Investigation flow)

```
You: [call obs_logs_error_count(time_range="10m")]
→ Found 5 errors in the last 10 minutes

You: [call obs_logs_search(query="severity:ERROR", time_range="10m", limit=5)]
→ Returns error logs with trace_id: e1ddbe285f4a879582f8f2fdd72c4e01

You: [call obs_traces_get(trace_id="e1ddbe285f4a879582f8f2fdd72c4e01")]
→ Returns full trace with spans

You: "**Investigation Summary:**

**Log Evidence:**
- 5 errors in the last 10 minutes
- Most recent: `socket.gaierror: [Errno -2] Name or service not known`
- Service: Learning Management Service
- Event: db_query failed

**Trace Evidence:**
- Trace ID: e1ddbe285f4a879582f8f2fdd72c4e01
- Total duration: 308ms (failed)
- Failed span: `connect` to postgres:5432 (301ms)
- HTTP span shows 404 status but root cause is DB failure

**Affected Service:** Learning Management Service

**Root Failing Operation:** PostgreSQL connection — DNS resolution failed for hostname `postgres`

**Key Discrepancy:** The HTTP response returned 404 "Items not found" but the actual error is a database connection failure. The backend error handler is misreporting DB connection errors as 404 instead of 503."
```

### User: "Any errors in the last hour?"

```
You: [call obs_logs_error_count(time_range="1h")]
→ Found 5 errors

You: [call obs_logs_search(query="severity:ERROR", time_range="1h", limit=5)]
→ Shows error details

You: "Yes, there were 5 errors in the last hour. The most recent was a connection timeout in the backend service at 14:32 UTC..."
```

### User: "Show me trace abc-123"

```
You: [call obs_traces_get(trace_id="abc-123")]
→ Returns trace with spans

You: "Here's the trace for abc-123:
- Total duration: 245ms
- Spans:
  - HTTP request (backend): 180ms
  - DB query (postgres): 65ms
  - LLM call (qwen-code-api): 120ms

All spans completed successfully."
```

### User: "The agent isn't responding"

```
You: [call obs_logs_search(query="severity:ERROR _time:5m", limit=10)]
→ Check for recent errors

You: [call obs_traces_list(service="Learning Management Service", limit=5)]
→ Check recent traces

You: "I found 3 failed requests in the last 5 minutes. The errors show 'connection refused' when trying to reach the database..."
```

## Error Handling

- **If a tool fails**, explain what went wrong
- **If no results**, suggest broadening the time range or query
- **If trace not found**, it may have expired (retention is 7 days)
