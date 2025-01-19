# MCRconer
Run a bunch of commands with a simple python script through rcon!  

## Usage
Before using this library, you need to install the `mcrcon` package using pip:  
```bash
pip install mcrcon
```  
And Install the mc mod `BettterRcon` in your server.  
The mod is written by me, and it only avaiable for Fabric 1.20.1.  
But it is simple and you may write it yourself.  
*If you don't install the mod, it only causes issues on functions with the need of responses such as `list_players()` and `banner().list()` .*  
*So it's **OKAY to not install the mod**, but you won't be able to use these functions.*  

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