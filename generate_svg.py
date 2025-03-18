import json

# Load the JSON response from Toggl
with open("toggl_data.json", "r") as f:
    data = json.load(f)

# Extract project details
project_data = data["data"][0]  # Assuming "Security" is always the first project
project_name = project_data["title"]["project"]
total_time_ms = project_data["time"]

# Convert milliseconds to hours and minutes
total_minutes = total_time_ms // 60000
hours = total_minutes // 60
minutes = total_minutes % 60

# SVG content
svg_content = f'''<svg width="300" height="100" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="#2da608"/>
    <text x="50%" y="40%" font-size="20" text-anchor="middle" fill="white">{project_name}</text>
    <text x="50%" y="70%" font-size="18" text-anchor="middle" fill="white">{hours}h {minutes}m</text>
</svg>'''

# Save to SVG file
with open("toggl_time.svg", "w") as svg_file:
    svg_file.write(svg_content)

print("SVG file generated successfully: toggl_time.svg")
