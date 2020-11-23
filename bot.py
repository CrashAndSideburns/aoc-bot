import os
import discord
from discord.ext import commands

import database

import sqlite3

BOT_TOKEN = os.getenv("BOT_TOKEN")

client = commands.Bot(database.get_prefix)

client.db = sqlite3.connect("data.db")

cogs = ["config_commands","leaderboard_commands","info_commands"]

if __name__ == "__main__":
    for cog in cogs:
        client.load_extension(cog)

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

client.run(BOT_TOKEN)
