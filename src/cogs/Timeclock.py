import datetime
import time
from enum import Enum
from os import getenv

from discord import Interaction, Embed, Forbidden, Member, Client, InteractionResponse, File

from psycopg import Connection, Cursor
from psycopg import connect as psycopg

import openpyxl
from openpyxl.styles import Alignment, Font

from src.lib import check_access, get_sql, log_content

tasks = [
    "in",
    "out",
    "weekly",
    "yearly",
    "unpaid",
    "pay",
    "add",
    "remove",
    "export"
]

TimeclockTasks = Enum("TimeclockTasks", {task.lower(): task for task in tasks})

def calculate_hours(results, tick: int = 0):
    totals = []
    for record in results:
        totals.append(record[tick])

    total = round(sum(totals), 2)
    avg = int(sum(totals) / len(totals))

    return total, avg


def instance_trim(haystack, needle):
    first_dash_index = haystack.find(needle)
    if first_dash_index != -1:
        return haystack[first_dash_index + 1:]
    else:
        return haystack


def format_for_table(sheet):
    for cell in sheet["A1:Z1"]:
        for cell in cell:
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal="center")

    dims = {}
    for row in sheet.rows:
        for cell in row:
            if cell.value:
                dims[cell.column_letter] = max((dims.get(cell.column_letter, 0), len(str(cell.value)))) + 2
    for col, value in dims.items():
        sheet.column_dimensions[str(col)].width = value


