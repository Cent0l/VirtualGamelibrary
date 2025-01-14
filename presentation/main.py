import asyncio
import json
from application.fetch_games import FetchGames
from api.steam_api_service import SteamAPIService

# Plik do przechowywania biblioteki użytkownika
library_file = "library.json"

def load_library():
    """Wczytuje bibliotekę z pliku JSON."""
    try:
        with open(library_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_library(library):
    """Zapisuje bibliotekę do pliku JSON."""
    with open(library_file, "w") as file:
        json.dump(library, file, indent=4)

async def main():
    steam_api_service = SteamAPIService()
    fetch_games_use_case = FetchGames(steam_api_service)

    # Wczytanie istniejącej biblioteki
    library = load_library()

    while True:
        print("\nSearch options:")
        print("1 - Show all available games")
        print("2 - Search game by appid")
        print("3 - Search games by name")
        print("4 - Get detailed information about a game by appid")
        print("5 - Add an existing game to your library by appid")
        print("6 - Add a custom game to your library")
        print("7 - Show your library")
        print("8 - Get game recommendations")
        print("0 - Exit")

        choice = input("Choose an option number: ")

        if choice == "1":
            games = await fetch_games_use_case.execute()
            print("\nList of games:")
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
            appid = int(input("Enter the appid of the game to add to your library: "))
            game = await fetch_games_use_case.get_game_by_appid(appid)
            if game:
                if any(g["appid"] == appid for g in library):
                    print(f"\nGame '{game.name}' is already in your library.")
                else:
                    library.append({"appid": game.appid, "name": game.name})
                    save_library(library)
                    print(f"\nGame '{game.name}' added to your library.")
            else:
                print("\nNo game found with the given appid.")

        elif choice == "6":
            name = input("Enter the name of the custom game: ")
            new_game = {"appid": len(library) + 1000000, "name": name}
            library.append(new_game)
            save_library(library)
            print(f"\nCustom game '{name}' added to your library.")

        elif choice == "7":
            if library:
                print("\nYour library:")
                for game in library:
                    print(f"AppID: {game['appid']}, Name: {game['name']}")
            else:
                print("\nYour library is empty.")

        elif choice == "8":
            appid = int(input("Enter the game appid to get recommendations: "))
            recommendations = await fetch_games_use_case.get_recommendations(appid)
            if recommendations:
                print("\nRecommended games:")
                for game in recommendations:
                    print(f"AppID: {game.appid}, Name: {game.name}")
            else:
                print("\nNo recommendations found.")

        elif choice == "0":
            print("\nExiting...")
            break

        else:
            print("\nInvalid option. Please choose a valid number.")


if __name__ == "__main__":
    asyncio.run(main())
