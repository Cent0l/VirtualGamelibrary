from fastapi import APIRouter, HTTPException
from core.game import Game
from pydantic import BaseModel
import json

router = APIRouter()
library_file = "library.json"


def load_library():
    try:
        with open(library_file, "r") as file:
            data = json.load(file)
            return [Game(**game) for game in data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_library(library):
    with open(library_file, "w") as file:
        json.dump([game.__dict__ for game in library], file)


library = load_library()


class GameModel(BaseModel):
    appid: int
    name: str


@router.get("/library", response_model=list[GameModel])
async def get_user_library():
    return [GameModel(appid=game.appid, name=game.name) for game in library]


@router.post("/library/adde/{appid}", response_model=GameModel)
async def add_existing_game_to_library(appid: int):
    if any(g.appid == appid for g in library):
        raise HTTPException(status_code=400, detail="Game already in library.")
    library.append(Game(appid=appid, name=f"Game {appid}"))
    save_library(library)
    return GameModel(appid=appid, name=f"Game {appid}")


@router.post("/library/addc/{name}", response_model=GameModel)
async def add_custom_game(name: str):
    existing_appids = [game.appid for game in library]
    new_appid = max(existing_appids, default=1000000) + 1
    new_game = Game(appid=new_appid, name=name)
    library.append(new_game)
    save_library(library)
    return GameModel(appid=new_appid, name=name)


@router.delete("/library/delete/{appid}", response_model=dict)
async def delete_game_from_library(appid: int):
    global library
    if not any(g.appid == appid for g in library):
        raise HTTPException(status_code=404, detail="Game not found in library.")
    library = [game for game in library if game.appid != appid]
    save_library(library)
    return {"detail": f"Game with appid {appid} has been removed from your library."}
