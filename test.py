from main import *
import time

with Rcon("127.0.0.1", "FalswIsNotCute", 25575) as rcon:
    tlr = titler(wait=True)
    tlr.title(JsonText("Hello Minecraft", color="gold", bold=True)).subtitle("Welcome to MCRconer!").run()
    playsound("entity.player.levelup")
    tellraw(message=JsonText("Little_1 is so cute!", italic=True, color="red"))
    banner().ban("Khouserless")