class Timeclock:
    def __init__(self, bot: Client):
        self.con: Connection = psycopg(getenv("connection_string"))
        self.cur: Cursor = self.con.cursor()
        self.clock_cache = {}
        self.bot = bot

    async def sql_wrapper(self, embed: Embed, interaction: Interaction, sql, params):
        response: InteractionResponse = interaction.response

        try:
            self.cur.execute(sql, params)
            self.con.commit()
        except Exception as e:
            print(e)

            embed.description = f"An error occurred while clocking in/out for {interaction.channel.name}."
            embed.set_footer(text="Please contact Primary Team Lead")

            await response.send_message(embed=embed, ephemeral=True)
            return

    async def clock_in(self, interaction: Interaction, response: InteractionResponse):
        if "t_" + str(interaction.user.id + interaction.channel.id) in self.clock_cache:
            await response.send_message("You are already clocked in", ephemeral=True)
            return

        self.clock_cache["t_" + str(interaction.user.id + interaction.channel.id)] = time.time()

        timeclock_in = get_sql("timeclock_in")

        embed = Embed(title="Clock In")

        await self.sql_wrapper(embed, interaction, timeclock_in,
                               (interaction.channel.name, interaction.user.nick, interaction.user.id))

        embed.description = f"{interaction.user.nick} has clocked in for {interaction.channel.name}."
        embed.set_footer(text="If this was a mistake, contact your team leader.")

        await response.send_message(embed=embed, ephemeral=True)

    async def clock_out(self, interaction: Interaction, response: InteractionResponse):
        if "t_" + str(interaction.user.id + interaction.channel.id) not in self.clock_cache:
            await response.send_message("You have not clocked in.", ephemeral=True)
            return

        clocked_in = self.clock_cache["t_" + str(interaction.user.id + interaction.channel.id)]
        clocked_out = time.time()
        time_worked = int(clocked_out - clocked_in)/60

        del self.clock_cache["t_" + str(interaction.user.id + interaction.channel.id)]

        timeclock_out = get_sql("timeclock_out")
        embed = Embed(title="Clock Out")

        await self.sql_wrapper(embed, interaction, timeclock_out,
                               (interaction.channel.name, interaction.user.nick, interaction.user.id, time_worked/60))

        embed.description = f"{interaction.user.nick} has clocked out for {interaction.channel.name}."
        embed.set_footer(text=f"Total time worked: {time_worked} minutes")

        await response.send_message(embed=embed, ephemeral=True)

    async def get_yearly(self, interaction: Interaction, response: InteractionResponse, target: Member = None):
        if target.id != interaction.user.id:
            if not await check_access(interaction):
                await response.send_message("You do not have permission to use this command.", ephemeral=True)
                return

        yearly = get_sql("timeclock_yearly")
        self.cur.execute(yearly, (target.id,))
        results = self.cur.fetchall()

        if len(results) == 0:
            await response.send_message("No timesheet found for this year.", ephemeral=True)
            return

        yearly, avg = calculate_hours(results, 0)
        cash, _ = calculate_hours(results, 1)

        embed = Embed(title="Timesheet")
        embed.description = f"Total Hours Worked: {yearly} hours"
        embed.description += f"\nAverage Hours Worked: {avg} hours"
        embed.description += f"\nTotal Paid: ${cash}"
        embed.set_footer(text="Hours are for this tax year only. For more information, contact your team leader.")

        await response.send_message(embed=embed, ephemeral=True)

    async def get_weekly(self, interaction: Interaction, response: InteractionResponse, target: Member = None):
        if target.id != interaction.user.id:
            if not await check_access(interaction):
                await response.send_message("You do not have permission to use this command.", ephemeral=True)
                return

        weekly = get_sql("timeclock_weekly")
        self.cur.execute(weekly, (target.id,))
        results = self.cur.fetchall()

        if len(results) == 0:
            await response.send_message("No timesheet found for this week.", ephemeral=True)
            return

        print(results)

        weekly, avg = calculate_hours(results, 1)
        cash, _ = calculate_hours(results, 0)

        embed = Embed(title="Timesheet")
        embed.description = f"Total Hours Worked: {weekly} hours"
        embed.description += f"\nAverage Hours Worked: {avg} hours"
        embed.description += f"\nTotal Paid: ${cash}"
        embed.set_footer(text="Hours are for this week only. For more information, contact your team leader.")

        await response.send_message(embed=embed, ephemeral=True)

    async def get_unpaid(self, interaction: Interaction, response: InteractionResponse, target: Member):
        if target.id != interaction.user.id:
            if not await check_access(interaction):
                await response.send_message("You do not have permission to use this command.", ephemeral=True)
                return

        unpaid_sql = get_sql("timeclock_unpaid")

        self.cur.execute(unpaid_sql, (target.id,))
        results = self.cur.fetchall()
        total, avg = calculate_hours(results)

        embed = Embed(title="Timesheet")
        embed.description = f"Total Hours Worked: {total} hours"
        embed.description += f"\nAverage Hours Worked: {avg} hours"
        embed.set_footer(text="Hours are for all unpaid hours. For more information, contact your team leader.")

        await response.send_message(embed=embed, ephemeral=True)

    async def pay(self, interaction: Interaction, response: InteractionResponse, target: Member, hours: int = 0, amount: int = 0):
        if not await check_access(interaction):
            await response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        if hours == 0:
            unpaid_sql = get_sql("timeclock_unpaid")
            self.cur.execute(unpaid_sql, (target.id,))
            results = self.cur.fetchall()
            hours, _ = calculate_hours(results)

        pay_sql = get_sql("timeclock_pay")
        self.cur.execute(pay_sql, (target.id, target.nick, -hours, amount))
        self.con.commit()



        embed = Embed(title="Payment")
        embed.description = f"A payment for {hours} hours has been credited to your account. Expect payment shortly."
        embed.set_footer(text="For more information, contact your team leader.")

        try:
            await target.create_dm()
            await target.dm_channel.send(embed=embed)
        except Forbidden:
            await response.send_message("User has DMs disabled. Unable to send payment notice. Payment has been documented.", ephemeral=True)
            return

    async def add(self, interaction: Interaction, response: InteractionResponse, target: Member, hours: int):
        if not await check_access(interaction):
            await response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        await log_content(interaction, f"{interaction.user.nick} added {hours} hours from {target.nick}'s timesheet.")

        embed = Embed(title="Time Added")
        correct_sql = get_sql("timeclock_correct")

        await self.sql_wrapper(embed, interaction, correct_sql,
                               (interaction.channel.name, target.nick, target.id, hours))

        embed.description = f"{hours} hours have been added to {target.nick}'s timesheet."
        await response.send_message(embed=embed)

    async def remove(self, interaction: Interaction, response: InteractionResponse, target: Member, hours: int):
        if not await check_access(interaction):
            await response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        await log_content(interaction, f"{interaction.user.nick} removed {hours} hours from {target.nick}'s timesheet.")

        embed = Embed(title="Time Removed")
        correct_sql = get_sql("timeclock_correct")

        await self.sql_wrapper(embed, interaction, correct_sql,
                               (interaction.channel.name, target.nick, target.id, -hours))

        embed.description = f"{hours} hours have been removed from {target.nick}'s timesheet."
        await response.send_message(embed=embed)

    async def export(self, interaction: Interaction, response: InteractionResponse, target: Member):
        if target.id != interaction.user.id:
            if not await check_access(interaction):
                await response.send_message("You do not have permission to use this command.", ephemeral=True)
                return

        wb = openpyxl.Workbook()


        ### Timesheet Table ###
        wb.worksheets[0].title = "Timesheet"
        ws = wb.active

        hours_sql = get_sql("timeclock_all_hours")
        self.cur.execute(hours_sql, (target.id,))
        results = self.cur.fetchall()

        ws.append(["Task", "Type", "Hours", "Hours Total", "Paid", "Timestamp"])

        total = 0
        for record in results:
            total += record[2]
            if record[0] != "Payment Issued":
                ws.append([instance_trim(instance_trim(record[0], " "), "-"), record[1], total, record[2], record[3], str(record[4]).strip()])

        format_for_table(ws)

        ### Salaries Table ###
        wb.create_sheet("Salaries")
        ws = wb["Salaries"]

        pay_sql = get_sql("timeclock_all_paid")
        self.cur.execute(pay_sql, (target.id,))
        results = self.cur.fetchall()

        ws.append(["Amount", "Hours Paid", "Timestamp"])

        for record in results:
            ws.append([record[0], record[1], record[2]])

        format_for_table(ws)

        ## Save ##
        name = "workbooks/" + interaction.user.nick.replace("\"", "") +  ".xlsx"
        wb.save(name)
        await response.send_message(file=File(name), ephemeral=True)

    async def clock(self, interaction: Interaction, action: TimeclockTasks = TimeclockTasks["weekly"], target: Member = None, hours: int = 0, amount: int = 0):
        user_target = target
        if not target:
            user_target = interaction.user

        response: InteractionResponse = interaction.response

        if action == TimeclockTasks["in"]:
            await self.clock_in(interaction, response)
        elif action == TimeclockTasks["out"]:
            await self.clock_out(interaction, response)
        elif action == TimeclockTasks["weekly"]:
            await self.get_weekly(interaction, response, user_target)
        elif action == TimeclockTasks["yearly"]:
            await self.get_yearly(interaction, response, user_target)
        elif action == TimeclockTasks["unpaid"]:
            await self.get_unpaid(interaction, response, user_target)
        elif action == TimeclockTasks["pay"]:
            await self.pay(interaction, response, user_target, hours, amount)
        elif action == TimeclockTasks["add"]:
            await self.add(interaction, response, user_target, hours)
        elif action == TimeclockTasks["remove"]:
            await self.remove(interaction, response, user_target, hours)
        elif action == TimeclockTasks["export"]:
            await self.export(interaction, response, user_target)
        else:
            await self.get_weekly(interaction, response, user_target)
