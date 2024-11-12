# application/fetch_games.py
from api.steam_api_service import SteamAPIService
from core.game import Game


class FetchGames:
    def __init__(self, steam_api_service: SteamAPIService):
        self.steam_api_service = steam_api_service

    async def execute(self):
        games_data = await self.steam_api_service.fetch_game_list()
        return [Game(appid=game['appid'], name=game['name']) for game in games_data]

    async def get_game_by_appid(self, appid):
        games = await self.execute()
        for game in games:
            if game.appid == appid:
                return game
        return None

    async def get_games_by_name(self, name):
        games = await self.execute()
        return [game for game in games if name.lower() in game.name.lower()]
