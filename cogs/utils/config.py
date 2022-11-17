import os
import dotenv
import time
import json
import random

dotenv.load_dotenv()
working_users= []


def getenv(key):
    """Gets any env file key"""
    return os.getenv(key)

def timetext(name):
    """ Timestamp, but in text form """
    return f"{name}_{int(time.time())}.txt"

async def open_account(user):
    users = await get_bank_data()
    jobs = await get_job_data()
    lootbox_data = await get_lootbox_data()

        
    if not str(user.id) in users:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = random.randint(0, 3000)
        users[str(user.id)]["bank"] = 0
        users[str(user.id)]["booster"] = 1
        users[str(user.id)]["max"] = 10
    if not str(user.id) in jobs:
        jobs[str(user.id)] = {}
        jobs[str(user.id)]["job"] = {}
        jobs[str(user.id)]["job"]["name"] = 'None'
        jobs[str(user.id)]["job"]["pay"] = 0
        jobs[str(user.id)]["job"]["hours"] = 0
        jobs[str(user.id)]['job']['fails'] = 0
    if not str(user.id) in lootbox_data:
        lootbox_data[str(user.id)] = {}
        lootbox_data[str(user.id)]["common"] = 0
        lootbox_data[str(user.id)]["uncommon"] = 0
        lootbox_data[str(user.id)]["rare"] = 0
        lootbox_data[str(user.id)]["epic"] = 0
        lootbox_data[str(user.id)]["legendary"] = 0
        lootbox_data[str(user.id)]["mythic"] = 0
        lootbox_data[str(user.id)]["admin"] = 0

    with open('databases/mainbank.json', 'w') as f:
        json.dump(users, f, indent=4)
    with open('databases/jobs.json', 'w') as f:
        json.dump(jobs, f, indent=4)
    with open('databases/lootboxes.json', 'w') as f:
        json.dump(lootbox_data, f, indent=4)

    return True
