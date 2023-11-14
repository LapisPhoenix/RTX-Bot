import difflib
import time
import random
import asyncio
import aiosqlite
from googletrans import Translator
from langdetect import detect
import discord
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.cooldowns = {}
        # 8 messages in 10 seconds
        self.anti_spam = commands.CooldownMapping.from_cooldown(8, 10, commands.BucketType.member)
        self.too_many_violations = commands.CooldownMapping.from_cooldown(4, 60, commands.BucketType.member)

        with open("banned words.txt", "r") as file:
            self.banned_words = file.read().splitlines()

        self.translator = Translator()

    @property
    async def reaction_roles(self):
        red = ('🔴', self.bot.guilds[0].get_role(1172343525631864892))
        blue = ('🔵', self.bot.guilds[0].get_role(1172343555818279002))
        green = ('🟢', self.bot.guilds[0].get_role(1172343596364615752))
        purple = ('🟣', self.bot.guilds[0].get_role(1172343634545356880))
        yellow = ('🟡', self.bot.guilds[0].get_role(1172343700089745428))
        orange = ('🟠', self.bot.guilds[0].get_role(1172343724269916250))
        giveaway = ('🎉', self.bot.guilds[0].get_role(1172384557799047208))
        video = ('📷', self.bot.guilds[0].get_role(1172751862093598850))
        bot_update = ('🤖', self.bot.guilds[0].get_role(1172752855724195981))
        announcements = ('🔊', self.bot.guilds[0].get_role(1172752879153586206))

        return red, blue, green, purple, yellow, orange, giveaway, video, bot_update, announcements

    async def handle_xp(self, message: discord.Message):
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
                    # 0: id, 1: warnings, 2: xp, 3: level
                    user = (message.author.id, 0, 0, 0)  # Default values for a new user

                xp = user[2]
                level = user[3]
                xp_level_threshold = round(5 * (level ** 2) + 50 * level + 100)
                xp_gained = random.randint(15, 25)  # Random number between 15 and 25
                xp += xp_gained

                level_5_role = message.guild.get_role(1172439547267780608)
                level_10_role = message.guild.get_role(1172439680759894066)
                level_15_role = message.guild.get_role(1172439729963290674)
                level_20_role = message.guild.get_role(1172439762829848626)
                level_30_role = message.guild.get_role(1172439797739048960)
                level_40_role = message.guild.get_role(1172439884875694080)
                level_50_role = message.guild.get_role(1172439934527877130)
                level_60_role = message.guild.get_role(1172439961782452284)
                level_69_role = message.guild.get_role(1172440031542116402)
                level_70_role = message.guild.get_role(1172440140879249478)
                level_80_role = message.guild.get_role(1172440226187186247)
                level_90_role = message.guild.get_role(1172440302146048011)
                level_100_role = message.guild.get_role(1172440361046659112)

                if xp >= xp_level_threshold:
                    level += 1
                    xp -= xp_level_threshold
                    embed = discord.Embed(title="Level Up!", description=f"{message.author.mention} "
                                                                         f"has leveled up to level {level}",
                                          color=discord.Color.green())
                    await message.channel.send(embed=embed)

                    if level == 5:
                        await message.author.add_roles(level_5_role)
                    elif level == 10:
                        await message.author.add_roles(level_10_role)
                    elif level == 15:
                        await message.author.add_roles(level_15_role)
                    elif level == 20:
                        await message.author.add_roles(level_20_role)
                    elif level == 30:
                        await message.author.add_roles(level_30_role)
                    elif level == 40:
                        await message.author.add_roles(level_40_role)
                    elif level == 50:
                        await message.author.add_roles(level_50_role)
                    elif level == 60:
                        await message.author.add_roles(level_60_role)
                    elif level == 69:
                        await message.author.add_roles(level_69_role)
                    elif level == 70:
                        await message.author.add_roles(level_70_role)
                    elif level == 80:
                        await message.author.add_roles(level_80_role)
                    elif level == 90:
                        await message.author.add_roles(level_90_role)
                    elif level == 100:
                        await message.author.add_roles(level_100_role)

                await db.execute("UPDATE users SET xp=?, level=? WHERE id=?", (xp, level, message.author.id))
                await db.commit()

                # Set cooldown for user
                self.cooldowns[message.author.id] = time.time()

    async def bump_reminder_task(self, message):
        await asyncio.sleep(7200)
        person = self.bot.get_user(message.interaction.user.id)
        await message.channel.send(f"{person.mention} Time to bump the server again!")

    async def handle_bumping(self, message):
        bump_channel = self.bot.get_channel(1172398920836595732)

        if message.channel == bump_channel:
            if message.author.id == 302050872383242240 and message.embeds:
                if "Bump done!" in message.embeds[0].description:
                    # Get the person who bumped
                    person = self.bot.get_user(message.interaction.user.id)
                    await message.channel.send(f"Thanks for bumping {person.mention}!"
                                               f" I'll remind you to bump again in 2 hours.")
                    self.bot.loop.create_task(self.bump_reminder_task(message))
                    return

    async def handle_censorship(self, message):
        if any(bad_word in message.content.lower() for bad_word in self.banned_words):
            if "skbidi toilet" in message.content.lower() and message.author.id == 725491843923574845:
                return
            await message.delete()
            await message.channel.send(f"{message.author.mention} You can't say that here!", delete_after=5)
            return

    async def translate(self, message):
        original_language = detect(message.content)
        if original_language == "en":
            return

        translation = self.translator.translate(message.content, dest="en")

        embed = discord.Embed(title="Translation", description=f"Original: {message.content}\n"
                                                                f"Translation: {translation.text}",
                              color=discord.Color.blue())
        embed.set_footer(text=f"Translated from {original_language.upper()} to ENGLISH")
        await message.channel.send(embed=embed)

    async def handle_spam(self, message):
        admin_role = message.guild.get_role(1156429381166702652)
        if isinstance(message.channel, discord.TextChannel) \
                and admin_role not in message.author.roles and \
                not isinstance(message.channel, discord.DMChannel) and \
                not message.author.bot:
            bucket = self.anti_spam.get_bucket(message)
            retry_after = bucket.update_rate_limit()
            if retry_after:
                await message.delete()
                epoch_time = round(time.time() + retry_after)
                await message.channel.send(f"{message.author.mention} You're sending messages too fast! "
                                           f"Try again in <t:{epoch_time}:R>.", delete_after=retry_after)
                return

        await self.handle_xp(message)

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
        if message.guild is None:
            return

        await self.handle_bumping(message)

        if message.author.bot:
            return

        await self.handle_spam(message)
        await self.handle_censorship(message)
        await self.translate(message)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id != 1172343220504641596:
            return

        # Define Emoji and Role
        roles = await self.reaction_roles

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

        roles = await self.reaction_roles

        current_roles = member.roles

        for role_group in roles:
            if payload.emoji.name == role_group[0] and role_group[1] in current_roles:
                await member.remove_roles(role_group[1])
                await member.send(f"Removed role: {role_group[1].name}")
                return
            else:
                await member.send("You don't have this role!")
                return


async def setup(bot):
    await bot.add_cog(Events(bot))
