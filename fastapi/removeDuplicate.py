from helpers.dbConnect import coordinateCollection

pipeline = [
    {
        "$group": {
            "_id": "$location.coordinates",
            "docs": {"$push": "$_id"}
        }
    },
    {
        "$project": {
            "keepId": {"$arrayElemAt": ["$docs", 0]}
        }
    },
    {
        "$group": {
            "_id": None,
            "ids": {"$push": "$keepId"}
        }
    }
]

result = coordinateCollection.aggregate(pipeline)
