import discord
from discord.ext import commands
import os

import re
import random

bot = commands.Bot(command_prefix='!')

def dice_roll(sides):
    return random.randint(1, sides)

def fate_dice_roll():
    return random.randint(-1, 1)

def fate_value_to_sign(value):
    if value > 0:
        return "[+]"
    elif value < 0:
        return "[-]"
    else:
        return "[0]"

def roll_fate_dice(modifier = 0):
    rolls = [fate_dice_roll() for _ in range(4)]
    result = sum(rolls) + modifier

    notation = "4F{:+d}".format(modifier) if modifier else "4F"
    roll_str = " ".join(fate_value_to_sign(r) for r in rolls)
    modifier_str = "{:+d}".format(modifier) if modifier else ""
    return "Rolling {}: {} {} = {}".format(notation, roll_str, modifier_str, str(result))

def roll_dice(count, sides, modifier):
    rolls = [dice_roll(sides) for _ in range(count)]
    result = sum(rolls) + modifier

    notation = "{:d}d{:d}{:+d}".format(count, sides, modifier) if modifier else "{:d}d{:d}".format(count, sides)
    roll_str = " ".join("[{:d}]".format(r) for r in rolls)
    modifier_str = "{:+d}".format(modifier) if modifier else ""
    return "Rolling {}: {} {} = {}".format(notation, roll_str, modifier_str, str(result))

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

help_str = """
Available commands:
  /roll /r /fate /f
examples:
  /roll d6
  /roll 2d6
  /roll 2d6-3
  /roll f+2
  /fate 2
"""

@bot.command()
async def help(ctx):
    await ctx.send(help_str)

@bot.command()
async def greet(ctx):
    await ctx.send("I'm pleased to be of service.")

@bot.command(name="roll", aliases=["r"])
async def roll(ctx, *args):
    """
    Use regular dice notation:
        (N)d(S)[+-](M)
        f[+-](M)

        4d6 + 3
        4d6+3

        F+2
        4F+2
    """

    notation = "".join(args).lower().strip()
    print("command: roll ", repr(notation))

    match = re.match(r"(f|4f)([+-]\d*)?", notation)
    if match:
        print("has match f")
        (_, modifier) = match.groups()
        modifier = int(modifier if modifier else 0)
        await ctx.send(roll_fate_dice(modifier))

    match = re.match(r"(\d*)d(\d*)([+-]\d*)?", notation)
    if match:
        print("has match d")
        (count, side, modifier) = match.groups()
        count = int(count if count else 1)
        side = int(side if side else 6)
        modifier = int(modifier if modifier else 0)
        await ctx.send(roll_dice(count, side, modifier))
    pass

@bot.command(name="fate", aliases=["f"])
async def fate(ctx, modifier: int = 0):
    await ctx.send(roll_fate_dice(modifier))

bot.run(os.environ["DISCORD_TOKEN"])
