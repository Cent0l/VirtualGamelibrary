#EKSPERYMENTALNE
import asyncio
import tkinter as tk
from tkinter import messagebox
from application.fetch_games import FetchGames
from api.steam_api_service import SteamAPIService


class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steam Game Library")
        self.root.geometry("500x500")

        self.steam_api_service = SteamAPIService()
        self.fetch_games_use_case = FetchGames(self.steam_api_service)

        # Tworzenie przycisków do interakcji z użytkownikiem
        self.show_all_games_button = tk.Button(self.root, text="Show All Games", command=self.show_all_games)
        self.show_all_games_button.pack(pady=10)

        self.search_game_button = tk.Button(self.root, text="Search Game by AppID", command=self.search_game_by_appid)
        self.search_game_button.pack(pady=10)

        self.add_to_library_button = tk.Button(self.root, text="Add Game to Library", command=self.add_game_to_library)
        self.add_to_library_button.pack(pady=10)

        self.loop = asyncio.new_event_loop()  # Tworzymy nową pętlę zdarzeń
        asyncio.set_event_loop(self.loop)  # Ustawiamy ją jako aktywną pętlę zdarzeń

    async def show_all_games(self):
        """Pobierz i wyświetl wszystkie gry."""
        games = await self.fetch_games_use_case.execute()
        game_list = '\n'.join([f"{game.appid}: {game.name}" for game in games])

        messagebox.showinfo("Games List", game_list)

    async def search_game_by_appid(self):
        """Wyszukaj grę po AppID."""
        appid = int(input("Enter the game appid: "))
        game = await self.fetch_games_use_case.get_game_by_appid(appid)
        if game:
            messagebox.showinfo("Found Game", f"Game: {game.name}")
        else:
            messagebox.showinfo("Game Not Found", "No game found with the given appid.")

    def add_game_to_library(self):
        """Dodaj grę do biblioteki."""
        appid = int(input("Enter the game appid to add to your library: "))
        # Pytanie o dodanie gry do biblioteki
        response = messagebox.askyesno("Add Game", f"Do you want to add game {appid} to your library?")
        if response:
            messagebox.showinfo("Game Added", f"Game {appid} added to your library!")
        else:
            messagebox.showinfo("Game Not Added", f"Game {appid} not added to your library.")

    def start_async_task(self, coro):
        """Uruchom zadanie asynchroniczne w tle."""
        asyncio.ensure_future(coro)

    def run(self):
        """Start Tkinter mainloop with asyncio."""
        # Użyj after(), by uruchomić asyncio zadania
        self.root.after(100, self.start_async_task, self.show_all_games())
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    app.run()
