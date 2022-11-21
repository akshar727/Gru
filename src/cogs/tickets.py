from io import BytesIO
from nextcord.ext import commands
import nextcord as discord
import aiosqlite



active_ticket_users = []

class AddUser(discord.ui.Modal):
    def __init__(self, channel):
        super().__init__(
            "Add User To Ticket",
            timeout=300
        )

        self.channel = channel
        self.user = discord.ui.TextInput(
            label="User ID",
            min_length = 2,
            max_length=30,
            required=True,
            placeholder="User ID (Must be a number)"
        )
        self.add_item(self.user)
    async def callback(self, interaction: discord.Interaction) -> None:
        user = interaction.guild.get_member(int(self.user.value))
        if user is None:
            return await interaction.send("Invalid User ID. Make sure the user is in this server!")
        if self.channel.permissions_for(user).read_messages:
            return await interaction.send(f"{user.mention} is already in this ticket!",ephemeral=True)
        overwrites = discord.PermissionOverwrite(read_messages=True)
        await self.channel.set_permissions(user,overwrite=overwrites)
        await interaction.send(f"{user.mention} has been added to this ticket!",ephemeral=True)


class RemoveUser(discord.ui.Modal):
    def __init__(self, channel):
        super().__init__(
            "Remove User From Ticket",
            timeout=300
        )

        self.channel = channel
        self.user = discord.ui.TextInput(
            label="User ID",
            min_length = 2,
            max_length=30,
            required=True,
            placeholder="User ID (Must be a number)"
        )
        self.add_item(self.user)
    async def callback(self, interaction: discord.Interaction) -> None:
        user = interaction.guild.get_member(int(self.user.value))
        if user is None:
            return await interaction.send("Invalid User ID. Make sure the user is in this server!")
        overwrites = discord.PermissionOverwrite(read_messages=False)
        if not self.channel.permissions_for(user).read_messages:
            return await interaction.send(f"{user.mention} is not in this ticket!",ephemeral=True)
        await self.channel.set_permissions(user,overwrite=overwrites)
        await interaction.send(f"{user.mention} has been removed from this ticket!",ephemeral=True)




class TicketSettings(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        # self.user = user

    @discord.ui.button(label="Close Ticket",style=discord.ButtonStyle.danger, custom_id="ticket_settings:close")
    async def close_ticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        # if self.user != interaction.user.id:
        #     return await interaction.response.send_message("This is not your ticket!",ephemeral=True)
        messages = await interaction.channel.history(limit=None,oldest_first=True).flatten()
        contents = [message.content for message in messages]
        final = ""
        for msg in contents:
            msg = msg + "\n"
            final = final + msg
        await interaction.response.send_message("The ticket is being closed.",ephemeral=True)
        await interaction.channel.delete()
        active_ticket_users.remove(interaction.user.id)
        await interaction.user.send(f"Your ticket in {interaction.guild.name} has been closed successfully! Here was the transcript:",file=discord.File(BytesIO(final.encode("utf-8")),filename="transcript.txt"))

    @discord.ui.button(label="Add User",style=discord.ButtonStyle.green, custom_id="ticket_settings:add_user")
    async def add_user(self, button: discord.ui.Button, interaction: discord.Interaction):
        # if self.user != interaction.user.id:
        #     return await interaction.response.send_message("This is not your ticket!"
        #     ,ephemeral=True)
        await interaction.response.send_modal(AddUser(interaction.channel))

    @discord.ui.button(label="Remove User",style=discord.ButtonStyle.gray, custom_id="ticket_settings:remove_user")
    async def remove_user(self, button: discord.ui.Button, interaction: discord.Interaction):
        # if self.user != interaction.user.id:
        #     return await interaction.response.send_message("This is not your ticket!"
        #     ,ephemeral=True)
        await interaction.response.send_modal(RemoveUser(interaction.channel))


class CreateTicket(discord.ui.View):
    def __init__(self,bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Create Ticket",style=discord.ButtonStyle.blurple, custom_id="create_ticket:main")
    async def create_ticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id in active_ticket_users:
            return await interaction.response.send_message("You already have a ticket open! Close it to open a new one.",ephemeral=True)
        await interaction.response.send_message("A ticket is being created for you!",ephemeral=True)
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT role FROM ticketRoles WHERE guild = ?",(interaction.guild.id,))
            role = await cursor.fetchone()
            if role:
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    interaction.guild.me: discord.PermissionOverwrite(read_messages=True),
                    interaction.user: discord.PermissionOverwrite(read_messages=True),
                    interaction.guild.get_role(role[0]): discord.PermissionOverwrite(read_messages=True),
                }
            else:
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    interaction.guild.me: discord.PermissionOverwrite(read_messages=True),
                    interaction.user: discord.PermissionOverwrite(read_messages=True),
                }

        channel = await interaction.guild.create_text_channel(f"{interaction.user}-help", overwrites=overwrites)
        await interaction.edit_original_message(content=f"Ticket created successfully! {channel.mention}")
        embed = discord.Embed(title=f"Ticket for {interaction.user}",description=f"{interaction.user} has created a ticket.\nClick one of the buttons below to alter the settings of this ticket.", color=discord.Color.random())
        await channel.send(embed=embed,view=TicketSettings())
        active_ticket_users.append(interaction.user.id)





class Tickets(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def setup_tickets(self,ctx):
        embed = discord.Embed(title="Create A Ticket!", description = "Click the `Create Ticket` button below to create a new ticket. The server's staff will be notified and shortly aid you with your problem.",color=discord.Color.green())
        await ctx.send(embed=embed,view=CreateTicket(self.bot))
    # TODO: Add to help
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def ticket_role(self,ctx, role: discord.Role):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT role FROM ticketRoles WHERE guild = ?",(ctx.guild.id,))
            role2 = await cursor.fetchone()
            if role2:
                await cursor.execute("UPDATE ticketRoles SET role = ? WHERE guild = ?",(role.id,ctx.guild.id,))
                await ctx.send("Tickets Auto-Assigned role successfully updated!")
            else:
                await cursor.execute("INSERT INTO ticketRoles VALUES (?, ?)",(role.id,ctx.guild.id,))
                await ctx.send("Tickets Auto-Assigned role successfully added!")

    @commands.Cog.listener()
    async def on_ready(self):
        if self.bot.persistent_views_added is False:
            self.bot.add_view(CreateTicket(self.bot))
            self.bot.add_view(TicketSettings())
            self.bot.persistent_views_added = True
        print("Added Ticket Views!")




def setup(bot):
    bot.add_cog(Tickets(bot))