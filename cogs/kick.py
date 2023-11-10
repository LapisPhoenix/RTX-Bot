import discord
from discord.ext import commands


class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, reason: str = "No Reason Provided."):
        await member.kick(reason=reason)
        embed = discord.Embed(title="Kick", description=f"Kicked {member.mention}", color=discord.Color.green())
        embed.add_field(name="Moderator", value=ctx.author.mention)
        embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Kick(bot))
