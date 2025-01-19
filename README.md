# MCRconer
Run a bunch of commands with a simple python script through rcon!  

## Usage
Before using this library, you need to install the `mcrcon` package using pip:  
```bash
pip install mcrcon
```  
Then you can start using the library by importing it in your python script:  
```python
from main import *

# First of all, open a connection to the server
# With block ensures that the connection is closed automatically,
# after all commands have been executed
with MCRcon('your.server.ip', 'your.rcon.password') as mcr:
    # Then, run some commands
    response = mcr.command('say Hello, world!') # directly call the command
    say('Hello, world!') # this is the same

    player_list = list_players()
    print(player_list)
    # etc...
    tlr = titler(wait=True)
    tlr.title(JsonText("Hello Minecraft", color="gold", bold=True)).subtitle("Welcome to MCRconer!").run()
    playsound("entity.player.levelup")
    tellraw(message=JsonText("Little_1 is so cute!", italic=True, color="red"))
    banner().ban("Khouserless")
# Automatically closes the connection
```