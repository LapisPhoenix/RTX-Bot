import os
import logging
import discord
import aiosqlite
from discord.ext import commands
from dotenv import load_dotenv


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot.remove_command('help')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(console)


async def setup_database():
    async with aiosqlite.connect("main.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users"
                         " (id INTEGER PRIMARY KEY, warnings INT, xp INT, level INT)")
        await db.commit()


async def load_cogs():
    for file in os.listdir("cogs"):
        if file.startswith("IGNORE_"):
            continue

        if not file.endswith(".py"):
            continue

        await bot.load_extension(f"cogs.{file[:-3]}")
        print(f"Loaded: cogs.{file[:-3]}")


@bot.event
async def on_ready():
    await setup_database()
    await load_cogs()
    print("Bot is ready")
    print(f"Bot latency: {round(bot.latency * 1000)}ms")
    print(f"Bot name: {bot.user.name}")
    print(f"Bot ID: {bot.user.id}")


if __name__ == '__main__':
    load_dotenv()
    bot.run(os.getenv("TOKEN"))
