import os
import dotenv
import time
import json
import random
import aiosqlite

dotenv.load_dotenv()
working_users= []


def getenv(key):
    """Gets any env file key"""
    return os.getenv(key)

def timetext(name):
    """ Timestamp, but in text form """
    return f"{name}_{int(time.time())}.txt"


async def get_prefix(bot,guild_id):
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT prefix FROM prefixes WHERE guild = ?", (guild_id,))
        prefix = await cursor.fetchone()
        if prefix:
            return prefix[0]
        else:
            return getenv("BOT_PREFIX")

async def open_account(user):
    db = await aiosqlite.connect("main.db")
    async with db.cursor() as cursor:
        await cursor.execute("SELECT wallet FROM mainbank WHERE user = ?",(user.id,))
        bank_data = await cursor.fetchone()
        if not bank_data:
            await cursor.execute("INSERT INTO mainbank (wallet, bank, booster, max, user) VALUES (?, ?, ?, ?, ?)",(random.randint(0,3000),0,1,100,user.id,))
        await cursor.execute("SELECT name FROM jobs WHERE user = ?",(user.id,))
        job_data = await cursor.fetchone()
        if not job_data:
            await cursor.execute("INSERT INTO jobs (name, pay, hours, fails, user) VALUES (?, ?, ?, ?, ?)",("None",0,0,0,user.id,))
        await cursor.execute("SELECT common FROM lootboxes WHERE user = ?",(user.id,))
        lootbox_data = await cursor.fetchone()
        if not lootbox_data:
            await cursor.execute("INSERT INTO lootboxes (common, uncommon, rare, epic, legendary, mythic, admin, user) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",(0, 0, 0, 0, 0, 0, 0,user.id,))
    await db.commit()

    return True

