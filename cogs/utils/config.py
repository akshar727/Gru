import os
import json
from dotenv import load_dotenv

load_dotenv()


def getenv(key):
    return os.getenv(key)

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data,f)

def open_json(filename):
    with open(filename, "r") as f:
        return json.loads(f.read())
