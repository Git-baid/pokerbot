
import discord
from discord.ext import commands
from discord.ui import Button, View

from DiscordBotToken import BotToken

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix='pokerbot', intents=intents)

yes_list = []
no_list = []
maybe_list = []
pending_list = []

prev_list = []

test_poker_role = 1155664407561519114
poker_role = 1145254199945338881
guild_id = 1072108038577725551



@client.event
async def on_ready():
    await client.tree.sync()
    print(f"Ready to use as {client.user}.")


# Ping command
@client.tree.command(name="ping", description="return bot latency")
async def ping(interaction: discord.Interaction):
    bot_latency = round(client.latency * 1000)
    await interaction.response.send_message(f"Response time: {bot_latency}ms.")


@client.tree.command(name="poker_create", description="Create a poker event")
async def poker(interaction: discord.Interaction, details: str):

    yes_list.clear()
    no_list.clear()
    maybe_list.clear()
    pending_list.clear()

    for member in interaction.guild.get_role(poker_role).members:
        pending_list.append(member.display_name)

    embed_message = discord.Embed(title="Poker Roll Call", color=discord.Color.red(), description=details)

    async def create_fields():
        yes_str = ""
        no_str = ""
        maybe_str = ""
        pending_str = ""

        for i in yes_list:
            yes_str += i + "\n"
        for i in no_list:
            no_str += i + "\n"
        for i in maybe_list:
            maybe_str += i + "\n"
        for i in pending_list:
            pending_str += i + "\n"

        embed_message.clear_fields()
        embed_message.add_field(name=f"\U00002705 Yes ({len(yes_list)})",
                                value=f"{yes_str}"
                                , inline=True)
        embed_message.add_field(name=f"\U0000274C No ({len(no_list)})",
                                value=f"{no_str}"
                                , inline=True)
        embed_message.add_field(name=f"\U00002753 Maybe ({len(maybe_list)})",
                                value=f"{maybe_str}"
                                , inline=True)
        embed_message.add_field(name=f"Pending ({len(pending_list)})",
                                value=f"{pending_str}"
                                , inline=True)


    # Yes button --------------------------------------------------------
    yes_button = Button(label="Yes", style=discord.ButtonStyle.green, emoji='\U00002705')

    async def yes_callback(interaction):
        button_presser = interaction.user.display_name

        for i in no_list:
            if i == button_presser:
                no_list.remove(i)
        for i in maybe_list:
            if i == button_presser:
                maybe_list.remove(i)
        for i in pending_list:
            if i == button_presser:
                pending_list.remove(i)

        if button_presser not in yes_list:
            yes_list.append(button_presser)

        await create_fields()
        await interaction.response.edit_message(embed=embed_message)
    yes_button.callback = yes_callback

    # No button --------------------------------------------------------
    no_button = Button(label="No", style=discord.ButtonStyle.red, emoji='\U0000274E')

    async def no_callback(interaction):
        button_presser = interaction.user.display_name

        for i in yes_list:
            if i == button_presser:
                yes_list.remove(i)
        for i in maybe_list:
            if i == button_presser:
                maybe_list.remove(i)
        for i in pending_list:
            if i == button_presser:
                pending_list.remove(i)

        if button_presser not in no_list:
            no_list.append(button_presser)

        await create_fields()
        await interaction.response.edit_message(embed=embed_message)
    no_button.callback = no_callback

    # Maybe button --------------------------------------------------------
    maybe_button = Button(label="Maybe", style=discord.ButtonStyle.blurple, emoji='\U00002753')

    async def maybe_callback(interaction):
        button_presser = interaction.user.display_name

        for i in yes_list:
            if i == button_presser:
                yes_list.remove(i)
        for i in no_list:
            if i == button_presser:
                no_list.remove(i)
        for i in pending_list:
            if i == button_presser:
                pending_list.remove(i)

        if button_presser not in maybe_list:
            maybe_list.append(button_presser)

        await create_fields()
        await interaction.response.edit_message(embed=embed_message)
    maybe_button.callback = maybe_callback

    # embed message -------------------------------------------------------------------------------

    await create_fields()
    view = View()
    view.add_item(yes_button)
    view.add_item(no_button)
    view.add_item(maybe_button)

    if len(prev_list) != 0:
        yes_button.disabled = True
        no_button.disabled = True
        maybe_button.disabled = True
        await prev_list[0].edit_original_response(view=view)
    prev_list.insert(0, interaction)

    yes_button.disabled = False
    no_button.disabled = False
    maybe_button.disabled = False

    await prev_list[0].response.send_message(embed=embed_message, view=view)


@client.event
async def on_message(message):
    # if message is from baidbot, ignore all other if statements
    if message.author == client.user:
        return

    # convert message to all lowercase
    message.content = message.content.lower()

client.run(BotToken)