# Nextcloud - Personal Cloud

Self-hosted Google Drive/Dropbox replacement with file sync, contacts, calendar, and more.

## Quick Deploy
```bash
docker-compose up -d
```
**Access:** http://myserver:8080

## My Setup
- **Storage**: `/srv/cloud` (mounted to Nextcloud data directory)
- **Database**: MySQL for compatibility and performance
- **Web Server**: Nginx (built into Nextcloud image)
- **Features**: File sync, contacts, calendar, mobile apps
- **Users**: Personal and family accounts

## Features Used
- **File synchronization** across devices
- **Contact and calendar sync** with mobile
- **Mobile app** for photo backup and file access
- **Web interface** for administration and file management

## Integration
- **Clients**: Desktop sync client, mobile apps, web interface
- **Storage**: Local server storage with regular backups
- **Access**: Direct or via Tailscale VPN for remote access

---
_Part of my [homelab project](../../README.md)._

