import os
import sqlite3
import discord
from discord.ext import commands
import inflect
import query

BOT_TOKEN = os.getenv("BOT_TOKEN")

ENGINE = inflect.engine()

def get_prefix(client, message):
    cursor = client.db.cursor()
    cursor.execute(f"SELECT prefix FROM guild_data WHERE guild_id=\"{message.guild.id}\"")
    return cursor.fetchone()[0]

def get_owner_id(client, message):
    cursor = client.db.cursor()
    cursor.execute(f"SELECT owner_id FROM guild_data WHERE guild_id=\"{message.guild.id}\"")
    return cursor.fetchone()[0]

def get_session_cookie(client, message):
    cursor = client.db.cursor()
    cursor.execute(f"SELECT session_cookie FROM guild_data WHERE guild_id=\"{message.guild.id}\"")
    return cursor.fetchone()[0]

def get_linked_id(client, aoc_id):
    cursor = client.db.cursor()
    cursor.execute(f"SELECT user_id FROM link_data WHERE aoc_id=\"{aoc_id}\"")
    resp = cursor.fetchone()
    if resp:
        return resp[0]
    else:
        return None


async def mention_linked(client, aoc_id):
    id = get_linked_id(client, aoc_id)
    if id:
        user = await client.fetch_user(id)
        return user.mention
    else:
        return ""

async def leaderboard_embed(client, ctx, leaderboard):
    members = leaderboard["members"]

    embed = discord.Embed(title=f"{ctx.guild.name} Advent of Code Leaderboard", colour=discord.Colour(0x663399), url="https://adventofcode.com")

    embed.set_author(name="Advent of Code Bot", icon_url=str(client.user.avatar_url))

    place = 0

    for member in members:
        place += 1
        mention = await mention_linked(client,members[member]['id'])
        mention_string = f"{f'Linked to {mention}' if mention else ''}"
        embed.add_field(name=f"{ENGINE.ordinal(place)} Place: {members[member]['name']}", value=f"{mention_string}\n{members[member]['stars']} :star:\nLocal Score: {members[member]['local_score']}\nGlobal Score: {members[member]['global_score']}", inline=False)

    return embed

client = commands.Bot(get_prefix)

client.db = sqlite3.connect("data.db")

@client.event
async def on_ready():
    cursor = client.db.cursor()
    for guild in client.guilds:
        cursor.execute(f"SELECT * FROM guild_data WHERE guild_id=\"{guild.id}\"")
        if not cursor.fetchone():
            cursor.execute(f"INSERT INTO guild_data (guild_id, prefix) VALUES (\"{guild.id}\",\">\")")
            client.db.commit()

    await client.change_presence(activity=discord.Game("Coding!"))
    print("Bot is online!")

@client.event
async def on_guild_join(guild):
    cursor = client.db.cursor()
    cursor.execute(f"INSERT INTO guild_data (guild_id, prefix) VALUES (\"{guild.id}\",\">\")")
    client.db.commit()

@client.event
async def on_guild_remove(guild):
    cursor = client.db.cursor()
    cursor.execute(f"DELETE FROM guild_data WHERE guild_id=\"{guild.id}\"")
    client.db.commit()

@client.command()
async def setprefix(ctx,prefix):
    cursor = client.db.cursor()
    cursor.execute(f"UPDATE guild_data SET prefix=\"{prefix}\" WHERE guild_id=\"{ctx.guild.id}\"")
    client.db.commit()

@client.command()
async def setownerid(ctx,id):
    cursor = client.db.cursor()
    cursor.execute(f"UPDATE guild_data SET owner_id=\"{id}\" WHERE guild_id=\"{ctx.guild.id}\"")
    client.db.commit()

@client.command()
async def setsessioncookie(ctx,cookie):
    cursor = client.db.cursor()
    cursor.execute(f"UPDATE guild_data SET session_cookie=\"{cookie}\" WHERE guild_id=\"{ctx.guild.id}\"")
    client.db.commit()

@client.command()
async def link(ctx,aoc_id):
    cursor = client.db.cursor()
    cursor.execute(f"SELECT aoc_id FROM link_data WHERE user_id=\"{ctx.author.id}\"")
    if cursor.fetchone():
        cursor.execute(f"UPDATE link_data SET aoc_id=\"{aoc_id}\" WHERE user_id=\"{ctx.author.id}\"")
    else:
        cursor.execute(f"INSERT INTO link_data (aoc_id, user_id) VALUES (\"{aoc_id}\", \"{ctx.author.id}\")")
    client.db.commit()

@client.command()
async def unlink(ctx):
    cursor = client.db.cursor()
    cursor.execute(f"DELETE FROM link_data WHERE user_id=\"{ctx.author.id}\"")
    client.db.commit()

@client.command(aliases=["lb"])
async def leaderboard(ctx):
    lb = query.PrivateLeaderboard(get_owner_id(client,ctx),get_session_cookie(client,ctx)).get(ctx)
    embed = await leaderboard_embed(client, ctx, lb)
    await ctx.send(embed=embed)

client.run(BOT_TOKEN)
