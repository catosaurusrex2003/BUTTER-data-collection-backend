import pprint
import uuid
from helpers.dbConnect import coordinateCollection
from helpers.queryDatabaseForPotholes import queryDatabaseForPotholes


def potholeController(long, lat, amt=0):
    """
    Checks for pothole marker in vicinity.
    if found then increments the number of potholes in it.
    else creates a new marker.

    Args:
        longitude
        latitude
        amt of potholes
    Return:
        the object of the pothole found else None
    """

    result = queryDatabaseForPotholes(long, lat, 20)

    if result:
        print(result)
        updateQuery = {"_id": result["_id"]}
        tempArray = result["numberofPotholes"]
        if len(tempArray) >= 10:
            tempArray.pop(0)
            tempArray.append(amt)
        else:
            tempArray.append(amt)
        update = {"$set": {"numberofPotholes": tempArray}}
        dbQueryResult = coordinateCollection.update_one(updateQuery, update)
        print(f"set {amt} potholes in {dbQueryResult}")
    else:
        doc = {
            "name": str(uuid.uuid4()),
            "location": {"type": "Point", "coordinates": [long, lat]},
            "numberofPotholes": [amt],
        }
        dbQueryResult = coordinateCollection.insert_one(doc).inserted_id
        print(f"new marker with {amt} potholes in  {dbQueryResult}")


# these two points have 1 meter difference in them
# lat = 19.111271921156934
# long = 72.87716353433828
# lat = 19.111280286000000
# long = 72.877167000000000
# name = "mpn2"

# potholeController(long,lat)


# doc = {
#     "name": str(uuid.uuid4()),
#     "location": {"type": "Point", "coordinates": [long, lat]},
#     "numberofPotholes": [amt], #
# }

# image   -> number of potholes
# sensor  -> yes or no pothole

# quality -> road quality


# time base sensor

# ek darkness detecting
