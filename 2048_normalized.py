import random
import getopt
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

# Calculate reward function
def calculate_reward(mat, prev_mat, action, prev_score, prev_highest_tile):
    # Calculate the current total score
    current_score = sum([sum(row) for row in mat])

    # Find the highest tile in the current state
    current_highest_tile = max([max(row) for row in mat])

    # Initialize reward
    reward = 0

    # Check if total score increased
    if current_score > prev_score:
        reward += current_score - prev_score

    # Check if reached 2048
    if current_highest_tile == 2048:
        reward += 1000  # Reward for reaching 2048

    # Check if action did not increase the score
    if current_score <= prev_score:
        reward -= 0.5  # Penalty for not increasing the score

    # Reward for creating more empty cells
    num_empty_cells = sum(row.count(0) for row in mat)
    prev_num_empty_cells = sum(row.count(0) for row in prev_mat)
    reward += 0.05 * (num_empty_cells - prev_num_empty_cells)

    # Reward for bringing tiles of the same value closer together
    for i in range(4):
        for j in range(4):
            if mat[i][j] != 0:
                tile_value = mat[i][j]
                for dx, dy in [(1, 0), (0, 1)]:
                    x, y = i + dx, j + dy
                    if 0 <= x < 4 and 0 <= y < 4 and mat[x][y] == tile_value:
                        # Found a neighboring tile with the same value
                        reward += 0.1  # Reward for bringing tiles closer together

    # Reward for placing tiles near the edges or corners
    for i in range(4):
        for j in range(4):
            if mat[i][j] != 0:
                tile_value = mat[i][j]
                # Edge weighting
                if i == 0 or i == 3 or j == 0 or j == 3:
                    reward += 0.05  # Reward for tiles near the edges
                # Corner occupancy
                if (i == 0 or i == 3) and (j == 0 or j == 3):
                    reward += 0.25  # Reward for tiles in the corners

    # Scale the reward
    max_possible_reward = 1000  # Maximum possible reward when reaching 2048
    scaled_reward = reward / max_possible_reward

    return scaled_reward, current_score, current_highest_tile

# Calculate combined normalized value function
def calculate_combined_value(score, reward, weight_score, weight_reward):
    combined_value = score * weight_score + reward * weight_reward
    # Normalize the combined value if needed
    max_possible_combined_value = 1000 * weight_score + 1000 * weight_reward  # Assuming maximum score and reward
    normalized_combined_value = combined_value / max_possible_combined_value
    return normalized_combined_value

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
        combined_value = calculate_combined_value(score, reward, weight_score=0.1, weight_reward=0.9)
        print("Reward:", reward)
        print("Score:", score)
        print("Highest Tile:", highest_tile)
        print("Combined Value:", combined_value)
        print_grid(mat)

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
        combined_value = calculate_combined_value(score, reward, weight_score=0.1, weight_reward=0.9)
        print("Reward:", reward)
        print("Score:", score)
        print("Highest Tile:", highest_tile)
        print("Combined Value:", combined_value)
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

