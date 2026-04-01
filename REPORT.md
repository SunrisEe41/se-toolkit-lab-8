# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

<!-- Paste the agent's response to "What is the agentic loop?" and "What labs are available in our LMS?" -->
The agentic loop is the core reasoning cycle that autonomous AI agents use to accomplish tasks. It  
consists of four main stages that repeat until a goal is achieved:

The Loop

 1 Perceive — Take in information from the environment (user input, tool results, file contents, API
   responses)
 2 Reason — Process the information, evaluate options, and decide what to do next
 3 Act — Execute actions using available tools (read/write files, run commands, make API calls, send
   messages)
 4 Observe — Receive feedback from the actions (outputs, errors, state changes)

Then the loop repeats with the new information.

Visual Flow

 Perceive → Reason → Act → Observe → (back to Perceive)

Why It Matters

This loop enables agents to:

 • Break complex tasks into manageable steps
 • Adapt when things don't go as planned
 • Learn from feedback and adjust strategy
 • Work autonomously toward a goal

As nanobot, I follow this loop for every task you give me. For example, if you ask me to "set up a  
project," I'll perceive your request, reason about the steps needed, act by creating files and
running commands, observe the results, and continue until the project is set up.

Based on the workspace, Lab 8 — The Agent is the Interface is the available lab in this LMS.

Required Tasks:

 Task  Description
 ─────────────────────────────────────────────────────────────────────────────────────
 1     Set Up the Agent — install nanobot, configure Qwen API, add MCP tools
 2     Deploy and Connect a Web Client — Dockerize nanobot, add WebSocket + Flutter UI
 3     Give the Agent New Eyes — build log/trace MCP tools for observability
 4     Diagnose a Failure — investigate, schedule health checks, fix a bug

Optional Tasks:

 Task  Description
 ─────────────────────────────────────────────────────────────────
 1     Add a Telegram Bot Client — same agent, different interface

The LMS backend provides APIs for items, interactions, and learners, backed by PostgreSQL. The lab  
focuses on building nanobot as an AI agent interface to query this system and observability data.

Would you like details on a specific task?

## Task 1B — Agent with LMS tools

<!-- Paste the agent's response to "What labs are available?" and "Describe the architecture of the LMS system" -->
Here are the available labs:

 1 Lab 01 – Products, Architecture & Roles
 2 Lab 02 — Run, Fix, and Deploy a Backend Service
 3 Lab 03 — Backend API: Explore, Debug, Implement, Deploy
 4 Lab 04 — Testing, Front-end, and AI Agents
 5 Lab 05 — Data Pipeline and Analytics Dashboard
 6 Lab 06 — Build Your Own Agent
 7 Lab 07 — Build a Client with an AI Coding Agent
 8 lab-08

Is there a specific lab you'd like to explore or get more information about?

Yes, the LMS backend is healthy. It currently has 56 items in the system and no errors reported.

## Task 1C — Skill prompt

<!-- Paste the agent's response to "Show me the scores" (without specifying a lab) -->
I'll help you check the scores. First, let me see what labs are available in the LMS.
2026-03-31 18:29:43.262 | INFO     | nanobot.agent.loop:_prepare_tools:253 - Tool call: mcp_lms_lms_labs({})

🐈 nanobot
There are 8 labs available. Which lab would you like to see the scores for? Here are the options:

 1 Lab 01 – Products, Architecture & Roles
 2 Lab 02 — Run, Fix, and Deploy a Backend Service
 3 Lab 03 — Backend API: Explore, Debug, Implement, Deploy
 4 Lab 04 — Testing, Front-end, and AI Agents
 5 Lab 05 — Data Pipeline and Analytics Dashboard
 6 Lab 06 — Build Your Own Agent
 7 Lab 07 — Build a Client with an AI Coding Agent
 8 lab-08

Please let me know which lab you're interested in, or if you'd like to see scores for all labs.

