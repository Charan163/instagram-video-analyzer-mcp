import os
import tempfile
import uvicorn
from fastmcp import FastMCP
from typing import Optional
from google import genai
import yt_dlp

mcp = FastMCP("Instagram Video Analyzer")

def download_reel(url: str, output_path: str):
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@mcp.tool()
def analyze_instagram_video(
    url: str, user_gemini_api_key: Optional[str] = None
) -> str:
    """Analyzes an Instagram Reel video URL using Gemini Vision API."""
    active_key = user_gemini_api_key or os.getenv("GEMINI_API_KEY")

    if not active_key:
        return "Error: Gemini API key is missing. Please provide your Google Gemini API key."

    client = genai.Client(api_key=active_key)

    with tempfile.TemporaryDirectory() as tmpdir:
        video_path = os.path.join(tmpdir, "reel.mp4")
        try:
            download_reel(url, video_path)
            
            # Upload video file to Gemini API
            video_file = client.files.upload(file=video_path)
            
            prompt = (
                "Analyze this Instagram Reel thoroughly:\n"
                "1. Opening Hook & Attention Strategy\n"
                "2. Video Script & Storytelling Breakdown\n"
                "3. Visual Editing & Pacing\n"
                "4. Audience Engagement & Virality Factors\n"
                "5. Actionable tips on how to recreate this content."
            )
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[video_file, prompt]
            )
            return response.text

        except Exception as e:
            return f"Error analyzing Instagram Reel: {str(e)}"

app = mcp.http_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("setup_complete:app", host="0.0.0.0", port=port)