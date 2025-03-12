from enum import Enum
from os import getenv

from discord import Interaction, InteractionResponse, Client

from psycopg import Connection, Cursor
from psycopg import connect as psycopg

from src.forms.Form3 import Form3
from src.forms.Form2 import Form2

from src.lib.main import log_content

tasks = [
    "2) Damaged Equipment",
    "3) Contractor Reimbursement"
]

FormItems = Enum("FormItems", {task: task for task in tasks})

class Forms:
    def __init__(self, bot: Client):
        self.con: Connection = psycopg(getenv("connection_string"))
        self.cur: Cursor = self.con.cursor()
        self.clock_cache = {}
        self.bot = bot

    async def file(self, interaction: Interaction, form: FormItems):
        response: InteractionResponse = interaction.response
        
        await log_content(interaction, f"{interaction.user.nick} started to file Form {form.value}.")
        if form == FormItems["2) Damaged Equipment"]:
            await response.send_modal(Form2())
        elif form == FormItems["3) Contractor Reimbursement"]:
            await response.send_modal(Form3())
        else:
            await response.send_message("Form not found", ephemeral=True)