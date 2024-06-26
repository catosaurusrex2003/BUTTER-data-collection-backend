import pymongo
from helpers.dbConnect import (
    coordinateCollection,
    testCoordinateCollection,
    sparsePotholesCollection,
)
from helpers.queryDatabaseForPotholes import (
    queryDatabaseForPotholes,
)
import uuid
import json


coordinateCollection.create_index([("location", pymongo.GEOSPHERE)])
testCoordinateCollection.create_index([("location", pymongo.GEOSPHERE)])
sparsePotholesCollection.create_index([("location", pymongo.GEOSPHERE)])

with open("databaseBackup.json", "r") as file:
    data = json.load(file)

    for i in data["data"]:
        longitude = float(i["location"]["coordinates"][0])
        latitude = float(i["location"]["coordinates"][1])
        numberofPotholes = i["numberofPotholes"]

        result = queryDatabaseForPotholes(longitude, latitude, 20)

        if result:
            print(result)
            updateQuery = {"_id": result["_id"]}
            tempArray = result["numberofPotholes"]
            if len(tempArray) >= 10:
                tempArray.pop(0)
                tempArray.append(numberofPotholes[0])
            else:
                tempArray.append(numberofPotholes)
            update = {"$set": {"numberofPotholes": tempArray}}
            dbQueryResult = coordinateCollection.update_one(updateQuery, update)
            print(f"set {numberofPotholes[0]} potholes in {dbQueryResult}")
        else:
            doc = {
                "name": str(uuid.uuid4()),
                "location": {"type": "Point", "coordinates": [longitude, latitude]},
                "numberofPotholes": numberofPotholes,
            }
            dbQueryResult = coordinateCollection.insert_one(doc).inserted_id
            print(f"new marker with {numberofPotholes[0]} potholes in  {dbQueryResult}")
