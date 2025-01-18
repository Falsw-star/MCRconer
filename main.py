import mcrcon # type: ignore
import os, json
import re


CLIENT: 'Rcon' = None # type: ignore


class Rcon(mcrcon.MCRcon):
    def __init__(self, host, password, port=25575, tlsmode=0, timeout=5):
        super().__init__(host, password, port, tlsmode, timeout)
    def connect(self):
        global CLIENT
        CLIENT = self
        return super().connect()
    def disconnect(self):
        global CLIENT
        CLIENT = None
        return super().disconnect()

def _call(command: str) -> str:
    if not CLIENT: raise ValueError("Please connect to server first.")
    return CLIENT.command(command)

def say(message: str) -> str:
    return _call(f"say {message}")

def list_players() -> list:
    """Method list will return a list of players online."""
    raw = _call("list")
    pattern = r'players online: (.*)'
    players: list[str] = re.findall(pattern, raw)[0].split(",")
    players = [player.strip() for player in players]
    return players

class tellraw(object):
    def __init__(self, message: str = "", target: str = "@a", 
            color: str = "white",
            font: str = "",
            bold: bool = False,
            italic: bool = False,
            underlined: bool = False,
            strikethrough: bool = False,
            obfuscated: bool = False) -> None:
        """If message is not empty, method __init__ will send it.
        Use method send to send message to server within returned server's response."""
        self.target = target
        self.color = color
        self.font = font
        self.bold = bold
        self.italic = italic
        self.underlined = underlined
        self.strikethrough = strikethrough
        self.obfuscated = obfuscated
        if message: self.send(message, target)
        
    def send(self, message: str, target: str = "") -> str:
        if not target: target = self.target
        content: dict = {
            "text": message,
            "color": self.color
        }
        if self.font: content["font"] = self.font
        if self.bold: content["bold"] = self.bold
        if self.italic: content["italic"] = self.italic
        if self.underlined: content["underlined"] = self.underlined
        if self.strikethrough: content["strikethrough"] = self.strikethrough
        if self.obfuscated: content["obfuscated"] = self.obfuscated
        command = f"tellraw {target} {json.dumps(content, ensure_ascii=False)}"
        return _call(command)

class ban(object):
    def __init__(self, player: str = "") -> None:
        """Method __init__ will not send command to server.
        Use method ban or pardon."""
        self.player = player

    def ban(self, player: str = "") -> str:
        if not player: player = self.player
        if not player: raise ValueError("Please input player name.")
        return _call(f"ban {player}")
    
    def pardon(self, player: str = "") -> str:
        if not player: player = self.player
        if not player: raise ValueError("Please input player name.")
        return _call(f"pardon {player}")
    
    def ban_ip(self, ip: str = "") -> str:
        if not ip: raise ValueError("Please input ip address.")
        return _call(f"ban-ip {ip}")

    def pardon_ip(self, ip: str = "") -> str:
        if not ip: raise ValueError("Please input ip address.")
        return _call(f"pardon-ip {ip}")
    
    def list(self) -> list:
        raw = _call("banlist").split("\n")
        count_line = raw.pop(0)
        pattern = r'(.*?) was banned by Server'
        return [ns[0] for ns in [re.findall(pattern, l) for l in raw] if ns]