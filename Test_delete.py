import requests

json={"name": "Test", "message": "This is a test"}
response = requests.delete(f"http://localhost:8000/storagehandler/{json["name"]}")
print("Response: ", response.json())

