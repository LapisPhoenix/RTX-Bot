import aiosqlite
import discord
from discord.ext import commands


class Rank(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command()
    async def rank(self, ctx: commands.Context, member: discord.Member | None = None):
        if member is None:
            member = ctx.author

        async with aiosqlite.connect("main.db") as db:
            async with db.execute("SELECT * FROM users WHERE id = ?", (member.id,)) as cursor:
                row = await cursor.fetchone()
                if row is None:
                    await ctx.send("This user has not sent any messages yet")
                    return

                xp = row[2]
                level = row[3]
                embed = discord.Embed(title=f"{member.name}'s rank", color=discord.Color.green())
                embed.add_field(name="Level", value=level)
                embed.add_field(name="XP", value=xp)
                await ctx.send(embed=embed)

    @commands.command()
    async def leaderboard(self, ctx: commands.Context):
        embed = discord.Embed(title="Leaderboard", color=discord.Color.green())
        async with aiosqlite.connect("main.db") as db:
            async with db.execute("SELECT id, level, xp FROM users ORDER BY level DESC, xp DESC") as curs:
                rows = await curs.fetchmany(10)
                for i, row in enumerate(rows):
                    member = ctx.guild.get_member(row[0])
                    embed.add_field(name=f"{i + 1}. {member.name}", value=f"Level: {row[1]} | XP: {row[2]}")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Rank(bot))