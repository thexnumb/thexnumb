import os
import requests
import json
import base64
from datetime import datetime

# Function to calculate the start and end dates of the current year
def get_current_year_dates():
    today = datetime.today()
    start_of_this_year = datetime(today.year, 1, 1)
    end_of_this_year = datetime(today.year, 12, 31)
    return start_of_this_year.date().strftime('%Y-%m-%d'), end_of_this_year.date().strftime('%Y-%m-%d')

# Set Start and End Dates for the Current Year
start_date, end_date = get_current_year_dates()
os.environ['START_DATE'] = start_date
os.environ['END_DATE'] = end_date

# Fetch Yearly Report Data
workspace_id = os.getenv('TOGGL_WORKSPACE_ID')
project_sec = os.getenv('PROJECT_ID')
project_per = os.getenv('PROJECT_PER')
api_token = os.getenv('TOGGL_API_TOKEN')

def create_svg(id):
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

    # Set values depending on project
    if id == 205117233:
        project_name = "Security"
        hex_color = "#2da608"
    else:
        project_name = "Personal"
        hex_color = "#FFA500"

    total_time_s = data['seconds']

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
    svg_filename = f'toggl_current_year_{project_name}_report.svg'
    with open(svg_filename, 'w') as svg_file:
        svg_file.write(svg_content)

    print(f"SVG file generated successfully: {svg_filename}")

# Generate current year reports
create_svg(205117233)  # Security
create_svg(205117652)  # Personal
