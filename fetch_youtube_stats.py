import requests
import svgwrite

# === CONFIGURATION ===
API_KEY = ""  # Replace with your actual API key
CHANNEL_ID = ""  # Replace with your channel ID
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

# YouTube logo (simple version)
dwg.add(dwg.rect(insert=(20, 20), size=(50, 35), rx=8, ry=8, fill="#FF0000"))
dwg.add(dwg.polygon(points=[(40, 30), (40, 45), (58, 37)], fill="white"))

# Title
dwg.add(dwg.text("THEXNUMB's YouTube Stats", insert=(90, 45), font_size="18px", fill="black", font_family="Arial"))

# Stats
dwg.add(dwg.text(f"👁️ Views: {view_count}", insert=(90, 80), font_size="16px", fill="black"))
dwg.add(dwg.text(f"👤 Subscribers: {sub_count}", insert=(90, 110), font_size="16px", fill="black"))
dwg.add(dwg.text(f"🎞️ Videos: {video_count}", insert=(90, 140), font_size="16px", fill="black"))

# Save SVG
dwg.save()
print(f"SVG saved to {OUTPUT_SVG}")
