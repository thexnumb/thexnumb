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
project_sec = os.getenv('PROJECT_ID')
project_per = os.getenv('PROJECT_PER')
api_token = os.getenv('TOGGL_API_TOKEN')

def create_svg (id):
    # API URL
    url = f"https://api.track.toggl.com/reports/api/v3/workspace/{workspace_id}/projects/{id}/summary"
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

    if id == 205117233:
        # Set Project name and Total Time
        project_name = "Security"
        total_time_s = data['seconds']
        hex_color = "#2da608"

        # Calculate Hours and Minutes
        hours = total_time_s // 3600
        minutes = (total_time_s % 3600) // 60

        # Generate SVG
        svg_content = f'''<svg width="260" height="130" xmlns="http://www.w3.org/2000/svg">
            <!-- Background with Rounded Corners -->
            <rect width="100%" height="100%" rx="15" ry="15" fill="{hex_color}" />

            <!-- Project Name -->
            <text x="50%" y="22%" font-size="24" font-family="Arial, sans-serif" font-weight="bold"
                text-anchor="middle" fill="white">{project_name}</text>

            <!-- Date Range -->
            <text x="50%" y="45%" font-size="14" font-family="Arial, sans-serif"
                text-anchor="middle" fill="white">From {start_date} to {end_date}</text>

            <!-- Time Spent -->
            <text x="50%" y="72%" font-size="30" font-family="Arial, sans-serif" font-weight="bold"
                text-anchor="middle" fill="white">{hours}h {minutes}m</text>
        </svg>'''

        # Save to SVG file
        svg_filename = f'toggl_weekly_{project_name}_report.svg'
        with open(svg_filename, 'w') as svg_file:
            svg_file.write(svg_content)

        print(f"SVG file generated successfully: {svg_filename}")

    else:
        # Set Project name and Total Time
        project_name = "Personal"
        total_time_s = data['seconds']
        hex_color = "#FFA500"

        # Calculate Hours and Minutes
        hours = total_time_s // 3600
        minutes = (total_time_s % 3600) // 60

        # Generate SVG
        svg_content = f'''<svg width="260" height="130" xmlns="http://www.w3.org/2000/svg">
            <!-- Background with Rounded Corners -->
            <rect width="100%" height="100%" rx="15" ry="15" fill="{hex_color}" />

            <!-- Project Name -->
            <text x="50%" y="22%" font-size="24" font-family="Arial, sans-serif" font-weight="bold"
                text-anchor="middle" fill="white">{project_name}</text>

            <!-- Date Range -->
            <text x="50%" y="45%" font-size="14" font-family="Arial, sans-serif"
                text-anchor="middle" fill="white">From {start_date} to {end_date}</text>

            <!-- Time Spent -->
            <text x="50%" y="72%" font-size="30" font-family="Arial, sans-serif" font-weight="bold"
                text-anchor="middle" fill="white">{hours}h {minutes}m</text>
        </svg>'''

        # Save to SVG file
        svg_filename = f'toggl_weekly_{project_name}_report.svg'
        with open(svg_filename, 'w') as svg_file:
            svg_file.write(svg_content)

        print(f"SVG file generated successfully: {svg_filename}")

create_svg(205117233)
create_svg(205117652)
