from flask import Flask, request, jsonify
from pathlib import Path
import json

file_open_check = Path("localstorage.json")
if not file_open_check.is_file(): 
    new_file = open("localstorage.json", "w")

app = Flask(__name__)

# Local storage of a passed json J will be handled with a saved json localstorage_dict
# In short, localstorage_dict[j[name]] = j

# Dumps localstorage_dict into localstorage
def update_storage(localstorage_dict): 
    with open("localstorage.json", "w") as localstorage: 
        json.dump(localstorage_dict, localstorage)

# Updates localstorage with saved information
def pull_localstorage(): 
    with open("localstorage.json", "r") as file: 
        return json.loads(file.read())

# Save new json to localstorages
@app.route('/storagehandler', methods = ['POST'])
def post_new(): 
    localstorage_dict = pull_localstorage()

    # Access passed json block
    data = request.get_json()

    # Check for valid json object
    if (data == None): 
        return jsonify({'error': 'Request must be of type JSON, and must contain a "name" field'}), 400
    if ("name" not in data): 
        return jsonify({'error': '"name" is a required field'}), 400
    
    # Save to localstorage_dict 
    if (data["name"] in localstorage_dict): 
        return jsonify({'error': f'Local storage object already exists with name "{data["name"]}". Did you mean to POST to "/storagehandler/upd"?'}), 409
    else: 
        localstorage_dict[data["name"]] = data
        update_storage(localstorage_dict)

    # Return success
    return jsonify({"message": "Storage Successful"}), 200

# Update existing json in localstorage
@app.route("/storagehandler/upd", methods = ['POST'])
def update_object(): 
    localstorage_dict = pull_localstorage()

    # Access passed json block
    data = request.get_json()

    # Check for valid json object
    if (data == None): 
        return jsonify({'error': 'Request must be of type JSON, and must contain a "name" field matching a currently stored json'}), 400 
    if ("name" not in data): 
        return jsonify({'error': '"name" is a required field'}), 400
    
    # Update localstorage_dict object 
    localstorage_dict = pull_localstorage()
    if (data["name"] not in localstorage_dict): 
        return jsonify({'error': f'{data["name"]} not found in local storage'}), 404
    else: 
        localstorage_dict[data["name"]] = data
        update_storage(localstorage_dict)

    # Return success
    return jsonify({"message": f"{data["name"]} successfully updated"}), 200

# Get json from localstorage
@app.route("/storagehandler/<name>", methods = ["GET"])
def get_object(name): 
    localstorage_dict = pull_localstorage()

    # Access {name} in storage
    update_storage(localstorage_dict)
    ret = localstorage_dict.get(name)

    # Check for proper retrieval, access, and return
    if (ret is None): 
        return jsonify({"error": f'No locally stored object associated with name {name}'}), 404
    else: 
        return jsonify(ret)

# Delete json from localstorage
@app.route("/storagehandler/<name>", methods = ["DELETE"])
def delete_object(name): 
    localstorage_dict = pull_localstorage()

    # Access {name} in storage
    localstorage_dict = pull_localstorage()
    ret = localstorage_dict.get(name)

    # Check for proper retrieval, delete, and return
    if (ret is None): 
        return jsonify({"error": f'No locally stored object associated with name {name}'}), 404
    else: 
        localstorage_dict.pop(name)
        update_storage(localstorage_dict)
        return jsonify({"message": f'{name} successfully removed from local storage'}), 200
    
if (__name__ == '__main__'): 
    app.run(port = 8000)