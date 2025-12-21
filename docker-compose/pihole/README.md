# **Pi-hole**

Acts as a network-wide "DNS Sinkhole" to block advertisements and tracking scripts for every device on the home Wi-Fi and Tailscale network.

## Quick Deploy
```bash
docker-compose up -d
```
**Access:** https://myserver:8081

**DNS Port:** `53` (Must remain open/unconflicted on host).



## **Features** 
**Ad-Blocking:** Stops ads in browsers, apps, and smart TVs at the DNS level.

* **Privacy:** Prevents telemetry and "calling home" from smart devices.
* **v6 Dashboard:** Modern, lightweight web interface for real-time query monitoring.
* **Tailscale Support:** Provides secure ad-blocking even when away from home.

## **Service Flow** 
Device Request → **Pi-hole (Port 53)** → Check Blocklist → (If clean) → Upstream DNS (1.1.1.1) → Website Loads.

## **Docker Compose Highlights**
**Image:** `pihole/pihole:latest` (v6).

* **Ports:** `53:53/tcp`, `53:53/udp`, `8081:80/tcp`.
* **Volume:** `./etc-pihole:/etc/pihole`.
* **Env:** `FTLCONF_dns_listeningMode: ALL` to ensure Docker bridge traffic is filtered.

## **Integrations**
- **Router:** Primary DNS set to server's reserved local IP on the router's admin panel.


* If Port 53 is busy, Pi-hole will fail to start. Use `ss -tulnp | grep :53` to check. Port can be configured to be used for Pi-hole.

---
_Part of my [homelab project](../../README.md)._
