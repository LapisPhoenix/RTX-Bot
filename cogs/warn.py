import aiosqlite
import discord
from discord.ext import commands


class Warn(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(aliases=["w"])
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx: commands.Context, member: discord.Member, reason: str = "No Reason Provided."):
        async with aiosqlite.connect("main.db") as db:
            async with db.execute("SELECT warnings FROM users WHERE id = ?", (member.id,)) as cursor:
                warnings = await cursor.fetchone()
                if warnings is None:
                    warnings = 0
                else:
                    warnings = warnings[0]
                await db.execute("UPDATE users SET warnings = ? WHERE id = ?", (warnings + 1, member.id))
                await db.commit()

        embed = discord.Embed(title="Warn", description=f"Warned {member.mention}", color=discord.Color.green())
        embed.add_field(name="Moderator", value=ctx.author.mention)
        embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=embed)

    @commands.command(aliases=["warns"])
    @commands.has_permissions(kick_members=True)
    async def warnings(self, ctx: commands.Context, member: discord.Member):
        async with aiosqlite.connect("main.db") as db:
            async with db.execute("SELECT warnings FROM users WHERE id = ?", (member.id,)) as cursor:
                warnings = await cursor.fetchone()
                if warnings is None:
                    warnings = 0
                else:
                    warnings = warnings[0]

        embed = discord.Embed(title="Warnings", description=f"{member.mention} has {warnings} warnings",
                              color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(aliases=["rw"])
    @commands.has_permissions(kick_members=True)
    async def removewarn(self, ctx: commands.Context, member: discord.Member, amount: int):
        async with aiosqlite.connect("main.db") as db:
            async with db.execute("SELECT warnings FROM users WHERE id = ?", (member.id,)) as cursor:
                warnings = await cursor.fetchone()
                if warnings is None:
                    warnings = 0
                else:
                    warnings = warnings[0]
                await db.execute("UPDATE users SET warnings = ? WHERE id = ?", (warnings - amount, member.id))
                await db.commit()

        embed = discord.Embed(title="Remove Warn", description=f"Removed {amount} warnings from {member.mention}",
                              color=discord.Color.green())
        embed.add_field(name="Moderator", value=ctx.author.mention)
        await ctx.send(embed=embed)

    @commands.command(aliases=["cw"])
    @commands.has_permissions(kick_members=True)
    async def clearwarns(self, ctx: commands.Context, member: discord.Member):
        async with aiosqlite.connect("main.db") as db:
            await db.execute("UPDATE users SET warnings = ? WHERE id = ?", (0, member.id))
            await db.commit()

        embed = discord.Embed(title="Clear Warns", description=f"Cleared all warnings from {member.mention}",
                              color=discord.Color.green())
        embed.add_field(name="Moderator", value=ctx.author.mention)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Warn(bot))
