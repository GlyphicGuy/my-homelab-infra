import os
import docker
import psutil
import subprocess
from fastmcp import FastMCP
from typing import List, Dict, Any
from arrapi import RadarrAPI, SonarrAPI
# --- Create the MCP Server ---
# We tell it to run as an HTTP server on port 5000
mcp = FastMCP(name="Debian Server Tools")

# --- Helper Function ---
# This connects to the Docker socket *inside* the container
# The socket is mounted from the host.
def get_docker_client():
    return docker.DockerClient(base_url='unix://var/run/docker.sock')

# --- Helper Function for Radarr ---
def get_radarr_client():
    # Reads the secrets from the environment variables we set in docker-compose
    radarr_url = os.environ.get("RADARR_URL")
    radarr_key = os.environ.get("RADARR_API_KEY")

    if not radarr_url or not radarr_key:
        print("RADARR_URL or RADARR_API_KEY environment variables not set.")
        return None
        
    return RadarrAPI(radarr_url, radarr_key)

# --- Helper Function for Sonarr ---
def get_sonarr_client():
    # Reads the secrets from the environment variables
    sonarr_url = os.environ.get("SONARR_URL")
    sonarr_key = os.environ.get("SONARR_API_KEY")

    if not sonarr_url or not sonarr_key:
        print("SONARR_URL or SONARR_API_KEY environment variables not set.")
        return None
        
    return SonarrAPI(sonarr_url, sonarr_key)


# --- Tool 1: List Containers ---
@mcp.tool()
def list_containers() -> List[Dict[str, Any]]:
    """
    Lists all running containers on the Debian server.
    """
    try:
        client = get_docker_client()
        containers = client.containers.list()
        
        # Format the output to be clean for the AI
        return [
            {
                "id": c.short_id,
                "name": c.name,
                "image": c.image.tags[0] if c.image.tags else "unknown",
                "status": c.status
            }
            for c in containers
        ]
    except Exception as e:
        return [{"error": str(e)}]

