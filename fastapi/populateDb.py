from helpers.dbConnect import coordinateCollection
import uuid
import json

with open("dummyData.json", "r") as file:
    data = json.load(file)

for i in data:
    doc = {
        "name": str(uuid.uuid4()),
        "location": {"type": "Point", "coordinates": i["location"]["coordinates"]},
        "numberofPotholes": i["numberOfPotholes"],
    }
    dbQueryResult = coordinateCollection.insert_one(doc).inserted_id
    print(f'new marker with at {i["location"]["coordinates"]}  potholes in  {dbQueryResult}')
