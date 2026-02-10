# n8n - Workflow Automation & AI Agents

Open-source workflow automation tool with AI agent capabilities for homelab orchestration.

## Quick Deploy
```bash
docker-compose up -d
```
**Access:** http://myserver:5678

<!-- ![n8n](../screenshots/n8n.png) -->

## Purpose
Visual workflow builder that connects services, automates tasks and powers AI agents. Acts as the orchestration layer for complex homelab automation beyond simple scripts.

## Features
- **Visual workflow builder** with drag-and-drop interface
- **500+ integrations** including REST APIs, databases, and services
- **AI agent support** via MCP protocol connection
- **Scheduled executions** for recurring tasks
- **Webhook triggers** for event-driven automation
- **Self-hosted** with full data control

## Integration
- **MCP Server**: Connects via `http://host.docker.internal:5000/mcp` for AI-powered homelab control
- **Services**: Can trigger/monitor Radarr, Sonarr, Jellyfin, and other APIs
- **External**: Integrates with web services, notifications, and data sources

## Configuration
See docker-compose.yml for volume mounts and network settings.

### Environment Variables
- `N8N_ENCRYPTION_KEY`: Secure credential storage (set your own)
- `WEBHOOK_URL`: External webhook endpoint for triggers
- `GENERIC_TIMEZONE`: Server timezone for scheduling

## Usage Examples
- **Media Request Bot**: Telegram/Discord bot → n8n → Radarr/Sonarr
- **Health Monitoring**: Periodic checks → Alert on failures
- **Backup Automation**: Scheduled database dumps → Cloud storage
- **AI Assistant**: Natural language → MCP Server → Service control

## Access & Security
- **First-time setup**: Create admin account on initial access
- **Webhooks**: Use authentication for external triggers
- **Network**: Internal Docker network + host access via `host.docker.internal`

---
_Part of my homelab project_
