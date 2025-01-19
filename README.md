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
    tellraw(message=JsonText("Hello TellRaw!", color="gold"))
    print(playsound("minecraft:entity.player.levelup", target="Falsw"))
    vtlr = titler()
    vtlr.title(JsonText("Welcome to", color="green", bold=True) + " " + JsonText("Minecraft", color="gold", bold=True))
    vtlr.subtitle(JsonText("A Python library for RCON", color="aqua"))
    vtlr.run()
    vtlr.actionbar(JsonText("Little is cute!", color="red", bold=True, italic=True))
    vtlr.run()
# Automatically closes the connection
```