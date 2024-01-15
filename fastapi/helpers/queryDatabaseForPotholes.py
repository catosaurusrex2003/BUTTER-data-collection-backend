from helpers.dbConnect import coordinateCollection

# 1 degree long = 111km at equator 0km at pole
# 1 degree latt = 111km approx
def queryDatabaseForPotholes(long, lat):
    """
    Queries data base for potholes under one metre from current detected position.
    Args:
        longitude
        latitude
    Return:
        the object of the pothole found else None
    """

    query = {
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [long, lat],
                },
                # in meters. and this is legit. damn
                "$maxDistance": 1,
            }
        }
    }
    # this find the nearest point to the pothole under 1 meter.
    result = coordinateCollection.find_one(query)
    return result
