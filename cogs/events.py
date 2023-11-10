import difflib
import time
import random
import aiosqlite
import discord
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.cooldowns = {}
        with open("banned words.txt", "r") as file:
            self.banned_words = file.read().splitlines()

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandNotFound):
            command = ctx.message.content.split()[0][len(ctx.prefix):]
            command_list = [command.name for command in self.bot.commands]
            matches = difflib.get_close_matches(command, command_list, n=1, cutoff=0.5)
            if matches:
                await ctx.send(f"Command not found. Did you mean `{ctx.prefix}{matches[0]}`?")
            else:
                await ctx.send("Command not found")

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the required permissions to run this command")

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument: `{error.param.name}`")

        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"Bad argument: `{error}`")

        elif isinstance(error, commands.NotOwner):
            await ctx.send("You must be the owner of the bot to run this command")

        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown. Try again in {round(error.retry_after, 1)} seconds")

        elif isinstance(error, commands.MissingRole):
            await ctx.send(f"You are missing the required role: `{error.missing_role}`")

        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("I don't have the required permissions to run this command")

        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send("This command cannot be used in private messages")

        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You don't have permission to run this command")

        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"An error occurred while running this command: `{error}`")

        else:
            await ctx.send(f"An error occurred while running this command: `{error}`")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        async with aiosqlite.connect("main.db") as db:
            async with db.execute("SELECT * FROM users WHERE id=?", (member.id,)) as cursor:
                if await cursor.fetchone() is None:
                    await db.execute("INSERT INTO users VALUES (?, ?, ?, ?)",
                                     (member.id, 0, 0, 0))
                    await db.commit()

        welcome_channel = self.bot.get_channel(1156412425625677854)
        rules_channel = self.bot.get_channel(1156430562135916556)
        reaction_role_channel = self.bot.get_channel(1172334020781154334)
        message = (f"{member.mention} Welcome to the server! Please read the rules in {rules_channel.mention} and "
                   f"get your roles in {reaction_role_channel.mention}.\n"
                   f"You are the member: \# **{member.guild.member_count}**")   # noqa

        await welcome_channel.send(message)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        async with aiosqlite.connect("main.db") as db:
            await db.execute("DELETE FROM users WHERE id=?", (member.id,))
            await db.commit()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if message.guild is None:
            return

        if message.content.lower() in self.banned_words:
            await message.delete()
            await message.channel.send(f"{message.author.mention} You can't say that here!", delete_after=5)
            return

        # Check if user is in cooldown
        if message.author.id in self.cooldowns:
            if time.time() - self.cooldowns[message.author.id] < 4:  # 4 second cooldown
                return
            else:
                del self.cooldowns[message.author.id]

        async with aiosqlite.connect("main.db") as db:
            async with db.execute("SELECT * FROM users WHERE id=?", (message.author.id,)) as cursor:
                user = await cursor.fetchone()
                if user is None:
                    await db.execute("INSERT INTO users VALUES (?, ?, ?, ?)",
                                     (message.author.id, 0, 0, 0))
                    await db.commit()
                    user = (message.author.id, 0, 0, 0)  # Default values for a new user

                xp = user[2]
                level = user[3]
                xp_level_threshold = round(5 * (level ** 2) + 50 * level + 100)
                xp_gained = random.randint(15, 25)  # Random number between 15 and 25
                xp += xp_gained

                if xp >= xp_level_threshold:
                    level += 1
                    xp -= xp_level_threshold
                    embed = discord.Embed(title="Level Up!", description=f"{message.author.mention} "
                                                                         f"has leveled up to level {level}",
                                          color=discord.Color.green())
                    await message.channel.send(embed=embed)

                await db.execute("UPDATE users SET xp=?, level=? WHERE id=?", (xp, level, message.author.id))
                await db.commit()

                # Set cooldown for user
                self.cooldowns[message.author.id] = time.time()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id != 1172343220504641596:
            return

        # Define Emoji and Role
        red = ('🔴', payload.member.guild.get_role(1172343525631864892))
        blue = ('🔵', payload.member.guild.get_role(1172343555818279002))
        green = ('🟢', payload.member.guild.get_role(1172343596364615752))
        purple = ('🟣', payload.member.guild.get_role(1172343634545356880))
        yellow = ('🟡', payload.member.guild.get_role(1172343700089745428))
        orange = ('🟠', payload.member.guild.get_role(1172343724269916250))
        giveaway = ('🎉', payload.member.guild.get_role(1172384557799047208))
        roles = [red, blue, green, purple, yellow, orange, giveaway]

        current_roles = payload.member.roles

        for role_group in roles:
            if payload.emoji.name == role_group[0] and role_group[1] not in current_roles:
                await payload.member.add_roles(role_group[1])
                await payload.member.send(f"Added role: {role_group[1].name}")
                return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.message_id != 1172343220504641596:
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        if member is None:
            # Member not found, can't perform role operations
            return

        # Define Emoji and Role
        red = ('🔴', guild.get_role(1172343525631864892))
        blue = ('🔵', guild.get_role(1172343555818279002))
        green = ('🟢', guild.get_role(1172343596364615752))
        purple = ('🟣', guild.get_role(1172343634545356880))
        yellow = ('🟡', guild.get_role(1172343700089745428))
        orange = ('🟠', guild.get_role(1172343724269916250))
        giveaway = ('🎉', guild.get_role(1172384557799047208))
        roles = [red, blue, green, purple, yellow, orange, giveaway]

        current_roles = member.roles

        for role_group in roles:
            if payload.emoji.name == role_group[0] and role_group[1] in current_roles:
                await member.remove_roles(role_group[1])
                await member.send(f"Removed role: {role_group[1].name}")
                return
            else:
                await member.send("You don't have a role from this group")
                return


async def setup(bot):
    await bot.add_cog(Events(bot))
