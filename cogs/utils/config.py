import os
import json
from dotenv import load_dotenv

load_dotenv()


def getenv(key):
    return os.getenv(key)

