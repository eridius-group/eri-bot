from enum import Enum
from os import getenv

from discord import Client, Interaction, Embed, InteractionResponse

tasks = [
    "company",
    "eri"
]

AboutOptions = Enum("AboutOptions", {task: task for task in tasks})

class About:
    def __init__(self, bot: Client):
        self.bot = bot
        self.company: str = getenv("company") or "Eridius Group LLC"
        self.existed: str = getenv("existed") or "2025"
        self.location: str = getenv("location") or "United States"
        self.website: str = getenv("website") or "https://eridius.org"
        self.description: str = getenv("description") or "We build open software for the people."

    async def company_dialog(self, interaction: Interaction):
        response: InteractionResponse = interaction.response

        embed = Embed(title=self.company)
        embed.description = self.description
        embed.add_field(name="Open Since", value="{}".format(self.existed))
        embed.add_field(name="Location", value="{}".format(self.location))
        embed.add_field(name="Website", value="{}".format(self.website))
        embed.set_footer(text="Powered by Eridius Eri™ Software https://eridius.org/eri")

        await response.send_message(embed=embed)

    async def eri(self, interaction: Interaction):
        response: InteractionResponse = interaction.response

        embed = Embed(title="Eri by Eridius")
        embed.description = "Eri is a utility for Discord to help manage employees, tasks, and more. Eri is source-available software, so you can have peace of mind that your data is handled properly."
        embed.set_footer(text="Powered by Eridius Eri™ Software https://eridius.org/eri")

        await response.send_message(embed=embed)

    async def entry(self, interaction: Interaction, req_type: AboutOptions = AboutOptions["company"]):
        if req_type == AboutOptions["company"]:
            await self.company_dialog(interaction)
        elif req_type == AboutOptions["eri"]:
            await self.eri(interaction)
        else:
            await self.company_dialog(interaction)