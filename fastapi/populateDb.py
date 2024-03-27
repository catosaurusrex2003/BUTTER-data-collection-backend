from helpers.dbConnect import coordinateCollection
import uuid
import json

with open("newJson.json", "r") as file:
    data = json.load(file)

for i in data:
    doc = {
        "name": str(uuid.uuid4()),
        "location": {
            "type": "Point",
            "coordinates": [float(i["coordinates"]["laty"]), float(i["coordinates"]["latx"])],
        },
        "numberofPotholes": [i["arr"][0]] * 10,
    }
    dbQueryResult = coordinateCollection.insert_one(doc).inserted_id
    print(
        f'new marker with at {doc["location"]}  potholes in  {dbQueryResult}'
    )
