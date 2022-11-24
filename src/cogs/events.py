from nextcord.ext import commands
import nextcord as discord
import json
import random
from src.utils import config
import aiosqlite

fake_cmds = ['balance', '_help']


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        setattr(self.bot, "db", await aiosqlite.connect("main.db"))
        # check_giveaway_ended.start()
        # with open('databases/giveaways.json','r') as f:
        #     g = json.load(f)
        # with open('databases/tickets.json','r') as f:
        #     ticket_data = json.load(f)
        # active_ticket_users = ticket_data["active_ticket_users"]
        # if not self.bot.persistent_views_added:
        #     client.add_view(CreateTicket())
        #     for user in active_ticket_users:
        #         client.add_view(TicketSettings(user))
        #     for giveaway in g:
        #         client.add_view(view=JoinGiveaway(int(giveaway)),message_id=int(giveaway))
        #     client.persistent_views_added = True
        #     print('Added Giveaway Buttons and Tickets!')
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS ticketRoles (role INTEGER, guild INTEGER)")
            await cursor.execute(
                "CREATE TABLE IF NOT EXISTS levels (level INTEGER, xp REAL, user INTEGER, guild INTEGER)")
            await cursor.execute(
                "CREATE TABLE IF NOT EXISTS levelSettings (levelsys BOOL, role INTEGER, levelreq INTEGER, "
                "guild INTEGER)")
            await cursor.execute("CREATE TABLE IF NOT EXISTS prefixes (prefix TEXT, guild ID)")
            await cursor.execute(
                "CREATE TABLE IF NOT EXISTS jobs (name TEXT, pay INTEGER, hours INTEGER, fails INTEGER, user INTEGER)")
            await cursor.execute(
                "CREATE TABLE IF NOT EXISTS mainbank (wallet INTEGER, bank INTEGER, booster INTEGER, max INTEGER, "
                "user INTEGER)")
            await cursor.execute(
                "CREATE TABLE IF NOT EXISTS lootboxes  (common INTEGER, uncommon INTEGER, rare INTEGER, epic INTEGER, "
                "legendary INTEGER, mythic INTEGER, admin INTEGER, user INTEGER)")
            await cursor.execute(
                "CREATE TABLE IF NOT EXISTS giveaways (time INTEGER, prize TEXT, participants TEXT, message INTEGER, "
                "channel INTEGER, guild INTEGER, winners INTEGER, finished BOOL)")
            await cursor.execute("CREATE TABLE IF NOT EXISTS ticketUsers (user INTEGER, guild INTEGER)")
        print("Connected to {0.user}".format(self.bot))
        print("All database tables are ready to use!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not member.bot:
            try:
                await member.send(
                    f'''Hi {member.name}, welcome to {member.guild.name}!''')
            except:
                print(f"Cannot send messages to {member}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            pass

        else:
            with open('databases/reactrole.json', 'r') as react_file:
                data = json.load(react_file)
                for x in data:
                    if x['emoji'] == payload.emoji.name or\
                            x['emoji'] == f"<:{payload.emoji.name}:{payload.emoji.id}>" or\
                            x['emoji'] == f"<a:{payload.emoji.name}:{payload.emoji.id}>":
                        role = discord.utils.get(self.bot.get_guild(
                            payload.guild_id).roles,
                                                 id=x['role_id'])
                        if role:
                            await payload.member.add_roles(role)
                        else:
                            del x

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        with open('databases/reactrole.json', 'r') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name or\
                        x['emoji'] == f"<:{payload.emoji.name}:{payload.emoji.id}>" or\
                        x['emoji'] == f"<a:{payload.emoji.name}:{payload.emoji.id}>":
                    role = discord.utils.get(self.bot.get_guild(
                        payload.guild_id).roles,
                                             id=x['role_id'])
                    if role:
                        await self.bot.get_guild(payload.guild_id
                                                 ).get_member(payload.user_id
                                                              ).remove_roles(role)
                    else:
                        del x

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        try:
            if message.mentions[0] == self.bot.user and message.content == '<@874328552965820416>':
                prefix = await config.get_prefix(self.bot, message.guild.id)
                await message.channel.send(f"My prefix for this server is `{prefix}`")
        except IndexError:
            pass
        author = message.author
        guild = message.guild
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT levelsys FROM levelSettings WHERE guild = ?", (guild.id,))
            levelsys = await cursor.fetchone()
            if levelsys and not levelsys[0]:
                # 0: False, 1: True
                return
            await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?", (author.id, guild.id,))
            xp = await cursor.fetchone()
            await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?", (author.id, guild.id,))
            level = await cursor.fetchone()

            if not xp or not level:
                await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)",
                                     (1, 0, author.id, guild.id,))
                await self.bot.db.commit()
            try:
                xp = xp[0]
                level = level[0]
            except TypeError:
                xp = 1.3
                level = 1

            xp += level * 1.3
            await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (xp, author.id, guild.id,))

            level_start = level
            level_end = int(xp ** (1 / 4))
            if level_start < level_end:
                await cursor.execute("UPDATE levels SET level = ? WHERE user = ? AND guild = ?",
                                     (level_end, author.id, guild.id,))
                await cursor.execute("SELECT role FROM levelSettings WHERE levelReq = ? AND guild = ?",
                                     (level_end, guild.id,))
                role = await cursor.fetchone()
                if role:
                    role = role[0]
                    role = guild.get_role(role)
                    try:
                        await author.add_roles(role)
                        return await message.channel.send(
                            'Congratulations! {} has leveled up to **Level {}** and has a total of **{} xp**! :tada: '
                            ':tada: They also recieved the **{}** role!'.format(
                                author.mention, level_end, round(xp), role.name))
                    except discord.HTTPException:
                        return await message.channel.send(
                            'Congratulations! {} has leveled up to **Level {}** and has a total of **{} xp**! :tada: '
                            ':tada: [WAS NOT ABLE TO GIVE LEVEL REWARD ROLE]'.format(
                                author.mention, level_end, round(xp)))
                await message.channel.send(
                    'Congratulations! {} has leveled up to **Level {}** and has a total of **{} xp**! :tada: :tada:'
                    .format(
                        author.mention, level_end, round(xp)))
        await self.bot.db.commit()

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        await config.open_account(ctx.author)
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT max from mainbank WHERE user = ?", (ctx.author.id,))
            max_amt = await cursor.fetchone()
            max_amt = max_amt[0]
            if ctx.command.qualified_name not in fake_cmds:
                max_amt += random.randint(50, 5000)
                await cursor.execute("UPDATE mainbank SET max = ? WHERE user = ?", (max_amt, ctx.author.id,))
        await self.bot.db.commit()

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        with open('databases/reactrole.json', 'r') as f:
            reaction_roles = json.load(f)
        msgs = [
            reaction_role_id["message_id"] for reaction_role_id in reaction_roles
        ]
        if payload.message_id not in msgs:
            return
        else:
            for i in range(len(reaction_roles)):
                if reaction_roles[i]["message_id"] == payload.message_id:
                    del reaction_roles[i]
                    break
            with open('databases/reactrole.json', 'w') as f:
                json.dump(reaction_roles, f, indent=4)


