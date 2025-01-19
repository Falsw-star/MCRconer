import mcrcon # type: ignore
import json, time
import re

from typing import Callable

__version__ = "0.1.0"

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

class JsonText(object):
    def __init__(self, text: str = "",
            color: str = "white",
            font: str = "",
            bold: bool = False,
            italic: bool = False,
            underlined: bool = False,
            strikethrough: bool = False,
            obfuscated: bool = False) -> None:
        self.color = color
        self.font = font
        self.bold = bold
        self.italic = italic
        self.underlined = underlined
        self.strikethrough = strikethrough
        self.obfuscated = obfuscated
        self.text = text
    
    def __str__(self) -> str:
        content: dict = {
            "text": self.text,
            "color": self.color
        }
        if self.font: content["font"] = self.font
        if self.bold: content["bold"] = self.bold
        if self.italic: content["italic"] = self.italic
        if self.underlined: content["underlined"] = self.underlined
        if self.strikethrough: content["strikethrough"] = self.strikethrough
        if self.obfuscated: content["obfuscated"] = self.obfuscated
        return json.dumps(content, ensure_ascii=False)

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
    def __init__(self, *, message: JsonText | None = None, target: str = "@a") -> None:
        """If message is not empty, method __init__ will send it.
        Use method send to send message to server within returned server's response."""
        self.message = message
        self.target = target
        if message: self.send(message, target)
        
    def send(self, message: JsonText, target: str = "") -> str:
        if not target: target = self.target
        command = f"tellraw {target} {message.__str__()}"
        return _call(command)

class titler(object):
    def __init__(self, target: str = "@a", fade_in: float = 0.5, stay: float = 3.5, fade_out: float = 1.0, wait: bool = False, save_queue: bool = False) -> None:
        """Method __init__ will not send meassage to server.
        Fades in, stays, and fades out are in seconds."""
        self.target = target
        self.fade_in: int = round(fade_in * 20)
        self.stay: int = round(stay * 20)
        self.fade_out: int = round(fade_out * 20)
        self.wait = wait

        self.queue: list[Callable[[], str]] = []
        self.save_queue = save_queue
    
    def _wait(self) -> None:
        if self.wait: time.sleep(self.fade_in + self.stay + self.fade_out)
    
    def reset(self, target: str = "") -> str:
        if not target: target = self.target
        command = f"title {target} reset"
        return _call(command)
    def clear(self, target: str = "") -> str:
        if not target: target = self.target
        command = f"title {target} clear"
        return _call(command)
    
    def _add(self, command: str) -> None:
        self.queue.append(lambda: _call(command))
    
    def title(self, content: JsonText | str, target: str = "") -> 'titler':
        if not target: target = self.target
        command = f"title {target} times {self.fade_in} {self.stay} {self.fade_out} title {content.__str__()}"
        self._add(command)
        return self
    
    def subtitle(self, content: JsonText | str, target: str = "") -> 'titler':
        if not target: target = self.target
        command = f"title {target} times {self.fade_in} {self.stay} {self.fade_out} subtitle {content.__str__()}"
        self._add(command)
        return self
    
    def actionbar(self, content: JsonText | str, target: str = "") -> 'titler':
        if not target: target = self.target
        command = f"title {target} times {self.fade_in} {self.stay} {self.fade_out} actionbar {content.__str__()}"
        self._add(command)
        return self
    
    def run(self, wait: bool | None = None) -> str:
        response = ""
        for command in self.queue:
            response += command()
        if not self.save_queue: self.queue = []
        if wait is True or self.wait is True: self._wait()
        return response
        

def playsound(sound: str,
              source: str = "master",
              target: str = "@a",
              pos: tuple[float, float, float] = (0, 0, 0),
              volume: float = 1.0,
              pitch: float = 1.0) -> str:
    """Method playsound will play sound to server.
    Check https://minecraft.fandom.com/zh/wiki/Sounds.json for more sound names."""
    x, y, z = pos
    command = f"playsound {sound} {source} {target} {x} {y} {z} {volume} {pitch}"
    return _call(command)

class banner(object):
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