# --- Tool 2: Get System Uptime ---
@mcp.tool()
def get_system_uptime() -> str:
    """
    Gets the system uptime for the Debian server.
    """
    try:
        # Use subprocess to run the 'uptime' command for a human-readable string
        result = subprocess.run(['uptime', '-p'], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error getting uptime: {str(e)}"

# --- Tool 3: Get Disk Usage ---
@mcp.tool()
def get_disk_usage(path: str = "/") -> Dict[str, str]:
    """
    Gets the disk usage for a specified path on the Debian server.
    Defaults to the root directory '/'.
    """
    try:
        usage = psutil.disk_usage(path)
        return {
            "path": path,
            "total": f"{usage.total // (1024**3)} GB",
            "used": f"{usage.used // (1024**3)} GB",
            "free": f"{usage.free // (1024**3)} GB",
            "percent_used": f"{usage.percent}%"
        }
    except Exception as e:
        return {"error": str(e)}

# --- Tool 4: Restart a Container ---
@mcp.tool()
def restart_container(name: str) -> str:
    """
    Restarts a specific container on the Debian server by its name.
    For example: 'restart jellyfin' or 'restart nextcloud'.
    """
    try:
        client = get_docker_client()
        print(f"Attempting to find container: {name}")
        container = client.containers.get(name) # This finds the container by name
        
        print(f"Found container {container.short_id}. Attempting to restart...")
        container.restart() 
        
        return f"Successfully restarted container '{name}' (ID: {container.short_id})."
    
    except docker.errors.NotFound:
        # This is a specific error if the name is wrong
        print(f"Error: Container '{name}' not found.")
        return f"Error: Container '{name}' not found. Use 'list_containers' to see available names."
    except Exception as e:
        # This catches all other errors
        print(f"An unexpected error occurred: {str(e)}")
        return f"An unexpected error occurred: {str(e)}"

# --- NEW: Tool 5: Add a Movie to Radarr ---
@mcp.tool()
def add_movie_to_radarr(title: str, year: int = None) -> str:
    """
    Searches for a movie by title and optional year, and adds the first result to Radarr.
    It will use the first available root folder and quality profile.
    """
    DESIRED_QUALITY_PROFILE = "Good HD" #check in your quality profiles

    try:
        radarr = get_radarr_client()
        if radarr is None:
            return "Error: Radarr server is not configured. Check server logs."

        print(f"Searching Radarr for: {title} ({year})")
        # 1. Search for the movie
        search_term = f"{title} {year}" if year else title
        search_results = radarr.search_movies(search_term)
        
        if not search_results:
            return f"Error: No movie found on Radarr with the title '{title}'."

        movie_to_add = search_results[0] # Just grab the first result
        movie_title = movie_to_add.title
        print(f"Found movie: {movie_title} (TMDB ID: {movie_to_add.tmdbId})")

        # 2. Get the first root folder
        root_folders = radarr.root_folder() 
        if not root_folders:
            return "Error: No root folders found in your Radarr setup."
        root_folder_path = root_folders[0].path
        
        # 3. Find the SPECIFIC quality profile
        quality_profiles = radarr.quality_profile()
        if not quality_profiles:
            return "Error: No quality profiles found in your Sonarr setup."

        target_profile = None
        for profile in quality_profiles:
            # Check the name, ignoring case
            if profile.name.lower() == DESIRED_QUALITY_PROFILE.lower():
                target_profile = profile
                break # We found it, stop looping

        # If we didn't find it, return an error
        if target_profile is None:
            return f"Error: Could not find a quality profile named '{DESIRED_QUALITY_PROFILE}'. Check your spelling."
        
        quality_profile_id = target_profile.id
        print(f"Found profile. Using Quality Profile: '{target_profile.name}' (ID: {quality_profile_id})")
        
        # 4. Add the movie!
        movie_to_add.add(
            root_folder_path, 
            quality_profile_id,
            search=True 
        )
        
        return f"Successfully added '{movie_title}' to Radarr."

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return f"An unexpected error occurred: {str(e)}"


# --- NEW: Tool 6: Add a Series to Sonarr (v3 Compatible) ---
@mcp.tool()
def add_series_to_sonarr(title: str, year: int = None) -> str:
    """
    Searches for a TV series by title and optional year, and adds the first result to Sonarr.
    It will use a specific, pre-defined quality profile. (Sonarr v3 compatible).
    """
   
    DESIRED_QUALITY_PROFILE = "HD-720p" 
    
    try:
        sonarr = get_sonarr_client()
        if sonarr is None:
            return "Error: Sonarr server is not configured. Check server logs."

        print(f"Searching Sonarr for: {title} ({year})")
        # 1. Search for the series
        search_term = f"{title} {year}" if year else title
        search_results = sonarr.search_series(search_term)
        
        if not search_results:
            return f"Error: No series found on Sonarr with the title '{title}'."

        series_to_add = search_results[0] # Just grab the first result
        series_title = series_to_add.title
        print(f"Found series: {series_title} (TVDB ID: {series_to_add.tvdbId})")

        # 2. Get the first root folder
        root_folders = sonarr.root_folder()
        if not root_folders:
            return "Error: No root folders found in your Sonarr setup."
        root_folder_path = root_folders[0].path
        
        # 3. Find the SPECIFIC quality profile
        quality_profiles = sonarr.quality_profile()
        if not quality_profiles:
            return "Error: No quality profiles found in your Sonarr setup."
            
        target_quality_profile = None
        for profile in quality_profiles:
            if profile.name.lower() == DESIRED_QUALITY_PROFILE.lower():
                target_quality_profile = profile
                break
        
        if target_quality_profile is None:
            return f"Error: Could not find a quality profile named '{DESIRED_QUALITY_PROFILE}'."
        
        print(f"Adding series with Quality Profile '{target_quality_profile.name}'...")
        
        # 4. Add the series! (v3 version, no language profile ID)
        series_to_add.add(
            root_folder_path, 
            target_quality_profile.id,
            search=True # Tells Sonarr to auto-search for missing episodes
        )
        
        return f"Successfully added '{series_title}' to Sonarr (Profile: {target_quality_profile.name})."

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return f"An unexpected error occurred: {str(e)}"



#--run the server ---
if __name__ == "__main__":
    print("Starting Debian Server MCP on http://0.0.0.0:5000")
    # This runs the server using the "http" transport

    mcp.run(transport="http", port=5000, host="0.0.0.0")
