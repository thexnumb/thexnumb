import os
import requests
import json
import base64
from datetime import datetime, timedelta

# Function to calculate the start and end dates of the previous week
def get_previous_week_dates():
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday() + 7)
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week.strftime('%Y-%m-%d'), end_of_week.strftime('%Y-%m-%d')

# Set Start and End Dates for the Previous Week
start_date, end_date = get_previous_week_dates()
os.environ['START_DATE'] = start_date
os.environ['END_DATE'] = end_date

# Fetch Weekly Report Data
workspace_id = os.getenv('TOGGL_WORKSPACE_ID')
project_id = os.getenv('TOGGL_PROJECT_ID')
api_token = os.getenv('TOGGL_API_TOKEN')

if not all([workspace_id, project_id, api_token]):
    print("Error: Missing Toggl environment variables.")
    exit(1)

# API URL
url = f"https://api.track.toggl.com/reports/api/v3/workspace/{workspace_id}/projects/{project_id}/summary"

# Encode API Token
auth_token = base64.b64encode(f"{api_token}:api_token".encode()).decode()

# Headers
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {auth_token}'
}

# Request Payload
payload = {
    "start_date": start_date,
    "end_date": end_date,
    "startTime": "00:00:00"
}

# Send API Request
try:
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # Raise an error for non-200 responses
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
    exit(1)
except json.JSONDecodeError:
    print("Error: Received invalid JSON response.")
    exit(1)

# Extract project title and total time
project_entry = next(iter(data.get("data", [])), {})

project_name = project_entry.get("title", {}).get("project")
total_time_ms = project_entry.get("time")
hex_color = project_entry.get("title", {}).get("hex_color")

# Convert milliseconds to hours and minutes
total_minutes = total_time_ms // 60000
hours = total_minutes // 60
minutes = total_minutes % 60

# Generate SVG
svg_content = f'''<svg width="300" height="100" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="{hex_color}"/>
    <text x="50%" y="40%" font-size="20" text-anchor="middle" fill="white">{project_name}</text>
    <text x="50%" y="70%" font-size="18" text-anchor="middle" fill="white">{hours}h {minutes}m</text>
</svg>'''

# Save to SVG file
svg_filename = 'toggl_weekly_report.svg'
with open(svg_filename, 'w') as svg_file:
    svg_file.write(svg_content)

print(f"SVG file generated successfully: {svg_filename}")
