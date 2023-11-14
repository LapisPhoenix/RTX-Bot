import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.group(invoke_without_command=True)
    async def help(self, ctx: commands.Context):
        embed = discord.Embed(title="Help", color=discord.Color.green())
        embed.add_field(name="Moderation", value="`ban`, `unban`, `kick`, `mute`, `unmute`, `warn`, `warnings`,"
                                                 " `clearwarns`, `lock`, `unlock`")
        embed.add_field(name="Utility", value="`ping`, `purge`, `rank`, `leaderboard`, `help`, `giveaway`, `poll`")
        embed.add_field(name="Dev", value="`load`, `unload`, `reload`, `reload_all`, `set_status`, `dm`, `list_cogs`")
        embed.add_field(name="Fun", value="`coinflip`, `dice`, `random`, `choose`, `rps`")

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

    @help.command()
    async def lock(self, ctx: commands.Context):
        embed = discord.Embed(title="Lock", description="Locks a channel", color=discord.Color.green())
        embed.add_field(name="Usage", value="`lock`")
        await ctx.send(embed=embed)

    @help.command()
    async def unlock(self, ctx: commands.Context):
        embed = discord.Embed(title="Unlock", description="Unlocks a channel", color=discord.Color.green())
        embed.add_field(name="Usage", value="`unlock`")
        await ctx.send(embed=embed)

    @help.command()
    async def load(self, ctx: commands.Context):
        embed = discord.Embed(title="Load", description="Loads a cog", color=discord.Color.green())
        embed.add_field(name="Usage", value="`load <cog>`")
        await ctx.send(embed=embed)

    @help.command()
    async def unload(self, ctx: commands.Context):
        embed = discord.Embed(title="Unload", description="Unloads a cog", color=discord.Color.green())
        embed.add_field(name="Usage", value="`unload <cog>`")
        await ctx.send(embed=embed)

    @help.command()
    async def reload(self, ctx: commands.Context):
        embed = discord.Embed(title="Reload", description="Reloads a cog", color=discord.Color.green())
        embed.add_field(name="Usage", value="`reload <cog>`")
        await ctx.send(embed=embed)

    @help.command()
    async def reload_all(self, ctx: commands.Context):
        embed = discord.Embed(title="Reload All", description="Reloads all cogs", color=discord.Color.green())
        embed.add_field(name="Usage", value="`reload_all`")
        await ctx.send(embed=embed)

    @help.command()
    async def set_status(self, ctx: commands.Context):
        embed = discord.Embed(title="Set Status", description="Sets the bot's status", color=discord.Color.green())
        embed.add_field(name="Usage", value="`set_status <status>`")
        await ctx.send(embed=embed)

    @help.command()
    async def dm(self, ctx: commands.Context):
        embed = discord.Embed(title="DM", description="DMs a member", color=discord.Color.green())
        embed.add_field(name="Usage", value="`dm <member> <message>`")
        await ctx.send(embed=embed)

    @help.command()
    async def giveaway(self, ctx: commands.Context):
        embed = discord.Embed(title="Giveaway", description="Starts a giveaway", color=discord.Color.green())
        embed.add_field(name="Usage", value="`giveaway <time> <winners> <prize>`")
        embed.add_field(name="Time Format", value="`1d1h1m1s`")
        await ctx.send(embed=embed)

    @help.command()
    async def list_cogs(self, ctx: commands.Context):
        embed = discord.Embed(title="List Cogs", description="Lists all cogs", color=discord.Color.green())
        embed.add_field(name="Usage", value="`list_cogs`")
        await ctx.send(embed=embed)

    @help.command()
    async def poll(self, ctx: commands.Context):
        embed = discord.Embed(title="Poll", description="Creates a poll", color=discord.Color.green())
        embed.add_field(name="Usage", value="`poll <question>`")
        await ctx.send(embed=embed)

    @help.command()
    async def coinflip(self, ctx: commands.Context):
        embed = discord.Embed(title="Coinflip", description="Flips a coin", color=discord.Color.green())
        embed.add_field(name="Usage", value="`coinflip`")
        await ctx.send(embed=embed)

    @help.command()
    async def dice(self, ctx: commands.Context):
        embed = discord.Embed(title="Dice", description="Rolls a die", color=discord.Color.green())
        embed.add_field(name="Usage", value="`dice`")
        await ctx.send(embed=embed)

    @help.command()
    async def random(self, ctx: commands.Context):
        embed = discord.Embed(title="Random", description="Generates a random number", color=discord.Color.green())
        embed.add_field(name="Usage", value="`random <start: Default=0> <end: Default=100>`")
        await ctx.send(embed=embed)

    @help.command()
    async def choose(self, ctx: commands.Context):
        embed = discord.Embed(title="Choose", description="Chooses between multiple choices", color=discord.Color.green())
        embed.add_field(name="Usage", value="`choose <choice1> <choice2> ...`")
        await ctx.send(embed=embed)

    @help.command()
    async def rps(self, ctx: commands.Context):
        embed = discord.Embed(title="RPS", description="Plays rock paper scissors", color=discord.Color.green())
        embed.add_field(name="Usage", value="`rps <choice>`")
        embed.add_field(name="Choices", value="`rock`, `paper`, `scissors`")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
