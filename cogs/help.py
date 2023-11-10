import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.group(invoke_without_command=True)
    async def help(self, ctx: commands.Context):
        embed = discord.Embed(title="Help", color=discord.Color.green())
        embed.add_field(name="Moderation", value="`ban`, `unban`, `kick`, `mute`, `unmute`, `warn`, `warnings`,"
                                                 " `clearwarns`")
        embed.add_field(name="Utility", value="`ping`, `purge`, `rank`, `leaderboard`")

        await ctx.send(embed=embed)

    @help.command()
    async def ban(self, ctx: commands.Context):
        embed = discord.Embed(title="Ban", description="Bans a member", color=discord.Color.green())
        embed.add_field(name="Usage", value="`ban <member> [reason]`")
        await ctx.send(embed=embed)

    @help.command()
    async def unban(self, ctx: commands.Context):
        embed = discord.Embed(title="Unban", description="Unbans a member", color=discord.Color.green())
        embed.add_field(name="Usage", value="`unban <member>`")
        await ctx.send(embed=embed)

    @help.command()
    async def kick(self, ctx: commands.Context):
        embed = discord.Embed(title="Kick", description="Kicks a member", color=discord.Color.green())
        embed.add_field(name="Usage", value="`kick <member> [reason]`")
        await ctx.send(embed=embed)

    @help.command()
    async def mute(self, ctx: commands.Context):
        embed = discord.Embed(title="Mute", description="Mutes a member", color=discord.Color.green())
        embed.add_field(name="Usage", value="`mute <member> <time> <reason>`")
        embed.add_field(name="Time Format", value="`1d1h1m1s`")
        await ctx.send(embed=embed)

    @help.command()
    async def unmute(self, ctx: commands.Context):
        embed = discord.Embed(title="Unmute", description="Unmutes a member", color=discord.Color.green())
        embed.add_field(name="Usage", value="`unmute <member>`")
        await ctx.send(embed=embed)

    @help.command()
    async def warn(self, ctx: commands.Context):
        embed = discord.Embed(title="Warn", description="Warns a member", color=discord.Color.green())
        embed.add_field(name="Usage", value="`warn <member> [reason]`")
        await ctx.send(embed=embed)

    @help.command()
    async def warnings(self, ctx: commands.Context):
        embed = discord.Embed(title="Warnings", description="Shows a member's warnings", color=discord.Color.green())
        embed.add_field(name="Usage", value="`warnings <member>`")
        await ctx.send(embed=embed)

    @help.command()
    async def clearwarns(self, ctx: commands.Context):
        embed = discord.Embed(title="Clear Warns", description="Clears a member's warnings", color=discord.Color.green())
        embed.add_field(name="Usage", value="`clearwarns <member>`")
        await ctx.send(embed=embed)

    @help.command()
    async def ping(self, ctx: commands.Context):
        embed = discord.Embed(title="Ping", description="Shows the bot's latency", color=discord.Color.green())
        embed.add_field(name="Usage", value="`ping`")
        await ctx.send(embed=embed)

    @help.command()
    async def purge(self, ctx: commands.Context):
        embed = discord.Embed(title="Purge", description="Deletes a number of messages", color=discord.Color.green())
        embed.add_field(name="Usage", value="`purge <amount>`")
        await ctx.send(embed=embed)

    @help.command()
    async def rank(self, ctx: commands.Context):
        embed = discord.Embed(title="Rank", description="Shows a member's rank", color=discord.Color.green())
        embed.add_field(name="Usage", value="`rank [member]`")
        await ctx.send(embed=embed)

    @help.command()
    async def leaderboard(self, ctx: commands.Context):
        embed = discord.Embed(title="Leaderboard", description="Shows the server's leaderboard", color=discord.Color.green())
        embed.add_field(name="Usage", value="`leaderboard`")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
