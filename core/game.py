#core/game.py
class Game:
    def __init__(self, appid, name):
        self.appid = appid
        self.name = name

    def __repr__(self):
        return f"Game(appid={self.appid}, name='{self.name}')"
