{
  "theme": "Default",
  "selectedAuthType": "oauth-personal",
  "mcpServers": {
    "MY_DEBIAN_SERVER": {
      "httpUrl": "http://tailscale-ip:5000/mcp",
    #if no response in 30sec stop trying
      "timeout": 30000 
    },
  }
}