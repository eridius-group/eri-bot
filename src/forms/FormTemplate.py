from discord.ui import Modal, TextInput
from discord import Embed, Interaction, TextStyle

from os import getenv

from psycopg import Connection, Cursor
from psycopg import connect as psycopg

from json import dumps

from src.lib import get_sql, log_content

class FormTemplate(Modal):
    con: Connection = psycopg(getenv("connection_string"))
    cur: Cursor = con.cursor()
    form_name = "Generic Form"

    async def on_submit(self, interaction: Interaction):
        response = interaction.response

        pairs = {}
        for component in self.children:
            component_dict = component.to_component_dict()
            pairs[component_dict["label"]] = component.value
        print(pairs)

        embed = Embed(title=self.form_name)
        embed.description = ""

        for item in pairs:
            embed.description += f"{item}: {pairs[item]}\n"

        embed.add_field(name="User", value=interaction.user.nick)
        embed.set_footer(text="Please review this request.")

        channel = await interaction.guild.fetch_channel(int(getenv("logs_channel")))
        await channel.send(embed=embed)

        form_sql = get_sql("add_form")

        self.cur.execute(form_sql, (interaction.user.id, interaction.user.nick, dumps(pairs)))
        self.con.commit()

        await log_content(interaction, f"{interaction.user.nick} submitted {self.form_name}.")

        await response.send_message(f'We have logged your Contractor Compensation. Your team lead will review it shortly.', ephemeral=True)