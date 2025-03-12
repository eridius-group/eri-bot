from os import getenv

from src.lib.main import get_sql

from discord import Embed, Client
from discord.ext import tasks
from discord.channel import TextChannel

from psycopg import connect as psycopg
from psycopg.cursor import Cursor
from psycopg.connection import Connection

from requests import Response
from requests import get

from markdownify import markdownify as md

class Mastodon:
    def __init__(self, bot: Client):
        self.con: Connection = psycopg(getenv("connection_string"))
        self.cur: Cursor = self.con.cursor()
        self.channel_id = int(getenv("mastodon_channel")) or 0
        self.mastodon_id = getenv("mastodon_id") or "114043102431589542"
        self.mastodon_instance = getenv("mastodon_instance") or "https://mastodon.social"
        self.bot = bot

    @tasks.loop(seconds=10)
    async def check_mastodon(self):
        channel: TextChannel = await self.bot.fetch_channel(self.channel_id)
        response: Response = get(f"{self.mastodon_instance}/api/v1/accounts/{self.mastodon_id}/statuses?exclude_replies=true")

        response_json = response.json()

        post_sql = get_sql("get_posts")
        add_post_sql = get_sql("add_post")

        posts = []

        for post in response_json:
            self.cur.execute(post_sql, (post['id'],))
            result = self.cur.fetchone()

            if result:
                continue

            content: str = post['content'] or ""
            content: str = content.replace("-", "\\-")

            embed: Embed = Embed(title=post['account']['display_name'], description=md(content))
            embed.set_footer(text=f"Posted at {post['created_at']}")
            posts.append({"id": post['id'], "embed": embed})

        for post in list(reversed(posts)):
            msg = await channel.send(embed=post['embed'])
            self.cur.execute(add_post_sql, (post['id'], msg.id))
            self.con.commit()