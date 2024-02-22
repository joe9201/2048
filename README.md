# 2048
Systems Imp Group Project

# Handover

### Elly - 22/02/2024

Attempted to modify the existing 2048 text based game to include a human player and a “random” player which chooses randomly selected moves to play the game 

**Rationale** - we already have the game written in simple python code to reduce computational issues that would arise from implementing the GUI version of the game 

**Architectural design** - utilised code from data and text module to allow the option to select between a human and a random agent as a player. There are now two methods in the game “def main_human_player():” and “def main_random_agent(): whereby the human one accepts input for the actions and the random agent selects actions at random. 

The “main” code at the bottom includes the option to select either a human or random player when executing the code in the terminal.

the command in terminal to play as human is:

python 2048_game.py -p "human" 

the common to play as random agent is:

python 2048_game.py -p "random"

Included functions to check if there are any valid moves left and  to terminate the game, otherwise the random player continues to play, excessive computational power, this function is currently not working

In the debugging file, we can see that in the final matrix, there is a valid move (the two 16s adjacent to each other) need to implement logic for the random agent to choose moves when there are ajacent tiles, as the current function to check if move valid accounts for this 

**Implementation** - utilise the terminal to select between the two “players” and access the different play functions 

**Performance evaluation** - the two options work, currently too much computation when running random, it was getting stuck in an infinite loop. 

**Issues** - as above, need to sense check why it’s getting stuck in an infinite loop 

**Next steps** - 

Need to stop the random agents infinite loop 

Something to consider (and ask supervisor) is whether the text based version is a fair test of performance, if we are evaluating against human players who played on the GUI version. 

Also to conduct further research in utilising TF Agents - https://www.tensorflow.org/agents which is a reinforcement library for tensorflow

Also to check with supervisor, whether its worth dividing the separate functions (i.e. making the matrix, human player, random player) into separate python files which are called as external methods, or if it should all be kept in the same python file 




