import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Connected as {bot.user}")

# ---------------- BASIC COMMANDS ----------------

@bot.command()
async def ping(ctx):
    await ctx.message.delete()
    await ctx.send("Pong")

@bot.command()
async def test(ctx):
    await ctx.message.delete()
    await ctx.send("Bot is working")

@bot.command()
async def help(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        title="Available Commands",
        color=discord.Color.blue()
    )
    embed.add_field(name="!ping", value="Test bot latency", inline=False)
    embed.add_field(name="!test", value="Check if bot works", inline=False)
    embed.add_field(name="!create <channel_name> <amount>", value="Create one or multiple text channels", inline=False)
    embed.add_field(name="!ban <@member|ALL> [reason]", value="Ban a member or everyone", inline=False)
    embed.add_field(name="!kick <@member|ALL> [reason]", value="Kick a member or everyone", inline=False)
    embed.add_field(name="!clear <amount>", value="Delete last messages in channel", inline=False)
    embed.add_field(name="!spam <message> <amount>", value="Send a message multiple times", inline=False)
    embed.add_field(name="!talk <message>", value="Make the bot say the given message", inline=False)
    await ctx.send(embed=embed)

# ---------------- MODERATION COMMANDS ----------------

@bot.command()
async def create(ctx, channel_name: str, amount: int = 1):
    await ctx.message.delete()
    if amount < 1 or amount > 10000:
        await ctx.send("Amount of channels must be between 1 and 10000.")
        return

    created_channels = []
    for i in range(1, amount + 1):
        name = f"{channel_name}-{i}" if amount > 1 else channel_name
        channel = await ctx.guild.create_text_channel(name)
        created_channels.append(channel.name)

    await ctx.send(f"Channels created: {', '.join(created_channels)}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, target: str, *, reason: str = "No reason provided"):
    await ctx.message.delete()
    if target.upper() == "ALL":
        await ctx.send("CONFIRMATION REQUIRED: Type `!confirm_ban_all` to continue.")
        bot.confirm_ban_all = reason
        return
    try:
        member = await commands.MemberConverter().convert(ctx, target)
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} has been banned\nReason: {reason}")
    except:
        await ctx.send("Failed to ban this member")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, target: str, *, reason: str = "No reason provided"):
    await ctx.message.delete()
    if target.upper() == "ALL":
        await ctx.send("CONFIRMATION REQUIRED: Type `!confirm_kick_all` to continue.")
        bot.confirm_kick_all = reason
        return
    try:
        member = await commands.MemberConverter().convert(ctx, target)
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} has been kicked\nReason: {reason}")
    except:
        await ctx.send("Failed to kick this member")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.message.delete()
    if amount < 1 or amount > 10000:
        await ctx.send("You can delete between 1 and 10000 messages at once.")
        return
    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f"{len(deleted)} messages deleted")

# ---------------- SPAM ----------------

@bot.command()
async def spam(ctx, *, args: str):
    await ctx.message.delete()
    try:
        msg, nbr = args.rsplit(" ", 1)
        nbr = int(nbr)
        if nbr < 1 or nbr > 5000:
            await ctx.send("You can spam between 1 and 5000 messages.")
            return
        for _ in range(nbr):
            await ctx.send(msg)
    except:
        await ctx.send("Error: use `!spam <message> <amount>`")

# ---------------- TALK ----------------

@bot.command()
async def talk(ctx, *, message: str):
    await ctx.message.delete()
    await ctx.send(message)

# ---------------- CONFIRMATIONS FOR ALL ----------------

@bot.command()
async def confirm_ban_all(ctx):
    await ctx.message.delete()
    reason = getattr(bot, "confirm_ban_all", None)
    if not reason:
        await ctx.send("No action to confirm.")
        return
    count = 0
    for member in ctx.guild.members:
        if member == ctx.guild.owner or member == ctx.me or member.guild_permissions.administrator:
            continue
        try:
            await member.ban(reason=reason)
            count += 1
        except:
            continue
    bot.confirm_ban_all = None
    await ctx.send(f"{count} members have been banned")

@bot.command()
async def confirm_kick_all(ctx):
    await ctx.message.delete()
    reason = getattr(bot, "confirm_kick_all", None)
    if not reason:
        await ctx.send("No action to confirm.")
        return
    count = 0
    for member in ctx.guild.members:
        if member == ctx.guild.owner or member == ctx.me or member.guild_permissions.administrator:
            continue
        try:
            await member.kick(reason=reason)
            count += 1
        except:
            continue
    bot.confirm_kick_all = None
    await ctx.send(f"{count} members have been kicked")

# ---------------- ERROR HANDLING ----------------

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to ban members.")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to kick members.")

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to delete messages.")

bot.run(TOKEN)
