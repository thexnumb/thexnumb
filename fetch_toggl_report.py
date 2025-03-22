import os
import requests
import json
import base64
from datetime import datetime, timedelta

# Function to calculate the start and end dates of the previous week
def get_previous_week_dates():
    today = datetime.today()
    start_of_week = today - timedelta(days=7)  # 7 days ago
    end_of_week = today - timedelta(days=1)    # Yesterday
    return start_of_week.date().strftime('%Y-%m-%d'), end_of_week.date().strftime('%Y-%m-%d')

# Set Start and End Dates for the Previous Week
start_date, end_date = get_previous_week_dates()
os.environ['START_DATE'] = start_date
os.environ['END_DATE'] = end_date

# Fetch Weekly Report Data
workspace_id = os.getenv('TOGGL_WORKSPACE_ID')
project_id = os.getenv('PROJECT_ID')  # <-- Corrected variable name
api_token = os.getenv('TOGGL_API_TOKEN')

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
}

# Send API Request
response = requests.post(url, headers=headers, json=payload)
data = response.json()

# Set Project name and Total Time
project_name = "Security"
total_time_s = data['seconds']
hex_color = "#2da608"

# Calculate Hours and Minutes
hours = total_time_s // 3600
minutes = (total_time_s % 3600) // 60

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