## Task 2A — Deployed agent

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->
nanobot-1  | ✓ Channels enabled: webchat
nanobot-1  | ✓ Heartbeat: every 1800s
nanobot-1  | 2026-04-01 16:52:09.448 | INFO     | nanobot.cron.service:_load_store:85 - Cron: jobs.json modified externally, reloading
nanobot-1  | 2026-04-01 16:52:09.448 | INFO     | nanobot.cron.service:start:202 - Cron service started with 0 jobs
nanobot-1  | 2026-04-01 16:52:09.448 | INFO     | nanobot.heartbeat.service:start:124 - Heartbeat started (every 1800s)
nanobot-1  | 2026-04-01 16:52:09.783 | INFO     | nanobot.channels.manager:start_all:91 - Starting webchat channel...
nanobot-1  | 2026-04-01 16:52:09.783 | INFO     | nanobot.channels.manager:_dispatch_outbound:119 - Outbound dispatcher started
nanobot-1  | 2026-04-01 16:52:11.451 | DEBUG    | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_health' from server 'lms'
nanobot-1  | 2026-04-01 16:52:11.451 | DEBUG    | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_labs' from server 'lms'
nanobot-1  | 2026-04-01 16:52:11.451 | DEBUG    | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_learners' from server 'lms'
nanobot-1  | 2026-04-01 16:52:11.451 | DEBUG    | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_pass_rates' from server 'lms'
nanobot-1  | 2026-04-01 16:52:11.451 | DEBUG    | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_timeline' from server 'lms'
nanobot-1  | 2026-04-01 16:52:11.451 | DEBUG    | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_groups' from server 'lms'
nanobot-1  | 2026-04-01 16:52:11.451 | DEBUG    | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_top_learners' from server 'lms'
nanobot-1  | 2026-04-01 16:52:11.451 | DEBUG    | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_completion_rate' from server 'lms'
nanobot-1  | 2026-04-01 16:52:11.451 | DEBUG    | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_sync_pipeline' from server 'lms'
nanobot-1  | 2026-04-01 16:52:11.451 | INFO     | nanobot.agent.tools.mcp:connect_mcp_servers:246 - MCP server 'lms': connected, 9 tools registered
nanobot-1  | 2026-04-01 16:52:12.990 | DEBUG    | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_mcp_webchat_ui_message' from server 'mcp_webchat'
nanobot-1  | 2026-04-01 16:52:12.991 | INFO     | nanobot.agent.tools.mcp:connect_mcp_servers:246 - MCP server 'mcp_webchat': connected, 1 tools registered
nanobot-1  | 2026-04-01 16:52:12.991 | INFO     | nanobot.agent.loop:run:280 - Agent loop started

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->
![alt text](image-2.png)
Connected to Nanobot!

Start by asking:
• What can you do in this system?
• What tools do you have right now?
• Ask one question about the LMS or the system state.

I am more than a chat UI only when the agent has tools, skills, and memory. Try discovering those capabilities from the conversation itself.

Show me the scores

I see there are 8 labs available. Please let me know which lab you'd like to see the scores for:

1. **Lab 01** – Products, Architecture & Roles
2. **Lab 02** — Run, Fix, and Deploy a Backend Service
3. **Lab 03** — Backend API: Explore, Debug, Implement, Deploy
4. **Lab 04** — Testing, Front-end, and AI Agents
5. **Lab 05** — Data Pipeline and Analytics Dashboard
6. **Lab 06** — Build Your Own Agent
7. **Lab 07** — Build a Client with an AI Coding Agent
8. **lab-08**

Just tell me the lab number (e.g., "lab-04" or "Lab 04") and I'll show you the scores!

What can you do in this system?

I'm **nanobot 🐈**, your AI assistant. Here's what I can do in this system:

## 📚 Learning Management System (LMS)

I can access live course data:

- List available labs and enrolled learners
- Show **pass rates**, **completion rates**, and **submission timelines** for any lab
- Display **group performance** and **top learners** per lab
- Check LMS backend health and trigger data syncs

## 📁 File & Workspace Management

- Read, write, and edit files in your workspace
- List directory contents and explore project structure
- Execute shell commands (with safety limits)

## 🌐 Web Access

- Search the web for information
- Fetch and extract content from URLs

## ⏰ Scheduling & Reminders

- Create one-time or recurring reminders via `cron`
- Manage periodic tasks through `HEARTBEAT.md`

## 💬 Interactive UI (WebChat)

- Present structured choices and confirmations when you need to pick options

## 🧠 Memory System

- Store important facts in `MEMORY.md` (long-term)
- Log events in `HISTORY.md` (searchable event log)

## 🛠️ Skills

I have access to extensible skills including:

- **lms** – Course data and analytics
- **memory** – Two-layer memory with grep-style recall
- **cron** – Scheduled reminders and recurring tasks
- **structured-ui** – Interactive choice messages
- **clawhub** – Search and install new skills
- **skill-creator** – Create or update agent skills

---

**What would you like to do?** For example:

- "Show me the pass rates for lab-04"
- "Who are the top learners in lab-02?"
- "Set a reminder for tomorrow at 3pm"
- "What labs are available?"

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
