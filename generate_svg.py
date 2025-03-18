import json

# Load Toggl JSON data
with open("toggl_time.json", "r") as f:
    data = json.load(f)

# Extract time-tracking details (Modify as needed)
total_seconds = sum(entry["duration"] for entry in data if entry["duration"] > 0)
hours = total_seconds // 3600
minutes = (total_seconds % 3600) // 60

# Create SVG content
svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="50">
    <rect width="100%" height="100%" fill="black"/>
    <text x="50%" y="50%" font-size="18" fill="white" text-anchor="middle" alignment-baseline="middle">
        🕒 {hours}h {minutes}m spent this week
    </text>
</svg>"""

# Save to file
with open("toggl_time.svg", "w") as f:
    f.write(svg_content)

print("SVG Updated!")
