# 2048
Systems Imp Group Project

# Handover

### Joe - 26/02

Uploaded a scores file. This can be used by calling either the random or human player. This calculates a normalised score (between 0 and 1) at the end of each move based upon.

- penalty for actions which do not increase the score

- reward for every increase in total score

- reward for creating more empty cells

- reward for bringing tiles of the same value closer together

- reward for placing tiles near the edges or corners 

- reward for every new highest tile found

- reward for getting to 2048

Decided not to incorporate this into the existing code in case there's anything we want to change in terms of the reward calculation (likely this can be further optimised). Once we've decided this though we can then move on to implementing a strategy/building the NN.

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




