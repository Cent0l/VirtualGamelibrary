import asyncio
from application.fetch_games import FetchGames
from api.steam_api_service import SteamAPIService


async def main():

    steam_api_service = SteamAPIService()
    fetch_games_use_case = FetchGames(steam_api_service)


    games = await fetch_games_use_case.execute()


    print("list of games:")
    for game in games[:5]:  # Wyświetl konkretne gry
        print(game)


if __name__ == "__main__":
    asyncio.run(main())
