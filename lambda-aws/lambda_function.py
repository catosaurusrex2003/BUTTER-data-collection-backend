import os
from pymongo import MongoClient
from bson.json_util import dumps

client = MongoClient(host=os.environ.get("ATLAS_URI"))

coordinateCollection = client.ipd.coordinate

def queryAllPotholes():
    """
    Queries data base for all potholes.
    Args:
        NOTHING
    Return:
        The array of potholes
    """
    result = coordinateCollection.find()
    allPotholes = []
    for document in result:
        del document["name"]
        allPotholes.append(document)
    return dumps(allPotholes)

def lambda_handler(event, context):
    # Name of database
    potholeData = queryAllPotholes()
    return {"data": potholeData}