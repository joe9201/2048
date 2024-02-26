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

# Calculate the score
def calculate_score(mat):
    return sum([sum(row) for row in mat])

# Main game loop for a human player
def main_human_player():
    mat = start_game()
    add_new(mat)
    print_grid(mat)
    score = 0  # Initialize the score
    while True:
        command = input("Enter command (W/A/S/D or Q to quit): ").strip().lower()
        if command == 'q':
            print("Quitting the game. Thanks for playing!")
            break
        elif command == 'w':
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
        score = calculate_score(mat)
        print("Score:", score)
        print_grid(mat)

def main_random_agent():
    print("Executing main_random_agent()")
    mat = start_game()
    add_new(mat)
    print_grid(mat)
    score = 0  # Initialize the score
    while True:
        command = random.choice(['w', 'a', 's', 'd'])
        print("Random Agent's move:", command)  # Print the agent's move
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
        score = calculate_score(mat)
        print("Score:", score)
        print_grid(mat)

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




