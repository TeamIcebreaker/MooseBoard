from discord.ext import commands
import json, logging
from utils.utils import BOT_TOKEN

from discord import Intents
# intents = Intents(presences=True, members=True, messages=True, guilds=True)

bot = commands.Bot(command_prefix=commands.when_mentioned_or(">"))
bot.remove_command('help')

extensions = ["cogs.team", "cogs.fun"]

for ext in extensions:
    bot.load_extension(ext)

bot.run(BOT_TOKEN)
