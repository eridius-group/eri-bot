from os import getenv

from discord import Embed, Client, Interaction, InteractionResponse

from psycopg import connect as psycopg
from psycopg.cursor import Cursor
from psycopg.connection import Connection

from src.lib import get_sql

class Leaderboard:
    def __init__(self, bot: Client):
        self.con: Connection = psycopg(getenv("connection_string"))
        self.cur: Cursor = self.con.cursor()
        self.bot = bot

    async def leaderboard(self, interaction: Interaction):
        response: InteractionResponse = interaction.response
        
        get_leaderboard_sql = get_sql("get_leaderboard")

        embed = Embed(title="Leaderboard")

        self.cur.execute(get_leaderboard_sql)

        content = ""

        leaderboard_rows = enumerate(self.cur.fetchall())
        for i, row in leaderboard_rows:
            user = await self.bot.fetch_user(row[1])
            content += "{}. {} - {} messages\n".format(i + 1, user.name, row[2])

        embed.description = content

        await response.send_message(embed=embed)