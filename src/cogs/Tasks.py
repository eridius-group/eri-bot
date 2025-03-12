from enum import Enum
from os import getenv

from discord import Embed, Interaction, Thread, Forbidden, HTTPException, Member, Client, InteractionResponse

from src.lib import log_content

class TaskPriorities(Enum):
    Low = "🟩"
    Medium = "🟨"
    High = "🟧"
    Critical = "🟥"

class Tasks:
    def __init__(self, bot: Client):
        self.task_channel: int = int(getenv("tasks_channel")) or 0
        self.bot = bot

    async def task(self, interaction: Interaction, name: str, assigned: Member, description: str = "", priority: TaskPriorities = "🟩", rate: str = "0"):
        response: InteractionResponse = interaction.response

        if rate.isdigit():
            rate = f"US${rate}"
        else:
            rate = "N/A"

        thread_name = f"{priority} {name}"

        embed = Embed(title=thread_name)
        embed.description = f"{description.replace("\\n", "\n")}\n \n**Rate:** {rate}\n**Assigned to:** {assigned.mention}"
        embed.description += "\n\n To receive payment, use `/clock in` when you start working, and then clock out using `/clock out`. If you forget to clock in/out, please contact your team leader."
        embed.description += "\n\n Most tasks are not paid hourly, but time is considered for payment. If you have any questions, please ask your team leader."
        embed.description += "\n\n Once you clock in, you are considered to be performing contracted labor, as defined in the Eridius Handbook. If you have any questions about the handbook, or what this means, contact your team leader."
        embed.set_footer(text="Task created by {}".format(interaction.user.nick))

        thread_channel = await self.bot.fetch_channel(int(getenv("tasks_channel")))

        await log_content(interaction, f"{interaction.user.nick} created {thread_channel.name}.")

        try:
            thread = await thread_channel.create_thread(name=thread_name, embed=embed)
            await thread.thread.send(f"Task is assigned to {assigned.mention}")
            await thread.thread.add_user(assigned)
        except Forbidden:
            await response.send_message("I don't have the necessary permissions to create a thread.", ephemeral=True)
            return
        except HTTPException as e:
            await response.send_message(f"An error occurred: {e}", ephemeral=True)
            return
        await response.send_message("Task created!", ephemeral=True)

    async def resolve(self, interaction: Interaction, message: str = "No resolve message provided."):
        response: InteractionResponse = interaction.response

        await log_content(interaction, f"{interaction.user.nick} resolved {interaction.channel.name}")

        if not isinstance(interaction.channel, Thread):
            await response.send_message("This command can only be used in a forum thread.", ephemeral=True)
            return

        embed = Embed(title="Resolved")
        embed.description = "This task was resolved by {}.".format(interaction.user.nick)
        embed.description += "\n\n{}".format(message.replace("\\n", "\n"))

        await response.send_message(embed=embed)

        try:
            await interaction.channel.edit(archived=True, locked=True)
        except Forbidden:
            await response.send_message("I don't have the necessary permissions to close this thread.", ephemeral=True)
        except HTTPException as e:
            await response.send_message(f"An error occurred: {e}", ephemeral=True)