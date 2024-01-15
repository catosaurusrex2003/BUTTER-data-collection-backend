import uuid

def addPotholeId(data):
    for item in data:
        pothole_id = str(uuid.uuid4())
        item["pothole_id"] = pothole_id
        item["x1"] = item["box"]["x1"]
        item["x2"] = item["box"]["x2"]
        item["y1"] = item["box"]["y1"]
        item["y2"] = item["box"]["y2"]
        del item["name"]
        del item["class"]
        del item["box"]
    return data