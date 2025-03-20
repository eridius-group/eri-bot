Eri is a software program developed by Eridius Group LLC and is available under an MIT license. Eri is designed to aid in managing day-to-day tasks at Eridius, including task management and time management. Due to its all-encompassing nature, Eri may be a little daunting to use at first, but this guide should help explain what Eri is and how to use it.

For starters, you may want to know what Eri is. Thankfully, there is a Discord command for that. Log onto the Discord server you use for work and type `/about`. This command will show you information about the organization you work for. This may not be helpful if you want to know what Eri is, so you should run the command `/about eri` to get an about summary for Eri itself. 

The summary likely reads as follows:

“Eri is a utility for Discord to help manage employees, tasks, and more. Eri is source-available software, so you can have peace of mind that your data is handled properly.”

Next up - you probably want to create some tasks! Anyone can create tasks, including you. You can create a task in any Discord channel by typing the command `/task [task name] [assigned to]`. This will open a thread in the Forums channel configured in Eri. Whoever you chose to assign the task to will receive a notification within Discord, and they’ll see the thread. Of course, you may want to provide more information, like a task description or how much they can expect to be paid. The full command, including optional parameters, is listed below:

`/task [task name] [assigned to] [description] [priority] [rate]`

In this command, you can add an optional description for the task. Since you cannot add line breaks in commands on Discord, simply type `\n` wherever you want to add a line break (newline). The priority can be Low, Medium, High, or Critical. The rate can be left empty if pay is not yet determined, or you can specify NA or any other non-numerical value to fill as not applicable. When specifying the rate, do not add the currency symbol - Eri will do that for you.

When a task is completed, you can run `/resolve [message]` to close the thread, archive it, and mark it as completed. Employees won’t be able to use that thread to clock in or out anymore, but they can still clock in or out in other channels on Discord.

Now that you have some tasks, you can clock in! Running `/clock in` will have Eri start tracking your time. When you’re done, simply type `/clock out`. Where you run this command is important, since Eri logs the channel’s name in your payment exports (which we explain a bit later). Eri logs this in its database and can ensure you are paid for your time. 

To see how much you have worked this week, type `/clock weekly`, or to see how much you have worked this year, type `/clock yearly`. The yearly command does not go back 365 days - instead, it breaks off January 31st of the current tax year, to comply with the United States tax system. 

In addition to your hours worked, Eri also tracks how much you’ve been paid. This also shows in the weekly and yearly summaries. If you want more information for how much you’ve worked, you can run the command `/clock export`, which will export your hours, payments, corrections, and all other information Eri has collected, into an Excel workbook. Excel workbooks can be imported into Google Drive and viewed in Sheets if you do not have Microsoft Office. This export command shows all the data and is not limited to one particular year or week. 

If you are paid on a non-continious schedule, you can see what hours you’ve worked since you’ve last been paid, which is done via `/clock unpaid`.

Eri also has some administrative commands for time-keeping. You can mark hours as paid using the `/clock pay` command. This command also accepts an integer of hours to mark as paid, and a dollar amount the employee has been paid. The full command looks like `/clock pay [user] [hours] [amount]`. 

Further, Eri allows you to submit time corrections. This is done via `/clock add [user]` and `/clock remove [user]`. All clock commands except `/clock in` and `/clock out` support a `[user]` parameter for administrative purposes. This means you are able to export an employee’s hours, check their weekly/yearly summaries, and add/remove hours.

Lastly, Eri has commands for making announcements in the server for work. This is an administrative command, and will send an embed message in the announcements channel. The command is `/announce [message]`, and like the `/task` command, you can add `\n` to add line breaks (newlines). 

That’s pretty much it! Eri is a large program, but it is very useful for administrative and management tasks. Hopefully it isn’t too daunting! 
