import discord
from discord.ext import commands

class ConfigCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def setprefix(self, ctx, prefix):
        cursor = self.client.db.cursor()
        cursor.execute("UPDATE guild_data SET prefix=? WHERE guild_id=?", (prefix, str(ctx.guild.id)))
        self.client.db.commit()

    @commands.command()
    async def setownerid(self, ctx, owner_id):
        cursor = self.client.db.cursor()
        cursor.execute("UPDATE guild_data SET owner_id=? WHERE guild_id=?", (owner_id, str(ctx.guild.id)))
        self.client.db.commit()

    @commands.command()
    async def setsessioncookie(self, ctx, session_cookie):
        cursor = self.client.db.cursor()
        cursor.execute("UPDATE guild_data SET session_cookie=? WHERE guild_id=?", (session_cookie, str(ctx.guild.id)))
        self.client.db.commit()

def setup(client):
    try:
        client.add_cog(ConfigCommands(client))
        print("ConfigCommands successfully loaded!")
    except:
        print("Error while loading ConfigCommands.")
