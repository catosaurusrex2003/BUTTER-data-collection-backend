from loguru import logger
import boto3
import time
from dotenv import find_dotenv, load_dotenv
import os
import requests
from io import BytesIO
from PIL import Image
from ultralytics import YOLO
import pickle
import json
import time
from utils.timit import time_it


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

cameraModel = YOLO("models/camera/Jul-26-2023-yoloV8m.pt")

with open("models/accelerometer/pothole-Jul-27-2023.pkl", "rb") as file:
    potholeModel = pickle.load(file)

with open("models/accelerometer/quality-Jul-27-2023.pkl", "rb") as file:
    qualityModel = pickle.load(file)

sqs_Client = boto3.client(
    "sqs",
    region_name=os.getenv("AWS_region"),
    aws_access_key_id=os.getenv("AWS_accessKeyId"),
    aws_secret_access_key=os.getenv("AWS_secretAccessKey"),
)

s3_client = boto3.client(
    "s3",
    region_name=os.getenv("AWS_region"),
    aws_access_key_id=os.getenv("AWS_accessKeyId"),
    aws_secret_access_key=os.getenv("AWS_secretAccessKey"),
)
queue_url = "https://sqs.ap-south-1.amazonaws.com/867190329008/myqueue"

bucket_name = "ipd-sqs-queue"


def download_image_to_memory(url):
    try:
        response = requests.get(url)
        logger.debug("Image Downloaded")
        response.raise_for_status()
        imageBytesIO = BytesIO(response.content)
        resized_image = Image.open(imageBytesIO)
        resized_image.thumbnail((400, 400), Image.ANTIALIAS)
        logger.debug("Image Resized")
        return resized_image
    except requests.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return False
    except Exception as err:
        logger.error(f"An error occurred: {err}")
        return False


def generate_signed_url(object_key):
    try:
        signed_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=120,  # 2 minutes
        )
        logger.debug("S3 Image Signed URL generate")
        return signed_url
    except Exception as e:
        logger.error("Error generating signed URL:", e)
        return False


def process_message_and_deque(message):
    """
    Process the message
    """
    logger.debug("RECIEVED MESSAGE: ", message["Body"])
    messageBody = json.loads(message["Body"])
    # url = generate_signed_url(messageBody["imageObjectId"])
    # if not url:
    #     logger.debug("no signed url generated")
    #     return
    resizedImage = download_image_to_memory(messageBody["imageUrl"])

    # Feed the 🍽 😋 model
    if not resizedImage:
        return
    results = cameraModel(resizedImage)
    if results:
        logger.critical(f"Number of POTHOLES in the image is {len(results[0])}")
        sqs_Client.delete_message(
            QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"]
        )
        logger.debug("deleted")


def runConcurrently(messagesArray):
    # tasks = [process_message_and_deque(message) for message in messagesArray]
    # await asyncio.gather(*tasks)
    for message in messagesArray:
        # asyncio.create_task(process_message_and_deque(message))
        process_message_and_deque(message)


@time_it
def main():
    shouldRun = True
    while shouldRun:
        logger.info("POLLING")
        response = sqs_Client.receive_message(
            QueueUrl=queue_url, MaxNumberOfMessages=10, WaitTimeSeconds=0
        )
        logger.info("POLLING done")
        if "Messages" in response:
            logger.warning(f'{len(response["Messages"])}  number of messages')
            runConcurrently(response["Messages"])
        else:
            shouldRun = False
            logger.error("no messages found")


# cProfile.run("main()")
# main()
# logger.debug("debug")
# logger.info("info")
# logger.warning("warning")
# logger.error("error")
# logger.critical("critical")
