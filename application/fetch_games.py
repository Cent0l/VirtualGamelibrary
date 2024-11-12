
from api.steam_api_service import SteamAPIService
from core.game import Game

class FetchGames:
    def __init__(self, steam_api_service: SteamAPIService):
        self.steam_api_service = steam_api_service

    async def execute(self):
        games_data = await self.steam_api_service.fetch_game_list()
        return [Game(appid=game['appid'], name=game['name']) for game in games_data]
