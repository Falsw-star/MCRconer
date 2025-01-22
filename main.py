import mcrcon # type: ignore
import json, time
import re
import copy

from libs.text import *

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

    def command(self, command: str) -> str:
        result = self._send(2, command)
         # time.sleep(0.003)  # MC-72390 workaround, it is fixed.
        return result

def _call(command: str) -> str:
    if not CLIENT: raise ValueError("Please connect to server first.")
    print(f"Sending command: {command}")
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
    def __init__(self, *, message: TextComponent | None = None, target: str = "@a") -> None:
        """If message is not empty, method __init__ will send it.
        Use method send to send message to server within returned server's response."""
        self.message = message
        self.target = target
        if message is not None: self.send(message, target)
        
    def send(self, message: TextComponent, target: str = "") -> str:
        if not target: target = self.target
        command = f"tellraw {target} {message.json()}"
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
    
    def _add(self, command: str) -> None:
        self.queue.append(lambda: _call(command))
    
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
    
    def title(self, content: TextComponent, target: str = "") -> 'titler':
        if not target: target = self.target
        command = f"title {target} title {content.json()}"
        self._add(command)
        return self
    
    def subtitle(self, content: TextComponent, target: str = "") -> 'titler':
        if not target: target = self.target
        command = f"title {target} subtitle {content.json()}"
        self._add(command)
        return self
    
    def actionbar(self, content: TextComponent, target: str = "") -> 'titler':
        if not target: target = self.target
        command = f"title {target} actionbar {content.json()}"
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

def particle(name: str,
             pos: tuple[float, float, float] = (0, 0, 0),
             delta: tuple[float, float, float] = (0, 0, 0),
             speed: float = 1.0,
             count: int = 0,
             mode: str = "force",
             viewers: str = "@a") -> str:
    """Method particle will send particle to server.
    Check https://zh.minecraft.wiki/w/%E7%B2%92%E5%AD%90#%E7%B1%BB%E5%9E%8B for more particle names."""
    x, y, z = pos
    dx, dy, dz = delta
    command = f"particle {name} {x} {y} {z} {dx} {dy} {dz} {speed} {count} {mode} {viewers}"
    return _call(command)

class particler:
    def __init__(self,
                 default_pos: tuple[float, float, float] = (0, 0, 0),
                 default_delta: tuple[float, float, float] = (0, 0, 0),
                 default_speed: float = 0.005,
                 default_count: int = 0,
                 default_mode: str = "force",
                 default_viewers: str = "@a") -> None:
        """Method __init__ will not send command to server.
        Notice: pos is absolute position, delta is relative position to default_pos."""
        self.default_pos = default_pos
        self.default_delta = default_delta
        self.default_speed = default_speed
        self.default_count = default_count
        self.default_mode = default_mode
        self.default_viewers = default_viewers
    
    def get_canvas(self, center: tuple[float, float, float] | tuple = ()) -> 'particler.canvas':
        return particler.canvas(self, center)
    
    class canvas(object):
        def __init__(self, particler: 'particler',
                     center: tuple[float, float, float] | tuple = ()) -> None:
            """Method __init__ will not send command to server."""
            if not center: center = particler.default_pos
            self.center = center
            self.particler = particler
            self.queue: list[tuple[str, tuple[float, float, float], tuple[float, float, float], float, int, str, str, float]] = []
            self.density: int = 3
            self.time_pos: float = 0
            self.default_name: str = "smoke"
        def set_density(self, density: int) -> 'particler.canvas':
            """Method set_density will set the density of particles.
            Unit: per block."""
            self.density = density
            return self
        def set_default_name(self, name: str) -> 'particler.canvas':
            self.default_name = name
            return self
        
        def get_pen(self) -> 'particler.canvas.pen':
            return particler.canvas.pen(self)

        class pen(object):
            def __init__(self, canvas: 'particler.canvas') -> None:
                self.canvas = canvas
                self.queue: list[tuple[str, tuple[float, float, float], tuple[float, float, float], float, int, str, str, float]] = []
                self.time_pos: float = 0
                self.max_time_pos: float = 0

            def set_time_pos(self, time_pos: float) -> 'particler.canvas.pen':
                self.time_pos = self.canvas.time_pos + time_pos
                self.max_time_pos = self.time_pos
                return self

            def dot(self,
                    pos: tuple[float, float, float] = (0, 0, 0),
                    wait: float = 0,
                    name: str = "") -> 'particler.canvas.pen':
                if not name: name = self.canvas.default_name
                x, y, z = pos
                dx, dy, dz = self.canvas.particler.default_delta
                speed = self.canvas.particler.default_speed
                count = self.canvas.particler.default_count
                mode = self.canvas.particler.default_mode
                viewers = self.canvas.particler.default_viewers
                self.queue.append((name, (x, y, z), (dx, dy, dz), speed, count, mode, viewers, self.time_pos + wait))
                return self

            def line(self,
                     start: tuple[float, float, float] = (0, 0, 0),
                     end: tuple[float, float, float] = (0, 0, 0),
                     duration: float = 0,
                     name: str = "") -> 'particler.canvas.pen':
                x1, y1, z1 = start
                x2, y2, z2 = end
                length = ((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)**0.5
                dot_count = int(length * self.canvas.density)
                dx, dy, dz = (x2 - x1) / dot_count, (y2 - y1) / dot_count, (z2 - z1) / dot_count
                dot_wait = duration / dot_count
                for i in range(dot_count):
                    x, y, z = x1 + dx * i, y1 + dy * i, z1 + dz * i
                    self.dot((x, y, z), dot_wait * i, name)
                if self.max_time_pos < self.time_pos + duration: self.max_time_pos = self.time_pos + duration
                return self
            
            def throw(self, add_max_time_pos: bool = False) -> 'particler.canvas':
                self.canvas.queue.extend(self.queue)
                if add_max_time_pos: self.canvas.time_pos += self.max_time_pos
                return self.canvas
        
        def show(self) -> 'particler':
            cx, cy, cz = self.center
            particles = [(name, (cx + x, cy + y, cz + z), (dx, dy, dz), speed, count, mode, viewers, time_pos)
                        for name, (x, y, z), (dx, dy, dz), speed, count, mode, viewers, time_pos in self.queue]
            particles.sort(key=lambda x: x[-1])
            for i in range(len(particles)):
                name, pos, delta, speed, count, mode, viewers, time_pos = particles[i]
                wait = time_pos - particles[i - 1][-1] if i > 0 else 0
                particle(name, pos, delta, speed, count, mode, viewers)
                time.sleep(wait)
            return self.particler