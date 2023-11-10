import discord
from discord.ext import commands


class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, reason: str = "No Reason Provided."):
        await member.ban(reason=reason)
        embed = discord.Embed(title="Ban", description=f"Banned {member.mention}", color=discord.Color.green())
        embed.add_field(name="Moderator", value=ctx.author.mention)
        embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx: commands.Context, member: discord.Member):
        await member.unban(reason="Unbanned")
        embed = discord.Embed(title="Unban", description=f"Unbanned {member.mention}", color=discord.Color.green())
        embed.add_field(name="Moderator", value=ctx.author.mention)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Ban(bot))
