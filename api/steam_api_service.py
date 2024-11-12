
import aiohttp

class SteamAPIService:
    BASE_URL = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=json"

    async def fetch_game_list(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.BASE_URL) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("applist", {}).get("apps", [])
                else:
                    print(f"file while downloading data: {response.status}")
                    return []
