import discord
import requests
import json
import inflect

ENGINE = inflect.engine()

class Member:
    def __init__(self, dict):
        self.global_score = dict["global_score"]
        self.name = dict["name"]
        self.stars = dict["stars"]
        self.last_star_ts = dict["last_star_ts"]
        self.completion_day_level = dict["completion_day_level"]
        self.id = dict["id"]
        self.local_score = dict["local_score"]

    async def mention(self, client):
        cursor = client.db.cursor()
        cursor.execute("SELECT user_id FROM link_data WHERE aoc_id=?", (self.id,))
        user_id = cursor.fetchone()
        if user_id:
            user = await client.fetch_user(int(user_id[0]))
            return user.mention
        else:
            return None

class Leaderboard:
    def __init__(self, owner_id, session_cookie):
        self.__owner_id = owner_id
        self.__session_cookie = session_cookie

    def __url(self):
        return f"https://adventofcode.com/2020/leaderboard/private/view/{self.__owner_id}.json"

    def __package_cookie(self):
        return {"session":self.__session_cookie}

    def __get(self):
        leaderboard = requests.get(self.__url(), cookies=self.__package_cookie()).json()
        with open(f"cache/{self.__owner_id}.json","w") as f:
            json.dump(leaderboard, f)
        members = sorted([Member(leaderboard["members"][id]) for id in leaderboard["members"]], key=lambda m: m.local_score, reverse=True)
        return {"owner_id":leaderboard["owner_id"], "event":leaderboard["event"], "members":members}

    def __get_cached(self):
        with open(f"cache/{self.__owner_id}.json","r") as f:
            leaderboard = json.load(f)
            members = sorted([Member(leaderboard["members"][id]) for id in leaderboard["members"]], key=lambda m: m.local_score, reverse=True)
            return {"owner_id":leaderboard["owner_id"], "event":leaderboard["event"], "members":members}

    async def make_embed(self, ctx, client, from_cached=True):
        embed = discord.Embed(title=f"{ctx.guild.name} Advent of Code Leaderboard", colour=discord.Colour(0x663399), url="https://adventofcode.com")
        embed.set_author(name="Advent of Code Bot", icon_url=str(client.user.avatar_url))
        if from_cached:
            leaderboard = self.__get_cached()
        else:
            leaderboard = self.__get()
        members = leaderboard["members"]
        for member in members:
            place = members.index(member) + 1
            mention = f"{f'Linked to {await member.mention(client)}' if await member.mention(client) else ''}"
            embed.add_field(name=f"{ENGINE.ordinal(place)} Place: {member.name}", value=f"{mention}\n{member.stars} :star:\nLocal Score: {member.local_score}\nGlobal Score: {member.global_score}", inline=False)
        return embed
