#!/usr/bin/env python3
"""
Entrypoint for nanobot gateway in Docker.

Resolves environment variables into config at runtime, then launches nanobot gateway.

Environment variables read:
    - LLM_API_KEY -> providers.custom.apiKey
    - LLM_API_BASE_URL -> providers.custom.apiBase
    - LLM_API_MODEL -> agents.defaults.model
    - NANOBOT_GATEWAY_CONTAINER_ADDRESS -> gateway.host
    - NANOBOT_GATEWAY_CONTAINER_PORT -> gateway.port
    - NANOBOT_WEBCHAT_CONTAINER_ADDRESS -> channels.webchat.host
    - NANOBOT_WEBCHAT_CONTAINER_PORT -> channels.webchat.port
    - NANOBOT_LMS_BACKEND_URL -> tools.mcpServers.lms.args[2] and env
    - NANOBOT_LMS_API_KEY -> tools.mcpServers.lms.env
    - NANOBOT_ACCESS_KEY -> channels.webchat.accessKey
"""

import json
import os
import sys
from pathlib import Path


def resolve_config() -> tuple[str, str]:
    """Read config.json, override with env vars, write resolved config."""
    # Determine paths
    script_dir = Path(__file__).parent.resolve()
    config_path = script_dir / "config.json"
    # Write resolved config to /tmp for write access by non-root user
    resolved_path = Path("/tmp/nanobot/config.resolved.json")
    resolved_path.parent.mkdir(parents=True, exist_ok=True)
    workspace_dir = script_dir / "workspace"

    if not config_path.exists():
        print(f"ERROR: config.json not found at {config_path}", file=sys.stderr)
        sys.exit(1)

    # Load base config
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # Override LLM provider settings
    llm_api_key = os.environ.get("LLM_API_KEY")
    llm_api_base_url = os.environ.get("LLM_API_BASE_URL")
    llm_api_model = os.environ.get("LLM_API_MODEL")

    if llm_api_key:
        config["providers"]["custom"]["apiKey"] = llm_api_key
    if llm_api_base_url:
        config["providers"]["custom"]["apiBase"] = llm_api_base_url
    if llm_api_model:
        config["agents"]["defaults"]["model"] = llm_api_model

    # Override gateway settings
    gateway_host = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS")
    gateway_port = os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT")

    if gateway_host:
        config["gateway"]["host"] = gateway_host
    if gateway_port:
        config["gateway"]["port"] = int(gateway_port)

    # Override webchat channel settings
    webchat_host = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS")
    webchat_port = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT")
    access_key = os.environ.get("NANOBOT_ACCESS_KEY")

    if "webchat" not in config["channels"]:
        config["channels"]["webchat"] = {}

    if webchat_host:
        config["channels"]["webchat"]["host"] = webchat_host
    if webchat_port:
        config["channels"]["webchat"]["port"] = int(webchat_port)
    if access_key:
        config["channels"]["webchat"]["accessKey"] = access_key
    config["channels"]["webchat"]["enabled"] = True
    if "allowFrom" not in config["channels"]["webchat"]:
        config["channels"]["webchat"]["allowFrom"] = ["*"]

    # Override MCP LMS server settings
    lms_backend_url = os.environ.get("NANOBOT_LMS_BACKEND_URL")
    lms_api_key = os.environ.get("NANOBOT_LMS_API_KEY")

    if "mcpServers" not in config["tools"]:
        config["tools"]["mcpServers"] = {}

    if "lms" not in config["tools"]["mcpServers"]:
        config["tools"]["mcpServers"]["lms"] = {
            "command": "python",
            "args": ["-m", "mcp_lms"],
        }

    lms_config = config["tools"]["mcpServers"]["lms"]

    if lms_backend_url:
        # Ensure args list has the URL as third argument
        if len(lms_config["args"]) < 3:
            lms_config["args"].append(lms_backend_url)
        else:
            lms_config["args"][2] = lms_backend_url

        # Also set in env for MCP server
        if "env" not in lms_config:
            lms_config["env"] = {}
        lms_config["env"]["NANOBOT_LMS_BACKEND_URL"] = lms_backend_url

    if lms_api_key:
        if "env" not in lms_config:
            lms_config["env"] = {}
        lms_config["env"]["NANOBOT_LMS_API_KEY"] = lms_api_key

    # Configure mcp-webchat MCP server for structured UI
    if "mcp_webchat" not in config["tools"]["mcpServers"]:
        config["tools"]["mcpServers"]["mcp_webchat"] = {
            "command": "python",
            "args": ["-m", "mcp_webchat"],
            "env": {},
        }

    webchat_mcp = config["tools"]["mcpServers"]["mcp_webchat"]
    if "env" not in webchat_mcp:
        webchat_mcp["env"] = {}
    # Pass relay URL and token if available
    ui_relay_url = os.environ.get("NANOBOT_UI_RELAY_URL")
    ui_relay_token = os.environ.get("NANOBOT_UI_RELAY_TOKEN")
    if ui_relay_url:
        webchat_mcp["env"]["NANOBOT_UI_RELAY_URL"] = ui_relay_url
    if ui_relay_token:
        webchat_mcp["env"]["NANOBOT_UI_RELAY_TOKEN"] = ui_relay_token

    # Write resolved config
    with open(resolved_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    return str(resolved_path), str(workspace_dir)


def main():
    """Resolve config and exec into nanobot gateway."""
    resolved_config, workspace_dir = resolve_config()

    print(f"Using resolved config: {resolved_config}")
    print(f"Using workspace: {workspace_dir}")

    # Launch nanobot gateway
    os.execvp(
        "nanobot",
        [
            "nanobot",
            "gateway",
            "--config",
            resolved_config,
            "--workspace",
            workspace_dir,
        ],
    )


if __name__ == "__main__":
    main()
