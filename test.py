from main import *

with Rcon("127.0.0.1", "FalswIsNotCute", 25575) as rcon:
    b = banner()
    print(b.list())