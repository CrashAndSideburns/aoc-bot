import requests
import json

class Member:
    def __init__(self, dict):
        self.global_score = dict["global_score"]
        self.name = dict["name"]
        self.stars = dict["stars"]
        self.last_star_ts = dict["last_star_ts"]
        self.completion_day_level = dict["completion_day_level"]
        self.id = dict["id"]
        self.local_score = dict["local_score"]

class Leaderboard:
    def __init__(self, owner_id, session_cookie):
        self.__owner_id = owner_id
        self.__session_cookie = session_cookie

    def __url(self):
        return f"https://adventofcode.com/2020/leaderboard/private/view/{self.__owner_id}.json"

    def __package_cookie(self):
        return {"session":self.__session_cookie}

    def get(self):
        leaderboard = requests.get(self.__url(), cookies=self.__package_cookie()).json()
        with open(f"cache/{self.__owner_id}.json","w") as f:
            json.dump(leaderboard, f)
        members = [Member(leaderboard["members"][id]) for id in leaderboard["members"]]
        return {"owner_id":leaderboard["owner_id"], "event":leaderboard["event"], "members":members}

    def get_cached(self):
        with open(f"cache/{self.__owner_id}.json","r") as f:
            leaderboard = json.load(f)
            members = [Member(leaderboard["members"][id]) for id in leaderboard["members"]]
            return {"owner_id":leaderboard["owner_id"], "event":leaderboard["event"], "members":members}
