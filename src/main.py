from os import getenv
from discord import Intents, Client, app_commands, Interaction, Message, Member
from psycopg import connect as psycopg
from dotenv import load_dotenv

from src.cogs.About import About, AboutOptions
from src.cogs.Announcements import Announcements
from src.cogs.Forms import Forms, FormItems
from src.cogs.Leaderboard import Leaderboard
from src.cogs.Mastodon import Mastodon
from src.cogs.Tasks import Tasks, TaskPriorities
from src.cogs.Timeclock import Timeclock, TimeclockTasks

from src.lib.main import get_sql

settings = {}
clock_cache = {}

load_dotenv()

intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)
tree = app_commands.CommandTree(client)
con = psycopg(getenv("connection_string"))
cur = con.cursor()

announcement = Announcements(client)
formClass = Forms(client)
leaderboard = Leaderboard(client)
task_object = Tasks(client)
timeclock = Timeclock(client)
mastodon = Mastodon(client)
about_obj = About(client)

@tree.command(
    name="announce",
    description="Send an announcement to the announcements channel."
)
async def announce(interaction: Interaction, message: str):
    await announcement.announce(interaction, message)

@tree.command(
    description="File a employee form.",
    name = "file"
)
async def file(interaction: Interaction, form: FormItems):
    await formClass.file(interaction, form)


@tree.command(
    name="leaderboard",
    description="Shows this month's leaderboard"
)
async def leaderboard(interaction: Interaction):
    await leaderboard.leaderboard(interaction)

@tree.command(
    name="task",
    description="Creates a task"
)
async def task(interaction: Interaction, name: str, assigned: Member, description: str = "", priority: TaskPriorities = "🟩", rate: str = "0"):
    await task_object.task(interaction, name, assigned, description, priority, rate)

@tree.command(
    name="resolve",
    description="Resolves this task."
)
async def resolve(interaction: Interaction, message: str = "No resolve message provided."):
    await task_object.resolve(interaction, message)

@tree.command(
    name="clock",
    description="Get, Set, or Remove details from your timesheet."
)
async def clock(interaction: Interaction, action: TimeclockTasks, target: Member = None, hours: int = 0):
    await timeclock.clock(interaction, action, target, hours)

@tree.command(
    name="about",
    description="Get information about your company."
)
async def about(interaction: Interaction, req_type: AboutOptions = "company"):
    await about_obj.entry(interaction, req_type)

@client.event
async def on_message(message: Message):
    if message.author.bot:
        return

    leaderboard_sql = get_sql("update_leaderboard")

    cur.execute(leaderboard_sql, (message.author.id,))
    con.commit()


@client.event
async def on_ready():
    print(f'{client.user.name} is now active.')
    await tree.sync()
    mastodon.check_mastodon.start()

client.run(getenv("token"))