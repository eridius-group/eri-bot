from discord import Embed, Interaction, Forbidden, HTTPException, Client
from discord.interactions import InteractionResponse

from os import getenv

from src.lib import check_access

class Announcements:
    def __init__(self, bot: Client):
        self.bot = bot
        self.target_channel: int = int(getenv("announcements_channel")) or 0

    async def announce(self, interaction: Interaction, message: str):
        response: InteractionResponse = interaction.response

        if not await check_access(interaction):
            await response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        channel = await self.bot.fetch_channel(self.target_channel)

        if not channel:
            await response.send_message("The announcement channel is not set or cannot be reached.", ephemeral=True)
            return

        embed = Embed(title="Announcement")
        embed.description = message.replace("\\n", "\n")
        embed.set_footer(text="Announcement by {}".format(interaction.user.nick))

        try:
            await channel.send(embed=embed)
        except Forbidden:
            await response.send_message("I do not have permission to send messages in the announcement channel.", ephemeral=True)
            return
        except HTTPException:
            await response.send_message("An error occurred while sending the announcement.", ephemeral=True)
            return

        await response.send_message("Announcement sent!", ephemeral=True)