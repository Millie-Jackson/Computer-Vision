# scripts/generate_test_data.py



import random
import pandas as pd
import os
from collections import deque



# Ensure the data folder exists
os.makedirs("data", exist_ok=True)

# Possible moves
moves = ["Rock", "Paper", "Scissors"]
beats = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}
counter = {"Rock": "Paper", "Paper": "Scissors", "Scissors": "Rock"}


# Simulated data storage
total_rounds = 100
round_numbers = []
player_moves = []
ai_moves = []
results = []

''' Patterned player stratergy:
 - Starts with Rock
 - After a loss: rotate to next move (rock->paper->scissors)
 - Sometimes goes random (20%) '''

# Patterns for simulation
player_pattern = deque(moves)
last_result = None

#ai_bias = {"Rock": 0.4, "Paper": 0.3, "Scissors": 0.3}  # AI favors Rock

for i in range(total_rounds):
    round_num = i + 1

    # Choose player move
    if last_result == "AI Wins":
        player_pattern.rotate(-1)
        player_move = player_pattern[0]
    else:
        player_move = player_pattern[0] if random.random() > 0.2 else random.choice(moves)

    # Choose AI move (tries to counter player 70% of time)
    ai_move = counter[player_move] if random.random() > 0.3 else random.choice(moves)

    # Determine winner
    if player_move == ai_move:
        result = "Draw"
    elif beats[player_move] == ai_move:
        result = "Player Wins"
    else:
        result = "AI Wins"

    # Store everything
    round_numbers.append(round_num)
    player_moves.append(player_move)
    ai_moves.append(ai_move)
    results.append(result)
    last_result = result

# Create DataFrame
df_simulated = pd.DataFrame({
    "Round": round_numbers,
    "Player Move": player_moves,
    "AI Move": ai_moves,
    "Result": results
})

# Save to CSV
df_simulated.to_csv("data/simulated_game_moves_for_testing.csv", index=False)
print("Simulated test dataset saved")



# END OF FILE