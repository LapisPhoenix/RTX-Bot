import re
import asyncio
import datetime
import discord
from discord.ext import commands


class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx: commands.Context, member: discord.Member, time: str, reason: str):
        embed = discord.Embed(title="Mute", description=f"Muted {member.mention}", color=discord.Color.green())
        pattern = re.compile(r"[0-9]+d[0-9]+h[0-9]+m[0-9]+s", re.IGNORECASE)
        if pattern.match(time) is None:
            embed = discord.Embed(title="Mute", description="Invalid time format. Please use this format: `1d1h1m1s`",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        time = time.lower()
        days = int(time.split("d")[0])
        hours = int(time.split("d")[1].split("h")[0])
        minutes = int(time.split("h")[1].split("m")[0])
        seconds = int(time.split("m")[1].split("s")[0])

        time_delta = datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        embed.add_field(name="Time", value=time)
        embed.add_field(name="Reason", value=reason)
        embed.add_field(name="Moderator", value=ctx.author.mention)
        await ctx.send(embed=embed)

        await member.timeout(time_delta, reason=reason)
        await asyncio.sleep(time_delta.total_seconds())

        if member.is_timed_out():
            embed = discord.Embed(title="Unmute", description=f"Unmuted {member.mention}", color=discord.Color.green())
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx: commands.Context, member: discord.Member):
        if member.is_timed_out():
            await member.timeout(None, reason="Unmuted")
            embed = discord.Embed(title="Unmute", description=f"Unmuted {member.mention}", color=discord.Color.green())
            embed.add_field(name="Moderator", value=ctx.author.mention)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Unmute", description=f"{member.mention} is not muted",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Mute(bot))
