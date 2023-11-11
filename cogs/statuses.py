import itertools
import discord
from discord.ext import commands, tasks


class Statuses(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.statuses = self.load_status()
        self.change_status.start()

    @staticmethod
    def load_status():
        with open("statuses.txt") as f:
            statuses = f.read().splitlines()

        return itertools.cycle(statuses)

    @tasks.loop(seconds=20)
    async def change_status(self):
        await self.bot.change_presence(activity=discord.Game(next(self.statuses)))


async def setup(bot):
    await bot.add_cog(Statuses(bot))
