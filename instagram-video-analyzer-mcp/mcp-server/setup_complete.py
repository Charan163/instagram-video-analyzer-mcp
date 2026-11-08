import os
from fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("Instagram Video Analyzer")

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
    print("🚀 Local Instagram Video Analyzer Backend starting on http://localhost:8000 ...")
    mcp.run(transport="sse", port=8000)