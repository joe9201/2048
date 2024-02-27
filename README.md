# 2048
Systems Imp Group Project

# Handover

### Greg - 27/07

I have updated the script to print the button presses 'w','s','a','d' as 'Up', 'Down', 'Left', 'Right'.

I have also added code to convert the game state into a suitable format for input into a neural network. This is done by flattening the grid and then one-hot encoding the values. This is the 'encode_state" function, which provides a 2D list where each inner list represents the one-hot encoded version of a corresponding row in the original grid, which should be easily read by a neural network. 

### Joe - 26/02

Uploaded a normalized scores file. This can be used by calling either the random or human player. This calculates a normalised score (between 0 and 1) at the end of each move based upon.

- penalty for actions which do not increase the score

- reward for every increase in total score

- reward for creating more empty cells

- reward for bringing tiles of the same value closer together

- reward for placing tiles near the edges or corners 

- reward for every new highest tile found

- reward for getting to 2048

The reward and total score are then combined and normalized to a value between 0 and 1.   

Decided not to incorporate this into the existing code in case there's anything we want to change in terms of the reward calculation (likely this can be further optimised). Once we've decided this though we can then move on to implementing more strategy or building the NN.

### Eloise - 25/02/2024
Today I looked at trying to get a version of 2048 with a screen display working, which I did - I chose visual studio code as my IDE.

I then used trusty ol’ GPT to help me understand the best way to attack either using this code (or the original text code from Elle and Greg) how to implement Q-learning.  
https://chat.openai.com/share/99395bf4-7131-4999-914e-e6f37c3e46ed 
From what I could understand, it was suggesting that due to the amount of state space for the code from lewisjdeanes is quite large, almost too large to implement using a q-learning technique however this is where it suggests deep q-learning is a better idea to go down.

For the original code from Elle and Greg, Chatgpt suggests similar things but instead of deep q-learning it suggests that the state space can be simplified by reducing the state space by grouping similar values together or by focusing on certain key features of the state (e.g., highest value tile, number of empty cells).

I looked into https://pythonprogramming.net/q-learning-analysis-reinforcement-learning-python-tutorial/ to understand what we can do with our data and understand how to display said data; For the end result of the project do we need to demonstrate the learning agent actually playing the game to the best of its ability or just display the data?

the 2048.py file and the constants.py work together to form the working visual version of the 2048 game

### Elly - 22/02/2024

Modified the existing 2048 text based game to include a human player and a “random” player which chooses randomly selected moves to play the game 

**Rationale** - we already have the game written in simple python code to reduce computational issues that would arise from implementing the GUI version of the game. Our goal is to sense check if the 2048 environment will allow for an agent to play the game. 

**Architectural design** - utilised code from data and text module to allow the option to select between a human and a random agent as a player. There are now two methods in the game “def main_human_player():” and “def main_random_agent(): whereby the human one accepts input for the actions and the random agent selects actions at random. 

The “main” code at the bottom includes the option to select either a human or random player when executing the code in the terminal.

the command in terminal to play as human is:

python 2048_game.py -p "human" 

the common to play as random agent is:

python 2048_game.py -p "random"

A "check valid moves" function was also implemented to check if there are any remaining cells available - required as otherwise the random agent gets stuck in an infinite loop. 

**Implementation** - utilise the terminal to select between the two “players” and access the different play functions 

**Performance evaluation** - the two options work as their supposed to, however the random agent isn't very clever, as it only knows random moves even if there is a valid move (such as adjacent tiles - see debugging file last move) it will not make it. 

**Issues** - we could adapt the random agent to be smarter and include logic where it will make a specific move if there are adjacent tiles, however as the endeavour was to implement an agent into the game, this may be reduant and better to move on to a learning agent with this ability required in mind.

it may be better to seperate the main functions (matrix builder, humans player, random player) into seperate files and call them as external methods. 

could also make the printing of the random agents moves clearer, as two of the matrixes are currently doubled up. 

**Next steps** - 

Something to consider (and ask supervisor) is whether the text based version is a fair test of performance, if we are evaluating against human players who played on the GUI version. 

Also to conduct further research in utilising TF Agents - https://www.tensorflow.org/agents which is a reinforcement library for tensorflow

**References**

- Systems Import code - Markey Gyaz
- random_player_agent function and stopping criteria function - Chat GPT




