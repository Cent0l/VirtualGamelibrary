# presentation/main.py
import asyncio
from application.fetch_games import FetchGames
from api.steam_api_service import SteamAPIService


async def main():
    steam_api_service = SteamAPIService()
    fetch_games_use_case = FetchGames(steam_api_service)

    print("Search options:")
    print("1 - Show all available games")
    print("2 - Search game by appid")
    print("3 - Search games by name")

    choice = input("Choose an option number: ")

    if choice == "1":
        games = await fetch_games_use_case.execute()
        print("List of games:")
        for game in games[:]:  #daj liczbe po : [:5] zeby ilosc wyswietlic
            print(game)

    elif choice == "2":
        appid = int(input("Enter the game appid: "))
        game = await fetch_games_use_case.get_game_by_appid(appid)
        if game:
            print(f"\nFound game: {game}")
        else:
            print("\nNo game found with the given appid.")

    elif choice == "3":
        name = input("Give game name or part of it: ")
        games = await fetch_games_use_case.get_games_by_name(name)
        if games:
            print("\nFound games:")
            for game in games:
                print(game)
        else:
            print("\nNo games found with the given name.")

    else:
        print("\nInvalid option.")


if __name__ == "__main__":
    asyncio.run(main())
