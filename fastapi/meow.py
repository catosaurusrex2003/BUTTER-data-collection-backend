from helpers.dbConnect import coordinateCollection
import json
from bson import ObjectId

# Custom JSON encoder to handle ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

# Initialize a dictionary with the key "data"
output_data = {"data": []}

# Iterate over the result of the find() method to access each document
for document in coordinateCollection.find():
    # Append each document to the list associated with the key "data"
    output_data["data"].append(document)

# Write the dictionary to a JSON file
with open("databaseBackup.json", "w") as file:
    json.dump(output_data, file, cls=JSONEncoder, indent=4)  # Use indent for pretty printing
