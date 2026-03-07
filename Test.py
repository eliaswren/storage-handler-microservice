import requests
import time

port = "http://localhost:8000/storagehandler"

json_file = {}
json_file['name'] = 'Test'
json_file['message'] = 'This is a test message'

# Post new json object to localstorage
response = requests.post(port, json=json_file)
print("POST Response: ", response.json())

time.sleep(1)

# Modify JSON in localstorage
json_file['message'] = 'This is an updated test message'
response = requests.post(port + "/upd", json=json_file)
print("POST Response (update): ", response.json())

time.sleep(1)

# Retrieve json from localstorage
response = requests.get(port + f"/{json_file['name']}")
print("GET Response: ", response.json())

time.sleep(1)

# Remove json from localstorage
response = requests.delete(port + f"/{json_file["name"]}")
print("DELETE Response: ", response.json())
