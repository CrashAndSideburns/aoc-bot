import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

import leaderboard as lb
import database

class LeaderboardCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 900, BucketType.guild)
    @commands.command()
    async def leaderboard(self, ctx):
        owner_id = database.get_owner_id(self.client.db, ctx.guild.id)
        session_cookie = database.get_session_cookie(self.client.db, ctx.guild.id)
        leaderboard = lb.Leaderboard(owner_id, session_cookie)
        await ctx.send(embed = await leaderboard.make_embed(ctx, self.client, from_cached=False))

    @leaderboard.error
    async def leaderboard_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            owner_id = database.get_owner_id(self.client.db, ctx.guild.id)
            session_cookie = database.get_session_cookie(self.client.db, ctx.guild.id)
            leaderboard = lb.Leaderboard(owner_id, session_cookie)
            await ctx.send(embed = await leaderboard.make_embed(ctx, self.client, from_cached=True))

    @commands.command()
    async def link(self, ctx, aoc_id):
        query = database.get_aoc_id(self.client.db, ctx.author.id)
        cursor = self.client.db.cursor()
        if query:
            cursor.execute("UPDATE link_data SET aoc_id=? WHERE user_id=?", (aoc_id, str(ctx.author.id)))
        else:
            cursor.execute("INSERT INTO link_data (aoc_id, user_id) VALUES (?, ?)", (aoc_id, str(ctx.author.id)))
        self.client.db.commit()

    @commands.command()
    async def unlink(self, ctx):
        cursor = self.client.db.cursor()
        cursor.execute("DELETE FROM link_data WHERE user_id=?", (str(ctx.author.id),))
        self.client.db.commit()

def setup(client):
    try:
        client.add_cog(LeaderboardCommands(client))
        print("LeaderboardCommands successfully loaded!")
    except:
        print("Error while loading LeaderboardCommands.")
