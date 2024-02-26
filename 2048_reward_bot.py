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
    if current_score > prev_score:
        reward += current_score - prev_score

    # Check if new highest tile found
    if current_highest_tile > prev_highest_tile:
        # Calculate the discounted reward for new highest tile
        highest_tile_reward = 0.1 * log2(current_highest_tile)  # Adjust the discount factor as needed
        reward += highest_tile_reward

    # Check if reached 2048
    if current_highest_tile == 2048:
        reward += 1000  # Reward for reaching 2048

    # Check if action did not increase the score
    if current_score <= prev_score:
        reward -= 0.5  # Penalty for actions not increasing the score

    return reward, current_score, current_highest_tile

# Reward bot function
def reward_bot(mat, prev_mat, action, prev_score, prev_highest_tile):
    print("Reward_bot's move:", action)
    if action == 'w':
        mat = transpose(mat)
        mat = compress(mat)
        mat = merge(mat)
        mat = compress(mat)
        mat = transpose(mat)
    elif action == 's':
        mat = transpose(mat)
        mat = reverse(mat)
        mat = compress(mat)
        mat = merge(mat)
        mat = compress(mat)
        mat = reverse(mat)
        mat = transpose(mat)
    elif action == 'a':
        mat = compress(mat)
        mat = merge(mat)
        mat = compress(mat)
    elif action == 'd':
        mat = reverse(mat)
        mat = compress(mat)
        mat = merge(mat)
        mat = compress(mat)
        mat = reverse(mat)

    reward, current_score, current_highest_tile = calculate_reward(mat, prev_mat, action, prev_score, prev_highest_tile)
    print("Reward:", reward)  # Print the reward for the action taken
    
    return mat, reward, current_score, current_highest_tile

# Main reward bot loop
def main_reward_bot():
    mat = start_game()
    add_new(mat)
    print_grid(mat)
    prev_mat = None  # Store the previous state of the board
    prev_score = 0   # Store the previous score
    prev_highest_tile = 0   # Store the previous highest tile
    while True:
        action = random.choice(['w', 'a', 's', 'd'])
        prev_mat = [row[:] for row in mat]  # Save the current state before taking action
        mat, reward, current_score, current_highest_tile = reward_bot(mat, prev_mat, action, prev_score, prev_highest_tile)
        print_grid(mat)  # Print the grid after the bot's move

        if not check_valid_moves(mat):
            print("Game over! No more valid moves.")
            break

        add_new(mat)
        prev_score = current_score
        prev_highest_tile = current_highest_tile
    

