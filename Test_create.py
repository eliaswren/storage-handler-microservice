import requests

response = requests.post(
    "http://localhost:8000/storagehandler", 
    json={"name": "Test", "message": "This is a test"}
    )
print("Response: ", response.json())

