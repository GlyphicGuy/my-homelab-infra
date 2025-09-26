#This automation file is not in my setup but can be used if needed

#!/bin/bash
echo "🎵 Deploying Navidrome Music Server..."

# Create directories
sudo mkdir -p /docker/navidrome/data
sudo mkdir -p /srv/music

# Set permissions
sudo chown -R 1000:1000 /docker/navidrome

# Deploy
docker-compose up -d

echo "✅ Navidrome deployed! Access at http://$(hostname -I | awk '{print $1}'):4533"