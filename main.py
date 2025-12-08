import discord
from discord.ext import commands
from discord.ui import Button, View

from DiscordBotToken import BotToken

import json

intents = discord.Intents().all()
intents.message_content = True
intents.members = True

poker_thumbnail = "https://cdn.discordapp.com/attachments/1072108039844397078/1157887619401777183/8336952.png?ex=651a3e60&is=6518ece0&hm=c7e1e31808d080e3d1b70539d828aef5e6c9f7a0946fec51c6444802ce807970&"
potluck_thumbnail = "https://cdn.discordapp.com/attachments/434752033552203793/1442369438832922745/image.png?ex=69252eb8&is=6923dd38&hm=ce942c34170a8c74681ee4a5d5dd1a7c9c7ef8c3041828a730aeb28d577dd212&"

poker_data_file = "/home/baid/Desktop/DiscordBots/pokerbotDiscord/pokerbot/poker_data.json"
potluck_data_file = "/home/baid/Desktop/DiscordBots/pokerbotDiscord/pokerbot/potluck_data.json"

async def disable_prev_buttons(roll_call_type):
    message_id = None
    channel_id = None
    if roll_call_type == "poker":
        with open('prev_poker_message.txt', 'r') as inp:
            fin = json.load(inp)
            channel_id = int(fin["channel_id"])
            message_id = int(fin["message_id"])
    if roll_call_type == "potluck":
        with open('prev_potluck_message.txt', 'r') as inp:
            fin = json.load(inp)
            channel_id = int(fin["channel_id"])
            message_id = int(fin["message_id"])
    message = await client.get_channel(channel_id).fetch_message(message_id)
    print(message)
    view = discord.ui.View.from_message(message)
    view.clear_items()
    view.add_item(Button(label='Yes', style=discord.ButtonStyle.green, custom_id=f"{roll_call_type}_yes", emoji='\U00002705', disabled=True))
    view.add_item(Button(label='No', style=discord.ButtonStyle.red, custom_id=f"{roll_call_type}_no", emoji='\U0000274E', disabled=True))
    view.add_item(Button(label='Maybe', style=discord.ButtonStyle.grey, custom_id=f"{roll_call_type}_maybe", emoji='\U00002753', disabled=True))
    await message.edit(view=view)

async def add_to_list(target_user_name, target_list_name, roll_call_type):
    data = {}
    if roll_call_type == "poker":
        with open(poker_data_file, 'r') as f:
            data = json.load(f)
    if roll_call_type == "potluck":
        with open(potluck_data_file, 'r') as f:
            data = json.load(f)

    if target_user_name not in data[target_list_name]:
        data[target_list_name].append(target_user_name)

        for list, names in data.items():
            if target_user_name in names and list != target_list_name:
                data[list].remove(target_user_name)
    else:
        data[target_list_name].remove(target_user_name)
    
    if roll_call_type == "poker":
        with open(poker_data_file, 'w') as f:
            json.dump(data, f, indent=4)
    if roll_call_type == "potluck":
        with open(potluck_data_file, 'w') as f:
            json.dump(data, f, indent=4)

async def create_fields(embed, roll_call_type):
    yes_str = ""
    no_str = ""
    maybe_str = ""
    data = {}

    if roll_call_type == "poker":
        with open(poker_data_file, 'r') as f:
            data = json.load(f)
    if roll_call_type == "potluck":
        with open(potluck_data_file, 'r') as f:
            data = json.load(f)

    yes_list = data["yes_list"]
    no_list = data["no_list"]
    maybe_list = data["maybe_list"]
    
    for i in yes_list:
        yes_str += i + "\n"
    for i in no_list:
        no_str += i + "\n"
    for i in maybe_list:
        maybe_str += i + "\n"

    embed.clear_fields()
    embed.add_field(name=f"\U00002705 Yes ({len(yes_list)})",
                    value=f"{yes_str}"
                    , inline=True)
    embed.add_field(name=f"\U0000274C No ({len(no_list)})",
                    value=f"{no_str}"
                    , inline=True)
    embed.add_field(name=f"\U00002753 Maybe ({len(maybe_list)})",
                    value=f"{maybe_str}"
                    , inline=True)


