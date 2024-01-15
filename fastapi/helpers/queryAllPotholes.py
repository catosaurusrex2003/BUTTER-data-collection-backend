from helpers.dbConnect import coordinateCollection
from bson.json_util import dumps

# 1 degree long = 111km at equator 0km at pole
# 1 degree latt = 111km approx
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
