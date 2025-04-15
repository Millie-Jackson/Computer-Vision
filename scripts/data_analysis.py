
import random
import csv
import os
import pandas as pd
from collections import Counter

# Initialize move history storage
player_move_history = []
ai_move_history = []

# Possible moves
moves = ["Rock", "Paper", "Scissors"]



def determine_winner(player, ai):
    """Decides the winner based on game rules."""

    if player == ai:
        return "Draw"
    if (player == "Rock" and ai == "Scissors") or (player == "Paper" and ai == "Rock") or (player == "Scissors" and ai == "Paper"):
        return "Player Wins"
    return "AI Wins"

def analyze_move_frequencies():
    """Analyzes how often the player chooses each move."""

    move_counts = Counter(player_move_history)
    total_moves = len(player_move_history)

    if total_moves == 0:
        return "No moves played yet."
    
    print("\n Player Move Frequency:")
    for move, count in move_counts.items():
        percentage = (count / total_moves) * 100
        print(f"{move}: {count} times ({percentage:.1f}%)")

def dectect_player_move_sequences():
    """Identifies common move transitions"""

    transitions = [(player_move_history[i], player_move_history[i+1]) for i in range(len(player_move_history) - 1)]
    
    transitions_counts = Counter(transitions)
    print("\n Common Player Move Sequences:")
    for transition, count in transitions_counts.most_common():
        print(f"{transition[0]} -> {transition[1]} : {count} times")

def predict_next_move(player_move_history):
    """Predicts the player's next move based on history"""

    if len(player_move_history) < 2:
        return random.choice(moves) # Not enough data -> choose randomly
    
    # Get last move
    last_move = player_move_history[-1]

    # Count transitions from the last move
    transitions = Counter([(player_move_history[i], player_move_history[i+1]) for i in range(len(player_move_history) - 1)])

    # Find the most common move following the last move
    possible_next_moves = {move: count for (prev, move), count in transitions.items() if prev == last_move}

    if not possible_next_moves:
        return random.choice(moves) # No trend detected -> choose randomly
    
    predicted_move = max(possible_next_moves, key=possible_next_moves.get)
    return predicted_move

def get_smart_ai_move(player_move_history):
    """AI selects the best move based on predicted player move."""

    predicted_player_move = predict_next_move(player_move_history)

    # Choose the best counter move
    counter_moves = {
        "Rock": "Paper",
        "Paper": "Scissors",
        "Scissors": "Rock"
    }

    return counter_moves.get(predicted_player_move, random.choice(moves)) # Default to random move

def analyze_player_patterns(player_move_history):
    """Analyzes player's decision patterns over time."""

    if not player_move_history:
        return "No moves recorded."
    
    move_counts = Counter(player_move_history)
    most_common = move_counts.most_common(1)
    transition_counts = Counter(zip(player_move_history[:-1], player_move_history[1:]))
    most_common_transition = transition_counts.most_common(1)

    analysis_results = []
    analysis_results.append("\n Player Move Analysis:")
    for move, count in move_counts.items():
        analysis_results.append(f"{move}: {count} times")

    if most_common:
        analysis_results.append(f"Most frequently played move: {most_common[0][0]} ({most_common[0][1]} times)")
    if most_common_transition:
        analysis_results.append(f"Most common move sequence: {most_common_transition[0][0][0]} -> {most_common_transition[0][0][1]} ({most_common_transition[0][1]} times)")

    return "\n".join(analysis_results)

def save_moves_to_csv(player_moves, ai_moves, results, filename="game_moves.csv"):
    """Appends player and AI moves to a CSV file for later analysis"""

    # Check if file exists
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)

        # Write headers only if it is a new file
        if not file_exists:
            writer.writerow(["Round", "Player Move", "AI Move", "Result"])

        for i, (player, ai, result) in enumerate(zip(player_moves, ai_moves, results), start=1):
            writer.writerow([i, player, ai, result])

    print(f"\n Moves appended to {filename} successfully!")

def display_moves_as_dataframe(player_moves, ai_moves):
    """Displays game moves as a Pandas DataFrame"""

    df = pd.DataFrame({"Round": list(range(1, len(player_moves) + 1)),
                        "Player Move": player_moves,
                        "AI Move": ai_moves})
    
    print("\n Game Move History:\n")
    print(df)

    return df # Return for further analysis

def check_dataset_size(filename="game_moves.csv"):
    """Loads the csv and displays how many rounds are recorded"""

    # Check if the file exists
    if not os.path.isfile(filename):
        print("\n No dataset found.")
        return
    
    # Check if the file is empty
    if os.stat(filename).st_size == 0:
        print("\n The data set is empty.")
        return

    try:
        df = pd.read_csv(filename)
        print(f"\n Total Rounds Recorded: {len(df)}")
    except pd.errors.EmptyDataError:
        print("\n The Dataset exists but is empty.")

def calculate_ai_win_rate(results):
    """Calculates win rate"""

    total = len(results)
    counts = Counter(results)
    ai_wins = counts.get("AI Wins", 0)
    win_rate = (ai_wins /  total) * 100 if total > 0 else 0
    print(f"\n AI Win Rate: {win_rate:.1f}% ({ai_wins}/{total} rounds)")



analyze_move_frequencies()
dectect_player_move_sequences()

# Predict the next move based on history
predicted_move = predict_next_move(player_move_history)
print(f"\n AI Predicts Player Will Choose: {predicted_move}")
ai_smart_move = get_smart_ai_move(player_move_history)
print(f"AI Chooses: {ai_smart_move} (to counter predicted move)")

print (f"Dataset size: ", player_move_history)