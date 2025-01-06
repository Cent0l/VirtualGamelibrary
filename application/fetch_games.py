from api.steam_api_service import SteamAPIService
from core.game import Game
from difflib import SequenceMatcher


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

    async def get_game_details(self, appid):
        details = await self.steam_api_service.fetch_game_details(appid)
        if details:
            return details
        return None

    async def get_game_news(self, appid):
        news = await self.steam_api_service.fetch_game_news(appid)
        if news:
            return news
        return None


    class FetchGames:


        def _similarity(self, a, b):
            """Prosta metryka podobieństwa dwóch ciągów."""
            return SequenceMatcher(None, a.lower(), b.lower()).ratio()

        async def get_recommendations(self, appid: int, limit: int = 5):
            """
            Zwraca listę rekomendowanych gier na podstawie podobieństwa nazwy.
            """
            games = await self.execute()
            current_game = await self.get_game_by_appid(appid)
            if not current_game:
                return []

            recommendations = sorted(
                games,
                key=lambda game: self._similarity(current_game.name, game.name),
                reverse=True
            )

            # Pomijamy aktualnie wyszukiwaną grę
            recommendations = [game for game in recommendations if game.appid != appid]

            return recommendations[:limit]

