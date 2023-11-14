import random
import datetime
import time
import discord
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command()
    async def coinflip(self, ctx: commands.Context):
        """Flip a coin"""
        if random.randint(0, 1) == 0:
            await ctx.send("Heads")
        else:
            await ctx.send("Tails")

    @commands.command()
    async def dice(self, ctx: commands.Context):
        """Roll a die"""
        await ctx.send(f"You rolled a {random.randint(1, 6)}")

    @commands.command()
    async def random(self, ctx: commands.Context, start: int = 0, end: int = 100):
        """Generate a random number"""
        await ctx.send(f"Your random number is {random.randint(start, end)}")

    @commands.command()
    async def choose(self, ctx: commands.Context, *choices):
        """Choose between multiple choices"""
        await ctx.send(f"I choose {random.choice(choices)}")

    @commands.command()
    async def rps(self, ctx: commands.Context, choice: str):
        """Play rock paper scissors"""
        choices = ["rock", "paper", "scissors"]
        if choice not in choices:
            await ctx.send("Invalid choice")
            return

        bot_choice = random.choice(choices)
        if choice == bot_choice:
            await ctx.send(f"I chose {bot_choice} so we tied")
        elif choice == "rock" and bot_choice == "paper":
            await ctx.send(f"I chose {bot_choice} so I win")
        elif choice == "rock" and bot_choice == "scissors":
            await ctx.send(f"I chose {bot_choice} so you win")
        elif choice == "paper" and bot_choice == "rock":
            await ctx.send(f"I chose {bot_choice} so you win")
        elif choice == "paper" and bot_choice == "scissors":
            await ctx.send(f"I chose {bot_choice} so I win")
        elif choice == "scissors" and bot_choice == "rock":
            await ctx.send(f"I chose {bot_choice} so I win")
        elif choice == "scissors" and bot_choice == "paper":
            await ctx.send(f"I chose {bot_choice} so you win")

    @commands.command()
    async def poll(self, ctx: commands.Context, *, question: str):
        """Create a poll"""
        embed = discord.Embed(title="Poll", description=question, color=discord.Color.green())
        embed.set_footer(text=f"Poll created by {ctx.author.display_name}", icon_url=ctx.author.avatar_url if ctx.author.avatar_url else ctx.author.default_avatar_url)
        message = await ctx.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")
        await message.add_reaction("🤷")


async def setup(bot):
    await bot.add_cog(Fun(bot))
