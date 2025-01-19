import mcrcon # type: ignore
import json, time
import re

from typing import Callable, Union

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
            color: str = "",
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
        self.extras: list[JsonText] = []
    
    def __str__(self) -> str:
        content: dict = {
            "text": self.text,
        }
        if self.color: content["color"] = self.color
        if self.font: content["font"] = self.font
        if self.bold: content["bold"] = self.bold
        if self.italic: content["italic"] = self.italic
        if self.underlined: content["underlined"] = self.underlined
        if self.strikethrough: content["strikethrough"] = self.strikethrough
        if self.obfuscated: content["obfuscated"] = self.obfuscated
        result = json.dumps(content, ensure_ascii=False)
        if self.extras:
            result += ", " + ", ".join([str(extra) for extra in self.extras])
            result = f"[{result}]"
        return result

    def __add__(self, other: Union[str, 'JsonText']) -> 'JsonText':
        if isinstance(other, str):
            other = JsonText(other)
        if isinstance(other, JsonText):
            self.extras.append(other)
            return self

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
    def __init__(self, target: str = "@a", fade_in: float = 0.5, stay: float = 3.5, fade_out: float = 1.0, wait: bool = True, save_queue: bool = False) -> None:
        """Method __init__ will not send meassage to server.
        Fades in, stays, and fades out are in seconds."""
        self.target = target
        self.fade_in: int = round(fade_in * 20)
        self.stay: int = round(stay * 20)
        self.fade_out: int = round(fade_out * 20)
        self.wait_f = lambda: time.sleep(fade_in + stay + fade_out) if wait else None
        self.queue: list[Callable[[], str]] = []
        self.save_queue = save_queue
    
    def times(self,
              fade_in: float | None | None = None,
              stay: float | None = None,
              fade_out: float | None = None) -> 'titler':
        
        if fade_in: self.fade_in = round(fade_in * 20)
        if stay: self.stay = round(stay * 20)
        if fade_out: self.fade_out = round(fade_out * 20)
        command = f"title {self.target} times {self.fade_in} {self.stay} {self.fade_out}"
        self._add(command)
        return self
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
    
    def title(self, content: JsonText, target: str = "") -> 'titler':
        if not target: target = self.target
        command = f"title {target} title {content.__str__()}"
        self._add(command)
        return self
    
    def subtitle(self, content: JsonText, target: str = "") -> 'titler':
        if not target: target = self.target
        command = f"title {target} subtitle {content.__str__()}"
        self._add(command)
        return self
    
    def actionbar(self, content: JsonText, target: str = "") -> 'titler':
        if not target: target = self.target
        command = f"title {target} actionbar {content.__str__()}"
        self._add(command)
        return self
    
    def run(self) -> str:
        response = ""
        for command in self.queue:
            response += command()
        self.wait_f()
        response += self.reset()
        if not self.save_queue: self.queue = []
        return response
        
def playsound(sound: str,
              source: str = "ambient",
              target: str = "@a",
              pos: tuple[float, float, float] = (0, 0, 0),
              volume: float = 1.0,
              pitch: float = 1.0,
              min_volume: float = 1.0,) -> str:
    """Method playsound will play sound to server.
    Check https://minecraft.fandom.com/zh/wiki/Sounds.json for more sound names."""
    x, y, z = pos
    command = f"playsound {sound} {source} {target} {x} {y} {z} {volume} {pitch} {min_volume}"
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