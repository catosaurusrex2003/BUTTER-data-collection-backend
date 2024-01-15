from fastapi import FastAPI, File, Form, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
from ultralytics import YOLO
import cv2
import numpy as np
import json
from util.replaceId import addPotholeId
from controllers.potholeController import potholeController
from helpers.queryAllPotholes import queryAllPotholes
import pickle
import base64
from PIL import Image
import io

app = FastAPI()

cameraModel = YOLO("models/camera/Jul-26-2023-yoloV8m.pt")

with open("models/accelerometer/pothole-Jul-27-2023.pkl", "rb") as file:
    potholeModel = pickle.load(file)

with open("models/accelerometer/quality-Jul-27-2023.pkl", "rb") as file:
    qualityModel = pickle.load(file)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Allow all origins (you can specify specific origins if needed)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
async def get():
    return {"working?": "yes i guess"}


@app.post("/predict")
def predict(
    file: bytes = File(None),
    base64str: str = Form(None),
    returnType: str = Form(None),
    returnFormat: str = Form("image"),
    coordinate: str = Form(),
):
    """
    Predict potholes in an image.

    Request Args:
        file: The image file to process.
        returnType: The format of the results to return, either "json" or "image".
        coordinate: The current coordinate of the image.

    Response:
        The results of the prediction, either as a JSON object or an image.
    """

    if base64str:
        image_bytes = base64.b64decode(base64str)
        print("recieved base64")
    elif file:
        image_bytes = file
        print("image file")
    else:
        return Response(status_code=400, content={"error": "No image file provided."})

    resized_image = Image.open(io.BytesIO(image_bytes))
    resized_image.thumbnail((400, 400), Image.ANTIALIAS)
    results = cameraModel(resized_image)
    coordinateObj = json.loads(coordinate)
    potholeController(
        coordinateObj["longitude"], coordinateObj["latitude"], len(results[0])
    )

    if returnType == "image":
        # Get the first result and plot it
        res_plotted = results[0].plot()

        # Convert the image to bytes
        _, img_encoded = cv2.imencode(".png", res_plotted)
        img_bytes = img_encoded.tobytes()

        # Create a response with the image bytes
        if returnFormat == "base64":
            baseStr = base64.b64encode(img_bytes)
            print("base64 string done sent")
            return baseStr
        else:
            response = Response(status_code=200, content=img_bytes)
            response.headers["Content-Type"] = "image/png"
            print("image done sent")
            return response

    else:  # json
        print("here")
        returnData = {}
        # doing this is necessary dont remove
        dataArray = json.loads(results[0].tojson())
        dataArray = addPotholeId(dataArray)
        returnData["potholesData"] = dataArray
        returnData["coordinate"] = json.loads(coordinate)
        returnData["numberPotholes"] = len(dataArray)
        print("json done sent")
        return returnData


async def processImageInBackground(image_bytes, coordinate):
    """
    This function processes image in background and populates the database

    Args:
        file : bytes string
        coordinate: sus
    Return:
        nothing
    """
    # resize
    resized_image = Image.open(io.BytesIO(image_bytes))
    resized_image.thumbnail((400, 400), Image.ANTIALIAS)

    # Feed the 🍽 😋 model
    results = cameraModel(resized_image)
    coordinateObj = json.loads(coordinate)
    potholeController(
        coordinateObj["longitude"], coordinateObj["latitude"], len(results[0])
    )


@app.post("/asyncpredict")
async def asyncpredict(
    file: bytes = File(None),
    base64str: str = Form(None),
    coordinate: str = Form(),
):
    """
    Predict potholes in an image.

    Request Args:
        file: The image file to process.
        coordinate: The current coordinate of the image.

    Response:
        -------NOTHING-------
        this
    """

    if base64str:
        image_bytes = base64.b64decode(base64str)
    elif file:
        image_bytes = file
    else:
        return Response(status_code=400, content={"error": "No image file provided."})

    # image_np = np.frombuffer(image_bytes, dtype=np.uint8)
    # image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    asyncio.create_task(processImageInBackground(image_bytes, coordinate))

    return {"message": "image recieved by server"}


@app.post("/quality")
async def qualitysensor(
    speed: str = Form(),
    accX: str = Form(),
    accY: str = Form(),
    accZ: str = Form(),
    gyroX: str = Form(),
    gyroY: str = Form(),
    gyroZ: str = Form(),
    coordinate: str = Form(),
):
    speed = float(speed)
    accX = float(accX)
    accY = float(accY)
    accZ = float(accZ)
    gyroX = float(gyroX)
    gyroY = float(gyroY)
    gyroZ = float(gyroZ)
    coordinateObj = json.loads(coordinate)
    print(speed, accX, accY, accZ, gyroX, gyroY, gyroZ, coordinateObj)
    data = np.array([[speed, accX, accY, accZ, gyroX, gyroY, gyroZ]])
    predictions = qualityModel.predict(data)
    if predictions[0]:
        potholeController(coordinateObj["longitude"], coordinateObj["latitude"], 1)
    print("VALUE IS :", predictions[0])
    return {"value": int(predictions[0])}


@app.post("/pothole")
async def potholesensor(
    speed: str = Form(),
    accX: str = Form(),
    accY: str = Form(),
    accZ: str = Form(),
    gyroX: str = Form(),
    gyroY: str = Form(),
    gyroZ: str = Form(),
    coordinate: str = Form(),
):
    speed = float(speed)
    accX = float(accX)
    accY = float(accY)
    accZ = float(accZ)
    gyroX = float(gyroX)
    gyroY = float(gyroY)
    gyroZ = float(gyroZ)
    coordinateObj = json.loads(coordinate)
    print(speed, accX, accY, accZ, gyroX, gyroY, gyroZ, coordinateObj)
    data = np.array([[speed, accX, accY, accZ, gyroX, gyroY, gyroZ]])
    predictions = potholeModel.predict(data)
    if predictions[0]:
        potholeController(coordinateObj["longitude"], coordinateObj["latitude"], 1)
    print("VALUE IS :", predictions[0])
    return {"value": int(predictions[0])}


@app.get("/getAllPotholes")
def getAllPotholes():
    potholeData = queryAllPotholes()
    return {"data": potholeData}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
    # uvicorn.run(app, host="192.168.0.104", port=5000)
