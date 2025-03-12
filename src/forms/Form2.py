from discord.ui import TextInput
from discord import TextStyle

from src.forms.FormTemplate import FormTemplate


class Form2(FormTemplate, title='Form 2 - Damaged Equipment'):
    form_name = "Form 2 - Damaged Equipment"

    item_type = TextInput(
        label='What was the item type?',
        required=True,
        style=TextStyle.short,
        placeholder='(e.g. "Laptop", "Tablet")',
        max_length=10
    )

    brand_model = TextInput(
        label="What was the brand and model of the device?",
        required=True,
        style=TextStyle.short,
        placeholder='Lenovo ThinkPad, iPad Pro, etc.',
        max_length=100
    )

    damaged_how = TextInput(
        label="How was this item damaged?",
        required=True,
        style=TextStyle.long,
        placeholder='Reason for payment',
        max_length=2000
    )