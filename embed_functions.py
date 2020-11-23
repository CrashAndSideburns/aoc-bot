import inflect
import discord

ENGINE = inflect.engine()

async def make_mention(client, aoc_id):
    cursor = client.db.cursor()
    cursor.execute("SELECT user_id FROM link_data WHERE aoc_id=?", (str(aoc_id),))
    user_id = cursor.fetchone()
    if user_id:
        user = await client.fetch_user(int(user_id[0]))
        return user.mention
    else:
        return None

async def make_embed(client, ctx, lbdict):
    members = lbdict["members"]

    embed = discord.Embed(title=f"{ctx.guild.name} Advent of Code Leaderboard", colour=discord.Colour(0x663399), url="https://adventofcode.com")

    embed.set_author(name="Advent of Code Bot", icon_url=str(client.user.avatar_url))

    for member in members:
        place = members.index(member) + 1
        mention = await make_mention(client, member.id)
        mention_string = f"{f'Linked to {mention}' if mention else ''}"
        embed.add_field(name=f"{ENGINE.ordinal(place)} Place: {member.name}", value=f"{mention_string}\n{member.stars} :star:\nLocal Score: {member.local_score}\nGlobal Score: {member.global_score}", inline=False)

    return embed
