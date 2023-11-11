import random
import datetime
import time
import re
import asyncio
import discord
from discord.ext import commands


class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def giveaway(self, ctx: commands.Context, time_str: str, winners: int, *, prize: str):
        pattern = re.compile(r"[0-9]+d[0-9]+h[0-9]+m[0-9]+s", re.IGNORECASE)
        if pattern.match(time_str) is None:
            embed = discord.Embed(title="Mute", description="Invalid time format. Please use this format: `1d1h1m1s`",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        time_str = time_str.lower()
        days = int(time_str.split("d")[0])
        hours = int(time_str.split("d")[1].split("h")[0])
        minutes = int(time_str.split("h")[1].split("m")[0])
        seconds = int(time_str.split("m")[1].split("s")[0])
        time_delta = datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        time_epoch = round(time.time() + time_delta.total_seconds())
        embed = discord.Embed(title="Giveaway", description=f"React with 🎉 to enter!",
                              color=discord.Color.green())
        embed.add_field(name="Prize", value=prize)
        embed.add_field(name="Winners", value=winners)
        embed.add_field(name="Hosted by", value=ctx.author.mention)
        message = await ctx.send(embed=embed, content=f"Time left: <t:{time_epoch}:R>")
        await message.add_reaction("🎉")
        await asyncio.sleep(time_delta.total_seconds())
        message = await ctx.fetch_message(message.id)
        users = message.reactions[0].users()
        winners_list = []

        async for user in users:
            if user.bot:
                continue

            if random.randint(0, 1) == 0:
                winners_list.append(user)

            if len(winners_list) == winners:
                break

        if len(winners_list) == 0:
            embed = discord.Embed(title="Giveaway", description="No one entered the giveaway",
                                  color=discord.Color.red())
            await message.channel.send(embed=embed)
            return

        embed = discord.Embed(title="Giveaway", description="You won a giveaway!", color=discord.Color.green())
        embed.add_field(name="Prize", value=prize)
        for winner in winners_list:
            embed.add_field(name="Winner", value=winner.mention, inline=False)

        await message.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Giveaway(bot))
