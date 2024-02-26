import getopt
import random
import sys
from math import log2

# Initialize the 4x4 grid
def start_game():
    mat = [[0] * 4 for _ in range(4)]
    return mat

# Add a new 2 or 4 to an empty cell
def add_new(mat):
    r, c = random.randint(0, 3), random.randint(0, 3)
    while mat[r][c] != 0:
        r, c = random.randint(0, 3), random.randint(0, 3)
    mat[r][c] = random.choice([2, 4])

# Perform a left swipe
def compress(mat):
    new_mat = [[0] * 4 for _ in range(4)]
    for i in range(4):
        pos = 0
        for j in range(4):
            if mat[i][j] != 0:
                new_mat[i][pos] = mat[i][j]
                pos += 1
    return new_mat

# Merge identical cells after a left swipe
def merge(mat):
    for i in range(4):
        for j in range(3):
            if mat[i][j] == mat[i][j + 1] and mat[i][j] != 0:
                mat[i][j] *= 2
                mat[i][j + 1] = 0
    return mat

# Reverse the matrix (for right swipe)
def reverse(mat):
    new_mat = [row[::-1] for row in mat]
    return new_mat

# Transpose the matrix (for up and down swipes)
def transpose(mat):
    new_mat = [[0] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            new_mat[i][j] = mat[j][i]
    return new_mat

# Display the grid
def print_grid(mat):
    for row in mat:
        print(row)
    print()  # Add an empty line after printing the grid

# Function to check if there are any valid moves left
def check_valid_moves(mat):
    # Check if there are any empty cells
    for i in range(4):
        for j in range(4):
            if mat[i][j] == 0:
                return True
    return False

# Calculate reward function
def calculate_reward(mat, prev_mat, action, prev_score, prev_highest_tile):
    # Calculate the current total score
    current_score = sum([sum(row) for row in mat])

    # Find the highest tile in the current state
    current_highest_tile = max([max(row) for row in mat])

    # Initialize reward
    reward = 0

    # Check if total score increased
    score_increase = current_score - prev_score
    reward += score_increase

    # Check if new highest tile found
    if current_highest_tile > prev_highest_tile:
        # Reward for new highest tile
        reward += 50  # Adjust as needed

    # Check if reached 2048
    if current_highest_tile == 2048:
        reward += 1000  # Reward for reaching 2048

    # Penalty for actions not increasing the score
    if score_increase <= 0:
        reward -= 10  # Penalty for actions not increasing the score

    return reward, current_score, current_highest_tile


# Main game loop for a human player
def main_human_player():
    mat = start_game()
    add_new(mat)
    print_grid(mat)
    score = 0  # Initialize the score
    prev_mat = None
    prev_score = 0
    prev_highest_tile = 0
    while True:
        command = input("Enter command (W/A/S/D or Q to quit): ").strip().lower()
        if command == 'q':
            print("Quitting the game. Thanks for playing!")
            break
        prev_mat = [row[:] for row in mat]
        prev_score = score
        prev_highest_tile = max([max(row) for row in mat])

        if command == 'w':
            mat = transpose(mat)
            mat = compress(mat)
            mat = merge(mat)
            mat = compress(mat)
            mat = transpose(mat)
        elif command == 's':
            mat = transpose(mat)
            mat = reverse(mat)
            mat = compress(mat)
            mat = merge(mat)
            mat = compress(mat)
            mat = reverse(mat)
            mat = transpose(mat)
        elif command == 'a':
            mat = compress(mat)
            mat = merge(mat)
            mat = compress(mat)
        elif command == 'd':
            mat = reverse(mat)
            mat = compress(mat)
            mat = merge(mat)
            mat = compress(mat)
            mat = reverse(mat)
        else:
            print("Invalid command. Use W/A/S/D to move or Q to quit.")
            continue

        if not check_valid_moves(mat):
            print("Game over! No more valid moves.")
            break

        add_new(mat)
        reward, score, highest_tile = calculate_reward(mat, prev_mat, command, prev_score, prev_highest_tile)
        print("Reward:", reward)
        print("Score:", score)
        print("Highest Tile:", highest_tile)
        print_grid(mat)

    # Print total reward, total score, and highest tile achieved
    print("Total Reward:", score)
    print("Total Score:", score)
    print("Highest Tile Achieved:", highest_tile)

# Main game loop for a random agent
def main_random_agent():
    print("Executing main_random_agent()")
    mat = start_game()
    add_new(mat)
    print_grid(mat)
    score = 0  # Initialize the score
    prev_mat = None
    prev_score = 0
    prev_highest_tile = 0
    while True:
        command = random.choice(['w', 'a', 's', 'd'])
        print("Random Agent's move:", command)  # Print the agent's move
        prev_mat = [row[:] for row in mat]
        prev_score = score
        prev_highest_tile = max([max(row) for row in mat])

        if command == 'w':
            mat = transpose(mat)
            mat = compress(mat)
            mat = merge(mat)
            mat = compress(mat)
            mat = transpose(mat)
        elif command == 's':
            mat = transpose(mat)
            mat = reverse(mat)
            mat = compress(mat)
            mat = merge(mat)
            mat = compress(mat)
            mat = reverse(mat)
            mat = transpose(mat)
        elif command == 'a':
            mat = compress(mat)
            mat = merge(mat)
            mat = compress(mat)
        elif command == 'd':
            mat = reverse(mat)
            mat = compress(mat)
            mat = merge(mat)
            mat = compress(mat)
            mat = reverse(mat)

        if not check_valid_moves(mat):
            print("Game over! No more valid moves.")
            break

        add_new(mat)
        reward, score, highest_tile = calculate_reward(mat, prev_mat, command, prev_score, prev_highest_tile)
        print("Reward:", reward)
        print("Score:", score)
        print("Highest Tile:", highest_tile)
        print_grid(mat)

    # Print total reward, total score, and highest tile achieved
    print("Total Reward:", score)
    print("Total Score:", score)
    print("Highest Tile Achieved:", highest_tile)

if __name__ == "__main__":
    # Define the command line arguments
    opts, args = getopt.getopt(sys.argv[1:], "hp:", ["help", "player="])
    player = None  # Initialise the player variable

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("Usage: 2048_test.py --player [human|random]")
            sys.exit()
        elif opt in ("-p", "--player"):
            player = arg

    if player == "human":
        main_human_player()
    elif player == "random":
        main_random_agent()
