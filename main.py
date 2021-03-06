import os
from dotenv import load_dotenv, find_dotenv
import discord
from discord.ext import commands

from cogs.check_in import CheckIn

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("Ready...")

# Si no necesitas la funcionalidad del check in, comenta o elimina
# la siguiente línea.
bot.add_cog(CheckIn(bot))

load_dotenv(find_dotenv())
DISCORD_KEY = os.environ.get("DISCORDKEY")

bot.run(DISCORD_KEY)
