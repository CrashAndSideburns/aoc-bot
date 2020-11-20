import requests
import json
import ratelimit

class PrivateLeaderboard:
    def __init__(self,owner_id,session_cookie):
        self.owner_id = owner_id
        self.session_cookie = session_cookie

    def url(self):
        return f"https://adventofcode.com/2020/leaderboard/private/view/{self.owner_id}.json"

    def package_cookie(self):
        return {"session" : self.session_cookie}

    @ratelimit.limits(calls=1)
    def __get(self):
        return requests.get(self.url(),cookies=self.package_cookie()).json()

    def get(self,ctx):
        try:
            data = self.__get()
            with open(f"cache/{ctx.guild.id}.json","w") as f:
                json.dump(data,f)
            return data
        except:
            with open(f"cache/{ctx.guild.id}.json","r") as f:
                return json.load(f)
