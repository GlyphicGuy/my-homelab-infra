# Arr Stack - Media Automation Suite

**Integrated system for automated media acquisition and management.**

## 🎯 Purpose
Automatically finds, downloads, and organizes movies and TV shows, feeding content directly to Jellyfin.

## 🔗 Component Services
- **[Sonarr](../sonarr/)** - TV show management & automation
- **[Radarr](../radarr/)** - Movie management & automation  
- **[Prowlarr](../prowlarr/)** - Unified indexer manager
- **[qBittorrent](../qbittorrent/)** - Download client

## 📋 Deployment Order
1. **qBittorrent** - Download client foundation
2. **Prowlarr** - Configure indexers and trackers
3. **Sonarr** - TV show automation
4. **Radarr** - Movie automation
5. **Configure integrations** between all services

## 🔄 Workflow
graph coming soon


## ⚙️ Integration Points
- **Sonarr/Radarr** → **Prowlarr**: Search indexers
- **Prowlarr** → **qBittorrent**: Send download links
- **qBittorrent** → **Sonarr/Radarr**: Import completed downloads
- **Sonarr/Radarr** → **Jellyfin**: Library updates

## 🗂️ Folder Structure
```
/srv/media/
├── movies/         # Radarr → Jellyfin
├── tv/             # Sonarr → Jellyfin  
├── downloads/      # qBittorrent active downloads
└── complete/       # Processed downloads
```

## 🚀 Quick Start
Deploy all components (see individual service READMEs for details):
```bash
# Deploy in order
cd ../qbittorrent && docker-compose up -d
cd ../prowlarr && docker-compose up -d  
cd ../sonarr && docker-compose up -d
cd ../radarr && docker-compose up -d
```
---
_Part of my [homelab project](../../README.md)._

