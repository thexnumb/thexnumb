import gnupg
import os
import json

# Initialize the GPG object
gpg = gnupg.GPG()

# Define the file paths
encrypted_file_path = 'toggl_time.json.gpg'
decrypted_file_path = 'toggl_time.json'

# Retrieve the encryption password from environment variables
password = os.getenv('ENCRYPTION_PASSWORD')
if not password:
    raise ValueError("Encryption password not set in environment variables.")

# Decrypt the file
with open(encrypted_file_path, 'rb') as enc_file:
    status = gpg.decrypt_file(enc_file, passphrase=password, output=decrypted_file_path)

if status.ok:
    print(f"File decrypted successfully: {decrypted_file_path}")
    try:
        # Open and process the decrypted JSON file
        with open(decrypted_file_path, 'r') as f:
            data = json.load(f)

        # Extract project details
        project_data = data.get('data', [])[0] if data.get('data') else None
        if project_data:
            project_name = project_data.get('title', {}).get('project', 'Unknown Project')
            total_time_ms = project_data.get('time', 0)
            
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
            svg_file_path = 'toggl_time.svg'
            with open(svg_file_path, 'w') as svg_file:
                svg_file.write(svg_content)
            print(f"SVG file generated successfully: {svg_file_path}")
        else:
            print("No project data found in the JSON.")
    except (KeyError, IndexError) as e:
        print(f"Error processing Toggl data: {e}")
        # Generate a placeholder SVG in case of errors
        placeholder_svg = '''<svg width="300" height="100" xmlns="http://www.w3.org/2000/svg">
            <rect width="100%" height="100%" fill="#cccccc"/>
            <text x="50%" y="50%" font-size="16" text-anchor="middle" fill="black">No Toggl data available</text>
        </svg>'''
        with open('toggl_time.svg', 'w') as svg_file:
            svg_file.write(placeholder_svg)
    finally:
        # Ensure the decrypted file is deleted after processing
        if os.path.exists(decrypted_file_path):
            os.remove(decrypted_file_path)
            print(f"Decrypted file {decrypted_file_path} deleted successfully.")
else:
    print(f"Decryption failed: {status.stderr}")
