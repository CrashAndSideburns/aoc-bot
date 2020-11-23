import discord
from discord.ext import commands

class InfoCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def github(self, ctx):
        await ctx.send("https://github.com/CrashAndSideburns/aoc-bot")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.client.latency * 1000)} ms")

def setup(client):
    try:
        client.add_cog(InfoCommands(client))
        print("InfoCommands successfully loaded!")
    except:
        print("Error while loading InfoCommands.")
