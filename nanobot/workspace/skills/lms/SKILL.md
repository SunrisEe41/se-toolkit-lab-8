---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

You have access to the LMS (Learning Management System) via MCP tools. Use these tools to fetch live course data about labs, learners, scores, and progress.

## Available Tools

| Tool | Parameters | Description |
|------|------------|-------------|
| `lms_health` | none | Check if the LMS backend is healthy and report the item count |
| `lms_labs` | none | List all labs available in the LMS |
| `lms_learners` | none | List all learners registered in the LMS |
| `lms_pass_rates` | `lab` (string) | Get pass rates (avg score and attempt count per task) for a lab |
| `lms_timeline` | `lab` (string) | Get submission timeline (date + submission count) for a lab |
| `lms_groups` | `lab` (string) | Get group performance (avg score + student count per group) for a lab |
| `lms_top_learners` | `lab` (string), `limit` (int, default 5) | Get top learners by average score for a lab |
| `lms_completion_rate` | `lab` (string) | Get completion rate (passed / total) for a lab |
| `lms_sync_pipeline` | none | Trigger the LMS sync pipeline. May take a moment |

## Strategy Rules

### When a lab parameter is needed but not provided

If the user asks for **scores, pass rates, completion, groups, timeline, or top learners** without naming a lab:

1. **First**, call `lms_labs` to get the list of available labs
2. **If multiple labs exist**, ask the user to choose one using the shared structured-ui layer
3. **Use each lab's `title` field** as the default user-facing label
4. **Pass the lab's `id` or `name`** (whichever the tool expects) when calling the actual tool

Example flow:
```
User: "Show me the pass rates"
You: [call lms_labs] → get list of labs
You: [present choices via structured-ui if multiple labs] → user selects "lab-04"
You: [call lms_pass_rates with lab="lab-04"] → return formatted results
```

### Formatting results

- **Percentages**: Display as "XX%" (e.g., "75%" not "0.75")
- **Counts**: Use plain numbers with labels (e.g., "128 submissions")
- **Scores**: Show as percentage or fraction as appropriate
- **Tables**: Use markdown tables for multi-row data (top learners, groups, timeline)
- **Keep responses concise**: Lead with the key insight, then show details

### When asked "what can you do?"

Explain your capabilities clearly:

> I can access live data from the Learning Management System. I can:
> - List available labs and learners
> - Show pass rates, completion rates, and submission timelines for any lab
> - Display group performance and top learners per lab
> - Check the LMS backend health
> - Trigger a sync pipeline refresh
>
> Just ask about a specific lab or say "what labs are available?" to get started.

## Tool Selection Guide

| User asks for... | Use this tool |
|------------------|---------------|
| "Is the LMS working?" | `lms_health` |
| "What labs exist?" / "available labs" | `lms_labs` |
| "Who is enrolled?" / "all learners" | `lms_learners` |
| "Pass rates" / "average scores" | `lms_pass_rates` (needs lab) |
| "When did people submit?" / "timeline" | `lms_timeline` (needs lab) |
| "Group performance" / "groups" | `lms_groups` (needs lab) |
| "Best students" / "top learners" | `lms_top_learners` (needs lab) |
| "Completion rate" / "how many finished" | `lms_completion_rate` (needs lab) |
| "Refresh the data" / "sync" | `lms_sync_pipeline` |

## Integration with Structured UI

This skill works with the shared `structured-ui` skill for presenting choices:

- When you need the user to pick a lab, call `lms_labs` first
- Extract each lab's `title` (or `name` if no title) as the display label
- Extract each lab's `id` (or `name`) as the value to pass back
- Let the structured-ui skill decide how to present the choice (buttons, menu, etc.)
- Once the user selects, use that value in subsequent tool calls

## Error Handling

- If a tool fails, explain what went wrong in plain language
- If a lab ID is invalid, suggest calling `lms_labs` to see valid options
- If the LMS is unreachable, mention that the backend may be down
