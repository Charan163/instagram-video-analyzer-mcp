import os
import uvicorn
from fastmcp import FastMCP
from typing import Optional

# Initialize FastMCP Server
mcp = FastMCP("Instagram Video Analyzer")


@mcp.tool()
def analyze_instagram_video(
    url: str, user_gemini_api_key: Optional[str] = None
) -> str:
    """Analyzes an Instagram Reel video URL and provides content breakdown.

    Args:
        url: The Instagram Reel video URL to analyze.
        user_gemini_api_key: Optional Google Gemini API key supplied by the user.
    """
    active_key = user_gemini_api_key or os.getenv("GEMINI_API_KEY")

    if not active_key:
        return (
            "Error: Gemini API key is missing. Please provide your Google Gemini API key "
            "to analyze this Instagram Reel."
        )

    return (
        f"Backend active. Ready to process Instagram Reel: {url} "
        f"(Using key ending in ...{active_key[-4:]})"
    )


# Expose standard ASGI HTTP app (FastMCP handles SSE routes internally)
app = mcp.http_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("setup_complete:app", host="0.0.0.0", port=port)