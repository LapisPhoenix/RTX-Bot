import itertools
import discord
from discord.ext import commands, tasks


class Statuses(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.change_status.start()

    @staticmethod
    def load_status():
        with open("statuses.txt") as f:
            statuses = f.read().splitlines()

        while True:
            for status in itertools.cycle(statuses):
                yield status

    @tasks.loop(seconds=20)
    async def change_status(self):
        await self.bot.change_presence(activity=discord.Game(next(self.load_status())))


async def setup(bot):
    await bot.add_cog(Statuses(bot))
