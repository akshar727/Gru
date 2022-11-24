from io import BytesIO

import nextcord as discord
from nextcord import SlashOption, Interaction
from nextcord.ext import commands
from src.utils import img_apis


# Credit to AlexFlipnote for all these image apis.
# TODO: Add all commands here to help
class AlexApis(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="captcha", description="Create a captcha image.")
    async def captcha(self, interaction: Interaction,
                      text: str = SlashOption(name="text", description="The text to put on the captcha.")):
        """Create a captcha image."""
        await interaction.response.send_message(file=discord.File(img_apis.create_captcha(text), "captcha.png"))

    @discord.slash_command(name="drake", description="Create a drake meme.")
    async def drake(self, interaction: Interaction,
                    top: str = SlashOption(description="The text to put next to the top picture"),
                    bottom: str = SlashOption(description="The text to put next to the bottom picture")):
        """Create a drake meme."""
        await interaction.response.send_message(file=discord.File(img_apis.create_drake(top, bottom), "drake.png"))

    @discord.slash_command(name="calling", description="Create a calling meme.")
    async def calling(self, interaction: Interaction,
                      text: str = SlashOption(description="The text to put on the meme.")):
        await interaction.response.send_message(file=discord.File(img_apis.create_calling(text), "calling.png"))

    @discord.slash_command(name="achievement", description="Create an achievement image from Minecraft.")
    async def achievement(self,
                          interaction: Interaction,
                          title: str = SlashOption(description="The title of the achievement", required=True,
                                                   default="Achievement Get!"),
                          achievement_text: str = SlashOption(description="The actual achievement (Ex: We need to go "
                                                                          "deeper)",
                                                              required=True),
                          color1: int = SlashOption(description="The 1st color value (red) 0-255", required=True),
                          color2: int = SlashOption(description="The 2nd color value (green) 0-255", required=True),
                          color3: int = SlashOption(description="The 3rd color value (blue) 0-255", required=True),
                          color4: int = SlashOption(description="The last color value (opacity) 0-255", required=True),
                          icon: int = SlashOption(description="Icon for the achievement (leave blank for random"
                                                              "). Icons can be found in the gru achicons command",
                                                  required=False)
                          ):
        """Create an achievement image."""
        color = (color1, color2, color3, color4)
        await interaction.response.send_message(
            file=discord.File(img_apis.create_achievement(title, achievement_text, color, icon), "achievement.png"))

    @discord.slash_command(name="achicons", description="Get a list of all the achievement icons.")
    async def achicons(self, interaction: Interaction):
        """Get a list of all the achievement icons."""
        await interaction.response.send_message(
            "".join([f"{i}: {img_apis.helper_icons[i]}\n" for i in img_apis.helper_icons]), ephemeral=True)

    @discord.slash_command(name="scroll", description="Create a scroll of truth image.")
    async def scroll_of_truth(self, interaction: Interaction,
                              text: str = SlashOption(description="The text to put on the scroll of truth.")):
        """Create a scroll of truth image."""
        img = img_apis.create_scroll(text)
        if not isinstance(img, BytesIO):
            return await interaction.response.send_message("You entered too much text! Try the command again with "
                                                           "less than `60` characters", ephemeral=True)
        await interaction.response.send_message(file=discord.File(img, "sot.png"))


def setup(bot):
    bot.add_cog(AlexApis(bot))
