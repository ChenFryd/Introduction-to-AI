import random

import heuristics
from game_engine import player_agent_heuristics
import alpha_beta_isolation, heuristic_alpha_beta_isolation_edit, heuristics
import numpy as np
from game_state import game_state
import matplotlib.pyplot as plt

strategies = {
    "base_heuristic": heuristics.base_heuristic,
    "simple": heuristics.simple,
    "defensive": heuristics.defensive,
    "defensive_abs": heuristics.defensive_abs,
    "offensive": heuristics.offensive,
    "offensive_abs": heuristics.offensive_abs,
    "walls": heuristics.walls,
    "walls_abs": heuristics.walls_abs,
    "defensive_to_offensive": heuristics.defensive_to_offensive,
    "defensive_to_offensive_abs": heuristics.defensive_to_offensive_abs,
    "offensive_to_defensive": heuristics.offensive_to_defensive,
    "offensive_to_defensive_abs": heuristics.offensive_to_defensive_abs,
}

def multi_strategy_simulation(number_of_games= 100, depth=7, grid_height=7, grid_width=7):
    strategies_results = np.zeros((len(strategies), len(strategies)))
    simulations_counter = 0
    for i, (strategy_name_player_1, strategy_function_player_1) in enumerate(strategies.items()):
        for j, (strategy_name_player_2, strategy_function_player_2) in enumerate(strategies.items()):
            total_wins = 0

            for game_counter in range(number_of_games):

                result = play_with_heuristics(strategy_function_player_1, strategy_function_player_2, depth, depth, grid_height, grid_width)
                print("simulation:{0} game:{1}, {2} vs {3} - Winner: {4}".format(simulations_counter,game_counter,strategy_name_player_1, strategy_name_player_2, result))
                simulations_counter += 1
                if result == 1:
                    total_wins += 1

            strategies_results[i, j] = (total_wins / number_of_games) * 100
            print("{0} vs {1} - win precentage: {2}".format(strategy_name_player_1, strategy_name_player_2, strategies_results[i,j]))
    return strategies_results

def play_with_heuristics(heuristic_player_1, heuristic_player_2, depth_player_1, depth_player_2, grid_height, grid_width):

    player_1 = player_agent_heuristics(heuristic_alpha_beta_isolation.alphabeta_max_h, heuristic_player_1,
                                       depth_player_1)
    player_2 = player_agent_heuristics(heuristic_alpha_beta_isolation.alphabeta_min_h, heuristic_player_2,
                                       depth_player_2)
    grid = np.zeros((grid_height, grid_width), dtype=int)
    # Generate random coordinates for player 1
    player1_location = (random.randint(0, grid_height - 1), random.randint(0, grid_width - 1))

    # Generate random coordinates for player 2, ensuring it's not the same as player 1
    while True:
        player2_location = (random.randint(0, grid_height - 1), random.randint(0, grid_width - 1))
        if player2_location != player1_location:
            break
    init_state = game_state(grid, player1_location, player2_location, 1)
    return play_isolation(player_1, player_2, init_state)


def play_isolation(player_1, player_2, init_state):
    players = {1: player_1, 2: player_2}
    curr_player = player_1
    player_turn = 1
    curr_state = init_state
    while not curr_state.is_terminal():
        chosen_move = curr_player.get_next_move(curr_state)
        curr_state.apply_move(chosen_move)
        player_turn = curr_state.get_curr_player()
        curr_player = players[player_turn]
    return player_turn % 2 + 1

# Run the simulation
print("Started Simulation")
number_of_games = 30
depth = 4
grid_height = 5
grid_width = 5
win_percentages = multi_strategy_simulation(number_of_games, depth, grid_height, grid_width)
# Calculate the average of each row
row_averages = np.mean(win_percentages, axis=1)

# Add a new column with row averages
win_percentages_with_averages = np.column_stack((win_percentages, row_averages))

# Calculate the average of each column
column_averages = np.mean(win_percentages_with_averages, axis=0)

# Add a new row with column averages
win_percentages_with_averages_and_rows = np.vstack((win_percentages_with_averages, column_averages))

print(win_percentages_with_averages_and_rows)
# Strategies on x and y axes
x_strategies = y_strategies = list(strategies.keys()) +['Average']
plt.figure(figsize=(12, 10))

# Create a heatmap
plt.imshow(win_percentages_with_averages_and_rows, cmap='viridis', interpolation='nearest')
plt.colorbar(label='Win Percentage')

for i in range(len(y_strategies)):
    for j in range(len(x_strategies)):
        plt.text(j, i, f'{win_percentages_with_averages_and_rows[i, j]:.1f}%', ha='center', va='center', color='w', fontsize=10)

plt.xticks(np.arange(len(x_strategies)), x_strategies, rotation=90)
plt.yticks(np.arange(len(y_strategies)), y_strategies)
plt.xlabel('X Strategies')
plt.ylabel('Y Strategies')
plt.title(f'Win Percentage Heatmap, games per two strategies: {number_of_games}, depth: {depth}, grid size: {grid_height}x{grid_width}')
plt.show()

print("Simulation finished")