from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import find_dotenv, load_dotenv
import pymongo

"""

RUN THIS FILE ONCE IF YOU ARE CREATING A NEW DATABASE
this is to set the type of the location index as a GEOSPHERE

"""


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
MONGOURI = os.getenv("MONGOURI")

# Create a new client and connect to the server
client = MongoClient(MONGOURI, server_api=ServerApi("1"))


# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

coordinateCollection = client.ipd.coordinates

testCoordinateCollection = client.ipd.coordinateTest

coordinateCollection.create_index([("location", pymongo.GEOSPHERE)])
testCoordinateCollection.create_index([("location", pymongo.GEOSPHERE)])
