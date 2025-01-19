from main import *
import time

with Rcon("127.0.0.1", "FalswIsNotCute", 25575) as rcon:
    say("Hello Minecraft")
    tellraw(message=JsonText("Hello TellRaw!", color="gold"))
    print(playsound("minecraft:entity.player.levelup", target="Falsw"))
    vtlr = titler()
    vtlr.title(JsonText("Welcome to", color="green", bold=True) + " " + JsonText("Minecraft", color="gold", bold=True))
    vtlr.subtitle(JsonText("A Python library for RCON", color="aqua"))
    vtlr.run()
    vtlr.actionbar(JsonText("Little is cute!", color="red", bold=True, italic=True))
    vtlr.run()