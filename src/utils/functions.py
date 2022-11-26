import os
import dotenv
import time
# import json
import random
import aiosqlite

dotenv.load_dotenv()
working_users = []


def convert_str_to_number(x):
    """Converts a string to a number

    Args:
        x (str): The string to convert

    Returns:
        int: The converted number
    """
    total_stars = 0
    num_map = {'K': 1000, 'M': 1000000, 'B': 1000000000}
    if x.isdigit():
        total_stars = int(x)
    else:
        if len(x) > 1:
            total_stars = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
    return int(total_stars)


def getenv(key: str):
    """Gets any env file key
    Args:
        key (str): The key to get
    """
    return os.getenv(key)


def timetext(name):
    """ Timestamp, but in text form
     Args:
            name (str): The name of the timestamp
     """
    return f"{name}_{int(time.time())}.txt"


async def get_prefix(bot, guild_id):
    """Gets the prefix for a guild

    Args:
        bot (GruBot): The bot
        guild_id (int): The guild id to get the prefix for

    Returns:
        str: The prefix for the guild or the default prefix if the guild doesn't have a prefix set

    """
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT prefix FROM prefixes WHERE guild = ?", (guild_id,))
        prefix = await cursor.fetchone()
        if prefix:
            return prefix[0]
        else:
            return getenv("BOT_PREFIX")


async def update_bank(user, change=0, mode='wallet') -> list[int]:
    """Updates the users bank or gets all the data of it

        Args:
            user (discord.User, discord.Member): The user to update the bank for
            change (int, optional): The amount to change the bank by. Defaults to 0.
            mode (str, optional): The bank to change. Defaults to 'wallet'.

        Returns:
            list[int]: The wallet, bank, max bank, and booster in a list

        """
    db = await aiosqlite.connect("main.db")
    async with db.cursor() as cursor:
        await cursor.execute("SELECT wallet, bank, max, booster, max FROM mainbank WHERE user = ?", (user.id,))
        data = await cursor.fetchone()
        if mode == 'wallet':
            await cursor.execute("UPDATE mainbank SET wallet = wallet + ? WHERE user = ?", (change, user.id))
        if mode == 'bank':
            await cursor.execute("UPDATE mainbank SET bank = bank + ? WHERE user = ?", (change, user.id))
        await db.commit()
        return list(data)


async def add_lootbox(user, lootbox, amount) -> None:
    """Adds a lootbox to a user

            Args:
                user (discord.User): The user to add the lootbox to
                lootbox (str): The lootbox to add
                amount (int): The amount to add

            """
    db = await aiosqlite.connect("main.db")
    async with db.cursor() as cursor:
        await cursor.execute(f"UPDATE lootboxes SET {lootbox} = {lootbox} + {amount} WHERE user = ?", (user.id,))
    await db.commit()


async def get_job(user):
    """Gets the users job data

            Args:
                user (discord.User): The user to get the job data for

            Returns:
                list: The job name, pay, hours, and fails in a list

            """
    db = await aiosqlite.connect("main.db")
    async with db.cursor() as cursor:
        await cursor.execute("SELECT name, pay, hours, fails FROM jobs WHERE user = ?", (user.id,))
        data = await cursor.fetchone()
        return data


async def open_account(user):
    """Opens an account for a user

            Args:
                user (discord.User, discord.Member): The user to open an account for


            """
    db = await aiosqlite.connect("main.db")
    async with db.cursor() as cursor:
        await cursor.execute("SELECT wallet FROM mainbank WHERE user = ?", (user.id,))
        bank_data = await cursor.fetchone()
        if not bank_data:
            await cursor.execute("INSERT INTO mainbank (wallet, bank, booster, max, user) VALUES (?, ?, ?, ?, ?)",
                                 (random.randint(0, 3000), 0, 1, 100, user.id,))
        await cursor.execute("SELECT name FROM jobs WHERE user = ?", (user.id,))
        job_data = await cursor.fetchone()
        if not job_data:
            await cursor.execute("INSERT INTO jobs (name, pay, hours, fails, user) VALUES (?, ?, ?, ?, ?)",
                                 ("None", 0, 0, 0, user.id,))
        await cursor.execute("SELECT common FROM lootboxes WHERE user = ?", (user.id,))
        lootbox_data = await cursor.fetchone()
        if not lootbox_data:
            await cursor.execute(
                "INSERT INTO lootboxes (common, uncommon, rare, epic, legendary, mythic, admin, user) VALUES "
                "(?, ?, ?, ?, ?, ?, ?, ?)",
                (0, 0, 0, 0, 0, 0, 0, user.id,))
    await db.commit()
