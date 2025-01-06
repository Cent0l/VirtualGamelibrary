from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from api.steam_api_service import SteamAPIService
from application.fetch_games import FetchGames
from core.game import Game
import json

app = FastAPI()

# Inicjalizacja serwisów
steam_api_service = SteamAPIService()
fetch_games_use_case = FetchGames(steam_api_service)

# Wczytanie biblioteki z pliku JSON
def load_library():
    try:
        with open("library.json", "r") as file:
            data = json.load(file)
            return [Game(**game) for game in data]
    except FileNotFoundError:
        return []

# Zapis biblioteki do pliku JSON
def save_library(library):
    with open("library.json", "w") as file:
        json.dump([game.__dict__ for game in library], file)

# Przechowywanie biblioteki w pamięci
library = load_library()


# Model Pydantic do reprezentacji gry
class GameModel(BaseModel):
    appid: int
    name: str

# Endpointy
@app.get("/games", response_model=list[GameModel])
async def get_all_games():
    """
    Zwraca listę wszystkich dostępnych gier.
    """
    games = await fetch_games_use_case.execute()
    return [GameModel(appid=game.appid, name=game.name) for game in games]

@app.get("/games/{appid}", response_model=GameModel)
async def get_game_by_appid(appid: int):
    """
    Wyszukuje grę po AppID.
    """
    game = await fetch_games_use_case.get_game_by_appid(appid)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found.")
    return GameModel(appid=game.appid, name=game.name)

@app.get("/games/search", response_model=list[GameModel])
async def search_games_by_name(name: str):
    """
    Wyszukuje gry na podstawie nazwy lub jej części.
    """
    games = await fetch_games_use_case.get_games_by_name(name)
    if not games:
        raise HTTPException(status_code=404, detail="No games found with the given name.")
    return [GameModel(appid=game.appid, name=game.name) for game in games]

@app.get("/games/{appid}/news")
async def get_game_news(appid: int):
    """
    Zwraca wiadomości dla gry na podstawie AppID.
    """
    news = await fetch_games_use_case.get_game_news(appid)
    if not news:
        raise HTTPException(status_code=404, detail="No news found for the given game.")
    return news

@app.post("/library", response_model=GameModel)
async def add_game_to_library(appid: int):
    """
    Dodaje grę do biblioteki użytkownika.
    """
    game = await fetch_games_use_case.get_game_by_appid(appid)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found.")
    # Sprawdzanie, czy gra już jest w bibliotece
    if any(g.appid == appid for g in library):
        raise HTTPException(status_code=400, detail="Game already in library.")
    library.append(game)
    save_library(library)
    return GameModel(appid=game.appid, name=game.name)

@app.get("/library", response_model=list[GameModel])
async def get_user_library():
    """
    Zwraca listę gier w bibliotece użytkownika.
    """
    return [GameModel(appid=game.appid, name=game.name) for game in library]

@app.get("/games/{appid}/recommendations", response_model=list[GameModel])
async def get_game_recommendations(appid: int, limit: int = 5):
    """
    Zwraca listę rekomendowanych gier na podstawie podobieństwa nazwy.
    """
    recommendations = await fetch_games_use_case.get_recommendations(appid, limit)
    if not recommendations:
        raise HTTPException(status_code=404, detail="No recommendations found.")
    return [GameModel(appid=game.appid, name=game.name) for game in recommendations]

