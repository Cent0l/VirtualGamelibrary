from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from api.steam_api_service import SteamAPIService
from application.fetch_games import FetchGames
from core.game import Game
import json

app = FastAPI()

steam_api_service = SteamAPIService()
fetch_games_use_case = FetchGames(steam_api_service)


def load_library():
    try:
        with open("library.json", "r") as file:
            data = json.load(file)
            return [Game(**game) for game in data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_library(library):
    with open("library.json", "w") as file:
        json.dump([game.__dict__ for game in library], file)


#loads library
library = load_library()


class GameModel(BaseModel):
    appid: int
    name: str


class CustomGameModel(BaseModel):
    name: str



#Endpointy API
@app.get("/games", response_model=list[GameModel])
async def get_all_games():
    games = await fetch_games_use_case.execute()
    return [GameModel(appid=game.appid, name=game.name) for game in games]

@app.get("/games/{appid}", response_model=GameModel)
async def get_game_by_appid(appid: int):
    game = await fetch_games_use_case.get_game_by_appid(appid)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found.")
    return GameModel(appid=game.appid, name=game.name)

@app.get("/game/search", response_model=list[GameModel])
async def search_games_by_name(name: str):
    games = await fetch_games_use_case.get_games_by_name(name)
    return [GameModel(appid=game.appid, name=game.name) for game in games]

@app.get("/games/{appid}/details")
async def get_game_details(appid: int):
    details = await fetch_games_use_case.get_game_details(appid)
    if not details:
        raise HTTPException(status_code=404, detail="No details found for the given game.")
    return details

@app.get("/games/{appid}/news")
async def get_game_news(appid: int):
    news = await fetch_games_use_case.get_game_news(appid)
    if not news:
        raise HTTPException(status_code=404, detail="No news found for the given game.")
    return news

@app.get("/games/{appid}/recommendations", response_model=list[GameModel])
async def get_game_recommendations(appid: int, limit: int = 5):
    recommendations = await fetch_games_use_case.get_recommendations(appid, limit)
    return [GameModel(appid=game.appid, name=game.name) for game in recommendations]

@app.post("/library/adde/{appid}", response_model=GameModel)
async def add_existing_game_to_library(appid: int):
    game = await fetch_games_use_case.get_game_by_appid(appid)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found.")

    if any(g.appid == appid for g in library):
        raise HTTPException(status_code=400, detail="Game already in library.")

    library.append(game)
    save_library(library)
    return GameModel(appid=game.appid, name=game.name)

@app.post("/library/addc/{name}", response_model=GameModel)
async def add_custom_game(name: str):
    existing_appids = [game.appid for game in library]
    new_appid = max(existing_appids, default=1000000) + 1

    new_game = Game(appid=new_appid, name=name)
    library.append(new_game)
    save_library(library)
    return GameModel(appid=new_game.appid, name=new_game.name)

@app.delete("/library/delete/{appid}", response_model=dict)
async def delete_game_from_library(appid: int):
    global library
    if not any(g.appid == appid for g in library):
        raise HTTPException(status_code=404, detail="Game not found in library.")

    library = [game for game in library if game.appid != appid]
    save_library(library)
    return {"detail": f"Game with appid {appid} has been removed from your library."}

@app.get("/library", response_model=list[GameModel])
async def get_user_library():
    return [GameModel(appid=game.appid, name=game.name) for game in library]