import json
import os

# Load the JSON response from Toggl
# The file name should match what's used in the GitHub Action
with open("toggl_time.json", "r") as f:
    data = json.load(f)

# Extract project details 
try:
    project_data = data["data"][0]  # Assuming the project is always the first one
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
    
except (KeyError, IndexError) as e:
    print(f"Error processing Toggl data: {e}")
    print("Generating placeholder SVG")
    
    # Create a placeholder SVG in case of errors
    placeholder_svg = '''<svg width="300" height="100" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="#cccccc"/>
        <text x="50%" y="50%" font-size="16" text-anchor="middle" fill="black">No Toggl data available</text>
    </svg>'''
    
    with open("toggl_time.svg", "w") as svg_file:
        svg_file.write(placeholder_svg)
