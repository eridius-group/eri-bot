from discord.ui import TextInput
from discord import TextStyle
from src.forms.FormTemplate import FormTemplate


class Form3(FormTemplate, title='Form 3 - Contractor Reimbursement'):
    form_name = "Form 3 - Contractor Reimbursement"

    amount = TextInput(
        label='What was the amount, in US dollars?',
        required=True,
        style=TextStyle.short,
        placeholder='US$0.00',
        max_length=6
    )

    reason = TextInput(
        label="What was this money spent on?",
        required=True,
        style=TextStyle.long,
        placeholder='Reason for payment',
        max_length=2000
    )