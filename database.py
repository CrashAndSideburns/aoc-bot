def get_prefix(client, message):
    cursor = client.db.cursor()
    cursor.execute("SELECT prefix FROM guild_data WHERE guild_id=?", (str(message.guild.id),))
    return cursor.fetchone()[0]

def get_owner_id(database, guild_id):
    cursor = database.cursor()
    cursor.execute("SELECT owner_id FROM guild_data WHERE guild_id=?", (str(guild_id),))
    return cursor.fetchone()[0]

def get_session_cookie(database, guild_id):
    cursor = database.cursor()
    cursor.execute("SELECT session_cookie FROM guild_data WHERE guild_id=?", (str(guild_id),))
    return cursor.fetchone()[0]

def get_aoc_id(database, user_id):
    cursor = database.cursor()
    cursor.execute("SELECT aoc_id FROM link_data WHERE user_id=?", (str(user_id),))
    resp = cursor.fetchone()
    if resp:
        return resp[0]
    else:
        return None
