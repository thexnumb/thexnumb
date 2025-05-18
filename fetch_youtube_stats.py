import requests
import os
import svgwrite

# === CONFIGURATION ===
API_KEY = os.getenv('YOUTUBE_API')  
CHANNEL_ID = os.getenv('YOUTUBE_CHANNEL_ID')  
OUTPUT_SVG = "youtube_stats.svg"

# === FETCH DATA ===
url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={CHANNEL_ID}&key={API_KEY}"
response = requests.get(url)
data = response.json()

if "items" not in data or not data["items"]:
    raise Exception("Failed to retrieve channel statistics.")

stats = data["items"][0]["statistics"]
view_count = stats.get("viewCount", "0")
sub_count = stats.get("subscriberCount", "0")
video_count = stats.get("videoCount", "0")

# === GENERATE SVG ===
dwg = svgwrite.Drawing(OUTPUT_SVG, size=("420px", "200px"), profile="tiny")

# Title
dwg.add(dwg.text("THEXNUMB's YouTube Stats", insert=(90, 45), font_size="18px", fill="orange", font_family="Arial"))

# Stats
dwg.add(dwg.text(f"👁️ Views: {view_count}", insert=(90, 80), font_size="16px", fill="orange"))
dwg.add(dwg.text(f"👤 Subscribers: {sub_count}", insert=(90, 110), font_size="16px", fill="orange"))
dwg.add(dwg.text(f"🎞️ Videos: {video_count}", insert=(90, 140), font_size="16px", fill="orange"))

# Save SVG
dwg.save()
print(f"SVG saved to {OUTPUT_SVG}")
