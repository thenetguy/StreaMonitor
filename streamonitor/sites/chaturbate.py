import requests
from streamonitor.bot import Bot

class Chaturbate(Bot):
    site = 'Chaturbate'
    siteslug = 'CB'

    def __init__(self, username):
        super().__init__(username)
        self.sleep_on_offline = 30
        self.sleep_on_error = 60

    def getVideoUrl(self):
        return self.getWantedResolutionPlaylist(self.lastInfo['url'])

    def getStatus(self):
        headers = {"Content-Type": "application/json"}
        data = [{"username": self.username}]

        try:
            r = requests.post("https://cf.netconnect.work/check_status", headers=headers, json=data)
            result = r.json()[0]

            if result["status"] == "PUBLIC":
                status = self.Status.PUBLIC
            elif result["status"] in ["PRIVATE", "HIDDEN"]:
                status = self.Status.PRIVATE
            elif result["status"] == "OFFLINE":
                status = self.Status.OFFLINE
            else:
                status = self.Status.RATELIMIT

            self.lastInfo = {"url": result["m3u8_url"]}
        except Exception as e:
            print(f"An error occurred: {e}")
            status = self.Status.RATELIMIT

        self.ratelimit = status == self.Status.RATELIMIT
        return status

Bot.loaded_sites.add(Chaturbate)
