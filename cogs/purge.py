import discord
from discord.ext import commands


class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        embed = discord.Embed(title="Purge", description=f"Purged {amount} messages", color=discord.Color.green())
        embed.add_field(name="Moderator", value=ctx.author.mention)
        await ctx.send(embed=embed, delete_after=5)


async def setup(bot):
    await bot.add_cog(Purge(bot))
