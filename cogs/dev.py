import discord
from discord.ext import commands


class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command()
    @commands.is_owner()
    async def reload_all(self, ctx: commands.Context):
        for extension in self.bot.extensions:
            await self.bot.reload_extension(extension)
        await ctx.send("Reloaded all cogs")

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx: commands.Context, extension: str):
        await self.bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"Loaded {extension}")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx: commands.Context, extension: str):
        await self.bot.unload_extension(f"cogs.{extension}")
        await ctx.send(f"Unloaded {extension}")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, extension: str):
        await self.bot.reload_extension(f"cogs.{extension}")
        await ctx.send(f"Reloaded {extension}")

    @commands.command()
    @commands.is_owner()
    async def set_status(self, ctx: commands.Context, *, status: str):
        await self.bot.change_presence(activity=discord.Game(status))
        await ctx.send(f"Set status to {status}")

    @commands.command()
    @commands.is_owner()
    async def dm(self, ctx: commands.Context, member: discord.Member, *, message: str):
        try:
            await member.send(message)
            await ctx.send(f"Sent message to {member.mention}")
        except discord.Forbidden:
            await ctx.send(f"Couldn't send message to {member.mention}")


async def setup(bot):
    await bot.add_cog(Dev(bot))
