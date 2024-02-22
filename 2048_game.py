import getopt
import random
import sys


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


# Main game loop for a human player
def main_human_player():
    mat = start_game()
    add_new(mat)
    print_grid(mat)
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
        add_new(mat)
        print_grid(mat)


# Main game loop for a random agent
# Main game loop for a random agent
def main_random_agent():
    mat = start_game()
    add_new(mat)
    print_grid(mat)
    while True:
        # Check if the game is over
        if not any(0 in row for row in mat):
            print("Game Over")
            break

        # Randomly select a move
        command = random.choice(['w', 'a', 's', 'd'])
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
        add_new(mat)
        print_grid(mat)


if __name__ == "__main__":

    # Define the command line arguments
    sys.argv = ['2048_test.py', "-p", "human"]

    opts, args = getopt.getopt(sys.argv[1:], "hp:",
                               ["help", "player="])
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
