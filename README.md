iSolo uses a 3 layer architecture to demonstrate a computer-based gamemaster for a nonspecific roleplaying game.
The idea is that your computer manages a database of game states. Each game state corresponds to a turn for a particular character played by a specific player. You can also create a new player and character. The new character gets added to the database of manageable game states. The application examines each game state, and gives the user the opportunity to add two secrets to a generic game state thus making a unique game state. The computerized GM then randomizes character actions and their success. The computerized GM then filters the game state to produce a filtered game state that the player "can be" presented with. If there was a user interface for the player, that filtered game state would be rendered on that UI. The filtered game state represents what the player knows. The game state represents the truth. It is up to the computerized GM to keep track of both game states for each character turn. The filtered game state is created according to a set of rules devised by myself. These rules don't conform to a specific roleplaying game, but they are inspired by the Pathfinder roleplaying game. My favorite!!!

*run GUI.py to see the demonstration.
*For best results, refresh the database each time you run the demonstration. You can refresh it by running states_of_games_DB.sql
in workbench.

GUI = Graphical User Interface
BLL = Business Logic Layer
DAL = Data Access Layers

PYTHON DEPENDENCIES: Internal and External
mysql.connector
tkinter
datetime
random
decimal
logging

SETUP:
Go to the command prompt and navigate to the folder where the application files are located on your computer.
Use the requirements.txt file to install the dependencies by entering the following command: pip install -r requirements.txt

RUNNING THE DEMONSTRATION:
Run the following command at the command prompt within the folder where the application files are located: GUI.py
You should have MySQL workbench installed on your computer, and you should have a valid login and password for workbench.
You should also have python installed on your computer. This application is written in the python programming language.

FILTERED GAME STATE RULES:

All Game states have the following fields:

system_date
character_ID
turn
starvation_mode
subsistence_level
condition1
condition2
affliction1
affliction2
secret_doors
secret_traps
secret_treasure
secret_cursed_treasure
secret_airborne_disease
secret_poison_gas
overland_speed

Starvation mode is designated as a 0 or 1. 0 means off, and 1 means on.

subsistence level is 'poor', 'fair', or 'good' it represents the character's wealth. Poor sets the starvation mode to 1. That means the
character is starving. Whenever starvation mode is 1 and subsistence level is poor, the character's overland speed is reduced to 13.3 miles/Day. When starvation mode is 0, that corresponds to a 'fair' or 'good' subsistence level. Fair and good each cumulatively add 0.5 miles/day to the character's overland speed.

Overland Speed: The default Overland speed is 15.5 miles/day when a character starts with subsistence level is fair or good. Increasing your subsistence level always increases overland speed by 0.5 miles/day. If a character starts with a poor subsistence level then their
overland speed will be set to 13.3 miles/day.

conditions: The character is limited to two simultaneous conditions. If the character does not find a trap, then it activates. They gain the bleeding condition as a result. If the character fails to discover that the treasure is cursed, then they gain the vampirism condition. If the character fails to discover airborne disease, then they are exhausted. If the character fails to discover poison gas, then they are sickened.

Afflictions: The character is limited to two simultaneous afflictions. Afflictions are never revealed to the character in the filtered game state unless the player specifically searches for them and successfully finds them. The three types of afflictions are curse, disease, and poison.

Secret Doors: Only revealed to the player if the search for them and find them.
Secret Traps: Always revealed to the player either because they didn't find them and they accidently set them off or they did find them
but they didn't set them off.

Secret Treasure: This increases a character's subsistence level if successfully found. That will in turn increase their overland speed.
Secret Cursed Treasure: This treasure turns the character into a vampire unless they specifically search for it and find it.

Secret Airborne Disease: This inflicts the character with a disease unless they specifically search for it and find it.
Secret Poison Gas: This inflicts the character with poison unless they specifically search for it and find it.

Note: this is not intended to be a game. It is merely a demonstration of how a computerized gm can manage game states and keep secrets from the player until they discover those secrets. It is a proof of concept. The concept is that a computer can act as a gamemaster for
a solo roleplayer. An actual game built off of this concept would play and feel like a table top roleplaying game. Not a video game.
It would be turn-based and immersive. Such a game would use an AI LLM as a narrator only to make GM-Player interactions seem more
human-like. That adds immersion to the experience.

The filter that creates the filtered game state from a game state is an advanced feature. I wanted to create such a filter because it is at the heart of creating a game that acts like a human gamemaster. The filter is implemented in both the GUI and the BLL. The logic of the filter is handled by the BLL. The GUI ensures that that the BLL has proper constraints to work with by limiting user inputs. My
biggest takeaway from this experience is the observation of how quickly an application becomes complex during development. This
perspective is very humbling, but helps cement software development limitations in the real world.



 
