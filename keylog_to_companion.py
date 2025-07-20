#Import Libraries
import keyboard
import requests
import sys
import json
import os

#Function to read json file and return it as a python dictionary
def readFile (filename):
    content = {}
    try:
        file = open(filename)
        content = json.loads(file.read())
        file.close()
    except:
        print("File not found")
    return content

#Subroutine to send Companion Press commmand
def send_signal_to_companion(page, row, column):
    try:
        url = f"{base_url}/api/location/{page}/{row}/{column}/press"

        # Send the POST request without any data payload
        response = requests.post(url)

        # Check if the request was successful
        if response.status_code == 200:
            print(f"Command sent successfully to {url}")
        else:
            print(f"Failed to send command, status code: {response.status_code}, reason: {response.text}")
    except Exception as e:
        print(f"Error sending command: {e}")

# -- MAIN -- 
#Find config file
directory = ""
python_filepath = os.path.abspath(__file__)
if getattr(sys, 'frozen', False):
    directory = os.path.dirname(sys.executable)
else:
    directory = os.path.dirname(python_filepath)
directory = directory + "/config.json"

config = readFile(directory)

#Get companion http address
settings = config["system"]
ip_address = settings["ip_address"]
port_number = settings["port_number"]
base_url = "http://" + ip_address + ":" + port_number

#Role Macros
keybinds = config["keybinds"]
keys = list(keybinds.keys())

#Assign keybinds
for key in keys:
    button = keybinds[key]
    page = button["page"]
    row = button["row"]
    column = button["column"]
    keyboard.add_hotkey(key, lambda p=page, r=row, c=column: send_signal_to_companion(p, r, c))

# Keep the script running to listen for key presses
print("Running in the background, Escape to Exit...")
keyboard.wait('esc')  # This will keep the script running, waiting for key presses