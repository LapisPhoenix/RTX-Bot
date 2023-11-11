import discord
from discord.ext import commands


class Lock(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(aliases=["lockdown", "ld", "lockchannel"])
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx: commands.Context):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        embed = discord.Embed(title="Lockdown", description=f"Locked {ctx.channel.mention}",
                              color=discord.Color.green())
        embed.add_field(name="Moderator", value=ctx.author.mention)
        await ctx.send(embed=embed)

    @commands.command(aliases=["unlockchannel", "ul", "unlockdown"])
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx: commands.Context):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        embed = discord.Embed(title="Unlockdown", description=f"Unlocked {ctx.channel.mention}",
                              color=discord.Color.green())
        embed.add_field(name="Moderator", value=ctx.author.mention)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Lock(bot))