class PokerView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # poker buttons
    @discord.ui.button(label='Yes', style=discord.ButtonStyle.green, custom_id='poker_yes', emoji='\U00002705')
    async def poker_yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        await add_to_list(interaction.user.display_name, "yes_list", "poker")
        await create_fields(interaction.message.embeds[0], "poker")
        await interaction.response.edit_message(embed=interaction.message.embeds[0])

    @discord.ui.button(label='No', style=discord.ButtonStyle.red, custom_id='poker_no', emoji='\U0000274E')
    async def poker_no(self, interaction: discord.Interaction, button: discord.ui.Button):
        await add_to_list(interaction.user.display_name, "no_list", "poker")

        await create_fields(interaction.message.embeds[0], "poker")
        await interaction.response.edit_message(embed=interaction.message.embeds[0])

    @discord.ui.button(label='Maybe', style=discord.ButtonStyle.grey, custom_id='poker_maybe', emoji='\U00002753')
    async def poker_maybe(self, interaction: discord.Interaction, button: discord.ui.Button):
        await add_to_list(interaction.user.display_name, "maybe_list", "poker")

        await create_fields(interaction.message.embeds[0], "poker")
        await interaction.response.edit_message(embed=interaction.message.embeds[0])


class PotluckView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # potluck buttons
    @discord.ui.button(label='Yes', style=discord.ButtonStyle.green, custom_id='potluck_yes', emoji='\U00002705')
    async def potluck_yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        await add_to_list(interaction.user.display_name, "yes_list", "potluck")

        await create_fields(interaction.message.embeds[0], "potluck")
        await interaction.response.edit_message(embed=interaction.message.embeds[0])

    @discord.ui.button(label='No', style=discord.ButtonStyle.red, custom_id='potluck_no', emoji='\U0000274E')
    async def potluck_no(self, interaction: discord.Interaction, button: discord.ui.Button):
        await add_to_list(interaction.user.display_name, "no_list", "potluck")

        await create_fields(interaction.message.embeds[0], "potluck")
        await interaction.response.edit_message(embed=interaction.message.embeds[0])

    @discord.ui.button(label='Maybe', style=discord.ButtonStyle.grey, custom_id='potluck_maybe', emoji='\U00002753')
    async def potluck_maybe(self, interaction: discord.Interaction, button: discord.ui.Button):
        await add_to_list(interaction.user.display_name, "maybe_list", "potluck")

        await create_fields(interaction.message.embeds[0], "potluck")
        await interaction.response.edit_message(embed=interaction.message.embeds[0])
    


class PersistentViewBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('.'), intents=intents)

    async def setup_hook(self) -> None:
        self.add_view(view=PokerView())
        self.add_view(view=PotluckView())


client = PersistentViewBot()


@client.event
async def on_ready():
    await client.tree.sync()
    print(f"Ready to use as {client.user}.")


# Ping command
@client.tree.command(name="ping", description="return bot latency")
async def ping(interaction: discord.Interaction):
    bot_latency = round(client.latency * 1000)
    await interaction.response.send_message(f"Response time: {bot_latency}ms.")

# Create poker roll call
@client.tree.command(name="poker_create", description="Create a poker event")
async def poker(interaction: discord.Interaction, details: str):
    channel = interaction.channel

    details += "\n--------------------"  # readability

    embed = discord.Embed(title="Poker Roll Call", color=discord.Color.red(), description=details)
    embed.set_thumbnail(url=poker_thumbnail)

    await disable_prev_buttons("poker")
    
    with open(poker_data_file, 'w') as f:
        # set all dictionaries in file to empty
        json.dump({"yes_list": [], "no_list": [], "maybe_list": []}, f)
        
    await create_fields(embed, "poker")
    await interaction.response.send_message(content="@everyone", embed=embed, view=PokerView(), allowed_mentions=discord.AllowedMentions(everyone=True))

    with open('prev_poker_message.txt', 'w') as outp:
        json.dump({"channel_id": channel.id, "message_id": channel.last_message_id}, outp)

# Create potluck roll call
@client.tree.command(name="potluck_create", description="Create a potluck event")
async def potluck(interaction: discord.Interaction, details: str):
    channel = interaction.channel

    details += "\n--------------------"  # readability

    embed = discord.Embed(title="Potluck Roll Call", color=discord.Color.blue(), description=details)
    embed.set_thumbnail(url=potluck_thumbnail)

    try:
        await disable_prev_buttons("potluck")
    except:
        pass
    
    with open(potluck_data_file, 'w') as f:
        # set all dictionaries in file to empty
        json.dump({"yes_list": [], "no_list": [], "maybe_list": []}, f)
        
    await create_fields(embed, "potluck")
    await interaction.response.send_message(content="@everyone", embed=embed, view=PotluckView(), allowed_mentions=discord.AllowedMentions(everyone=True))

    with open('prev_potluck_message.txt', 'w') as outp:
        json.dump({"channel_id": channel.id, "message_id": channel.last_message_id}, outp)

@client.event
async def on_message(message):
    # if message is from pokerbot, ignore all other if statements
    if message.author == client.user:
        return

    # convert message to all lowercase
    # message.content = message.content.lower()


client.run(BotToken)
