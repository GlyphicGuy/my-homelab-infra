# Sonarr - TV Show Automation

**Part of the [Arr Stack](../arr-stack/)**

## Purpose
Automated TV show management - finds, downloads, and organizes episodes.

## Access
- **Web UI**: http://myserver:8989
- **Default credentials**: None (set on first access)

## Integration
- **Source**: Prowlarr indexers
- **Download**: qBittorrent client  
- **Destination**: Jellyfin TV library (`/srv/media/tv`)

## Configuration
See [docker-compose.yml](../arr-stack/docker-compose.yml) for volume mounts and settings.