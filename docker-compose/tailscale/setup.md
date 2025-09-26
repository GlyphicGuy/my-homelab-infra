# Tailscale Setup Guide

## Server Setup
1. Install Tailscale: `curl -fsSL https://tailscale.com/install.sh | sh`
2. Start service: `sudo tailscale up`
3. Enable on boot: `sudo systemctl enable --now tailscaled`

## Client Setup
1. Install Tailscale on phone/laptop
2. Login with your account
3. Access services via Tailscale IP

## Access Examples
- Navidrome: `http://100.x.x.x:4533`
- Jellyfin: `http://100.x.x.x:8096`
- Nextcloud: `http://100.x.x.x:8080`

---
>_explore tailscale settings and features to learn more and better :)_