#         with open('databases/lootboxes.json', 'r') as f:
#             lootboxes = json.load(f)
#         if lvl_end - lvl_start > 1:
#             await channel.send("Wow, you got a lot of lootboxes!")
#             crates = []
#             for i in range(0, lvl_end - lvl_start):
#                 crate_type = random.choice([
#                     "mythic", "legendary", "legendary", "epic", "epic", "epic",
#                     "epic", "rare", "rare", "rare", "rare", "rare", "rare",
#                     "rare", "uncommon", "uncommon", "uncommon", "uncommon",
#                     "uncommon", "uncommon", "uncommon", "uncommon", "uncommon",
#                     "common", "common", "common", "common", "common", "common",
#                     "common", "common", "common", "common"
#                 ])
#                 lootboxes[str(user.id)][crate_type] += 1
#                 crates.append(crate_type)
#             m_amt = len([i for i, x in enumerate(crates) if x == "mythic"])
#             l_amt = len([i for i, x in enumerate(crates) if x == "legendary"])
#             e_amt = len([i for i, x in enumerate(crates) if x == "epic"])
#             r_amt = len([i for i, x in enumerate(crates) if x == "rare"])
#             u_amt = len([i for i, x in enumerate(crates) if x == "uncommon"])
#             c_amt = len([i for i, x in enumerate(crates) if x == "common"])
#             await channel.send(
#                 f"You found:\n {m_amt} Mythic box{'es' if m_amt > 1 or m_amt == 0 else ''}\n {l_amt} Legendary box{'es' if l_amt > 1 or l_amt == 0 else ''}\n {e_amt} Epic box{'es' if e_amt > 1 or e_amt == 0 else ''}\n {r_amt} Rare box{'es' if r_amt > 1 or r_amt == 0 else ''}\n {u_amt} Uncommon box{'es' if u_amt > 1 or u_amt == 0 else ''} and\n {c_amt} Common box{'es' if c_amt > 1 or c_amt == 0 else ''} :tada: :tada: <:chest:898333946557894716> <:chest:898333946557894716> <:chest:898333946557894716>"
#             )

#         else:
#             crate_type = random.choice([
#                 "mythic", "legendary", "legendary", "epic", "epic", "epic",
#                 "epic", "rare", "rare", "rare", "rare", "rare", "rare", "rare",
#                 "uncommon", "uncommon", "uncommon", "uncommon", "uncommon",
#                 "uncommon", "uncommon", "uncommon", "uncommon", "common",
#                 "common", "common", "common", "common", "common", "common",
#                 "common", "common", "common"
#             ])
#             await channel.send(
#                 f"You earned a **{crate_type.capitalize()}** <:chest:898333946557894716> lootbox!! :tada:"
#             )
#             lootboxes[str(user.id)][crate_type] += 1
#         with open('databases/lootboxes.json', 'w') as f:
#             json.dump(lootboxes, f, indent=4)
#         users[str(user.guild.id)][str(user.id)]['level'] = lvl_end
#         with open('databases/levels.json', 'w') as f:
#             json.dump(users, f, indent=4)


def setup(bot):
    bot.add_cog(Events(bot))
