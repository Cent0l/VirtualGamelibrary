from fastapi import APIRouter, HTTPException
from application.fetch_games import FetchGames
from api.steam_api_service import SteamAPIService
from core.game import Game
from pydantic import BaseModel

router = APIRouter()
steam_api_service = SteamAPIService()
fetch_games_use_case = FetchGames(steam_api_service)


class GameModel(BaseModel):
    appid: int
    name: str


@router.get("/games", response_model=list[GameModel])
async def get_all_games():
    games = await fetch_games_use_case.execute()
    return [GameModel(appid=game.appid, name=game.name) for game in games]


@router.get("/games/{appid}", response_model=GameModel)
async def get_game_by_appid(appid: int):
    game = await fetch_games_use_case.get_game_by_appid(appid)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found.")
    return GameModel(appid=game.appid, name=game.name)


@router.get("/game/search", response_model=list[GameModel])
async def search_games_by_name(name: str):
    games = await fetch_games_use_case.get_games_by_name(name)
    if not games:
        raise HTTPException(status_code=404, detail="No games found with the given name.")
    return [GameModel(appid=game.appid, name=game.name) for game in games]
