import requests
import json
import os
import time
import argparse
import getpass

# Constants
BASE_URL = "https://api.daikinskyport.com"
URL_LOGIN = f"{BASE_URL}/users/auth/login"
DEVICES_URL = f"{BASE_URL}/devices"
DEVICE_DATA_URL_TEMPLATE = f"{BASE_URL}/deviceData/{{}}"

# Function to create a directory if it does not exist
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Function to handle login and retrieve the access token
def login(username,password):


    # If password is not provided via command line, prompt for it securely
    if password is None:
        password = getpass.getpass(prompt='Password: ')

    payload = json.dumps({
        "email": username,
        "password": password
    })

    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.post(URL_LOGIN, headers=headers, data=payload)
    
    if response.status_code == 400:
        print("Bad request: Please check your username and password.")
        return False
   

    data = response.json()

    return data['accessToken'] if data else None

def fetch_devices(authorization_key):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': authorization_key
    }

    response = requests.get(DEVICES_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch devices. Status code: {response.status_code}")
        return []

def fetch_device_data(device_id, authorization_key):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': authorization_key
    }
    device_data_url = DEVICE_DATA_URL_TEMPLATE.format(device_id)
    response = requests.get(device_data_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for device with id '{device_id}'")
        return None

def save_device_data(name, firmware_version, device_data, datamap_directory):
    file_path = os.path.join(datamap_directory, f"{name}__{firmware_version}.json")
    with open(file_path, 'w') as json_file:
        json.dump(device_data, json_file, indent=4)
    print(f"Data for device '{name}' saved to '{file_path}'")

def main(username, password):

    auth_key = login(username, password)
    if auth_key == False:
        return False

    # Fetch devices
    devices = fetch_devices(auth_key)
    if not devices:
        return

    # Create the "datamap" directory in the same directory as the Python script
    script_directory = os.path.dirname(os.path.realpath(__file__))
    datamap_directory = os.path.join(script_directory, "datamaps")
    create_directory(datamap_directory)

    # Process each device
    for device in devices:
        if 'id' in device and 'name' in device and 'firmwareVersion' in device:
            device_id = device['id']
            name = device['name']
            firmware_version = device['firmwareVersion']

            # Fetch device data
            device_data = fetch_device_data(device_id, auth_key)
            if device_data:
                save_device_data(name, firmware_version, device_data, datamap_directory)
if __name__ == "__main__":
    main()