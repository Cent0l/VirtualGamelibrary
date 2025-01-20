import aiohttp

class SteamAPIService:
    BASE_URL = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=json"
    DETAILS_URL = "https://store.steampowered.com/api/appdetails?appids={appid}&cc=us&l=en"
    NEWS_URL = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={appid}&count=5&format=json"


    async def fetch_game_list(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.BASE_URL) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("applist", {}).get("apps", [])
                else:
                    print(f"Error while downloading data: {response.status}")
                    return []

    async def fetch_game_details(self, appid):
        url = self.DETAILS_URL.format(appid=appid)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get(str(appid), {}).get('success'):
                        return data[str(appid)]['data']
                else:
                    print(f"Error while downloading game details: {response.status}")
                    return None

    async def fetch_game_news(self, appid):
        url = self.NEWS_URL.format(appid=appid)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("appnews", {}).get("newsitems", [])
                else:
                    print(f"Error fetching news: {response.status}")
                    return []
