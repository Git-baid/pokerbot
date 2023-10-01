import discord
from discord.ext import commands
from discord.ui import Button, View

from DiscordBotToken import BotToken

intents = discord.Intents().all()
intents.message_content = True
intents.members = True

yes_list = []
no_list = []
maybe_list = []

interaction_list = []

thumbnail = "https://cdn.discordapp.com/attachments/1072108039844397078/1157887619401777183/8336952.png?ex=651a3e60&is=6518ece0&hm=c7e1e31808d080e3d1b70539d828aef5e6c9f7a0946fec51c6444802ce807970&"
# test channel
#poker_channel = 1072251242740461648
# active channel
poker_channel = 1145254696601272401
guild_id = 1072108038577725551


async def disable_prev_buttons():
    with open('prev_message.txt', 'r') as inp:
        message_id = int(inp.read())

    message = await client.get_channel(poker_channel).fetch_message(int(message_id))

    view = discord.ui.View.from_message(message)
    view.clear_items()
    view.add_item(
        Button(label='Yes', style=discord.ButtonStyle.green, custom_id='1', emoji='\U00002705', disabled=True))
    view.add_item(Button(label='No', style=discord.ButtonStyle.red, custom_id='2', emoji='\U0000274E', disabled=True))
    view.add_item(
        Button(label='Maybe', style=discord.ButtonStyle.grey, custom_id='3', emoji='\U00002753', disabled=True))
    await message.edit(view=view)


async def create_fields(embed):
    yes_str = ""
    no_str = ""
    maybe_str = ""

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


class PersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Yes', style=discord.ButtonStyle.green, custom_id='1', emoji='\U00002705')
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        button_presser = interaction.user.display_name

        for i in no_list:
            if i == button_presser:
                no_list.remove(i)
        for i in maybe_list:
            if i == button_presser:
                maybe_list.remove(i)

        if button_presser not in yes_list:
            yes_list.append(button_presser)

        await create_fields(interaction.message.embeds[0])
        await interaction.response.edit_message(embed=interaction.message.embeds[0])

    @discord.ui.button(label='No', style=discord.ButtonStyle.red, custom_id='2', emoji='\U0000274E')
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        button_presser = interaction.user.display_name

        for i in yes_list:
            if i == button_presser:
                yes_list.remove(i)
        for i in maybe_list:
            if i == button_presser:
                maybe_list.remove(i)

        if button_presser not in no_list:
            no_list.append(button_presser)

        await create_fields(interaction.message.embeds[0])
        await interaction.response.edit_message(embed=interaction.message.embeds[0])

    @discord.ui.button(label='Maybe', style=discord.ButtonStyle.grey, custom_id='3', emoji='\U00002753')
    async def maybe(self, interaction: discord.Interaction, button: discord.ui.Button):
        button_presser = interaction.user.display_name

        for i in yes_list:
            if i == button_presser:
                yes_list.remove(i)
        for i in no_list:
            if i == button_presser:
                no_list.remove(i)

        if button_presser not in maybe_list:
            maybe_list.append(button_presser)

        await create_fields(interaction.message.embeds[0])
        await interaction.response.edit_message(embed=interaction.message.embeds[0])


class PersistentViewBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('.'), intents=intents)

    async def setup_hook(self) -> None:
        self.add_view(view=PersistentView())


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


@client.tree.command(name="poker_create", description="Create a poker event")
async def poker(interaction: discord.Interaction, details: str):
    yes_list.clear()
    no_list.clear()
    maybe_list.clear()

    channel = interaction.guild.get_channel(poker_channel)

    details += "\n---------------------------------------"  # readability

    embed = discord.Embed(title="Poker Roll Call", color=discord.Color.red(), description=details)
    embed.set_thumbnail(url=thumbnail)

    try:
        await disable_prev_buttons()
    except:
        pass

    await create_fields(embed)
    await interaction.response.send_message(embed=embed, view=PersistentView())

    with open('prev_message.txt', 'w') as outp:
        outp.write(str(channel.last_message_id))


@client.event
async def on_message(message):
    # if message is from baidbot, ignore all other if statements
    if message.author == client.user:
        return

    # convert message to all lowercase
    message.content = message.content.lower()


client.run(BotToken)
