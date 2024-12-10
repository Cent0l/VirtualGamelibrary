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
    print("4 - Get detailed information about a game by appid")
    print("5 - Get news about a game by appid")

    choice = input("Choose an option number: ")

    if choice == "1":
        games = await fetch_games_use_case.execute()
        print("List of games:")
        for game in games[:5]:  # Show first 5 games for example
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

    elif choice == "4":
        appid = int(input("Enter the game appid to get detailed information: "))
        details = await fetch_games_use_case.get_game_details(appid)
        if details:
            print(f"\nGame details:")
            print(f"Name: {details.get('name')}")
            print(f"Description: {details.get('detailed_description', 'No description available.')}")
            print(f"Price: {details.get('price_overview', {}).get('final_formatted', 'No price available.')}")
        else:
            print("\nNo detailed information found for the given appid.")


    elif choice == "5":

        appid = int(input("Enter the game appid to get news: "))
        news = await fetch_games_use_case.get_game_news(appid)
        if news:
            print(f"\nNews for game {appid}:")
            for item in news[:5]:  # last 5 news
                print(f"Title: {item.get('title', 'No title')}")
                print(f"Contents: {item.get('contents', 'No content')}")
                print("----------------------------")
        else:

            print("\nNo news found for the given appid.")


if __name__ == "__main__":
    asyncio.run(main())
