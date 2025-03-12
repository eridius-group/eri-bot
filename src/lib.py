from os import getenv

from discord import Interaction, Embed, Forbidden

async def log_content(interaction: Interaction, content: str):
    response = interaction.response
    try:
        logs_channel = await interaction.guild.fetch_channel(int(getenv("logs_channel")) or 0)
        embed = Embed(title="Log Event")
        embed.description = content or "Empty log event."
        embed.add_field(name="User", value=interaction.user.nick)
        embed.add_field(name="Channel", value=interaction.channel.name)
        await logs_channel.send(embed=embed)
    except Forbidden:
        await response.send_message("I do not have permission to send messages in the logs channel.", ephemeral=True)
        return
    except Exception as e:
        print(e)
        await response.send_message("An error occurred while logging this action.", ephemeral=True)
        return

async def check_access(interaction: Interaction):
    await log_content(interaction, f"{interaction.user.nick} has ran an administrative command.")
    if interaction.user.get_role(int(getenv("admin_role"))):
        return True
    return False

def get_sql(name: str) -> bytes:
    with open(f"src/sql/{name}.sql", "rb") as file:
        return file.read()