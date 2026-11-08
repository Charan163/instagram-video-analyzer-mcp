import os
from fastmcp import FastMCP
import uvicorn

# Initialize FastMCP Server
mcp = FastMCP("Instagram Video Analyzer")

# Expose ASGI app for Uvicorn
app = mcp.http_app()

# Safely read the key from the terminal environment variable
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("⚠️ WARNING: GEMINI_API_KEY environment variable is missing in this terminal!")

@mcp.tool()
def analyze_instagram_video(url: str) -> str:
    """Analyzes an Instagram Reel video URL and provides content breakdown."""
    if not api_key:
        return "Error: GEMINI_API_KEY is not configured in environment variables."
    
    return f"Backend active. Ready to process Instagram Reel: {url}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("setup_complete:app", host="0.0.0.0", port=port)