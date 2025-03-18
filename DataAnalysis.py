
import random
import time
from collections import Counter

# Initialize move history storage
player_move_history = []
ai_move_history = []

# Possible moves
moves = ["Rock", "Paper", "Scissors"]

def get_player_move():
    """Simulates player input."""

    move = random.choice(moves) # Simulate player move
    player_move_history.append(move) # Store move

    return move

def get_ai_move():
    """Chooses AI move."""

    move = random.choice(moves)
    ai_move_history.append(move)

    return moves

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

    transitions = []
    for i in range(len(player_move_history) - 1):
        prev_move = player_move_history[i]
        next_move = player_move_history[i+1]
        transitions.append((prev_move, next_move))
    
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



# Play multiple rounds
for round_number in range(10): # Simulate 10 rounds
    time.sleep(1)
    player_move = get_player_move()
    ai_move = get_ai_move()
    result = determine_winner(player_move, ai_move)

    print(f"Round {round_number+1}: Player chose {player_move}, AI chose {ai_move} -> {result}")

analyze_move_frequencies()
dectect_player_move_sequences()

# Predict the next move based on history
predicted_move = predict_next_move(player_move_history)
print(f"\n AI Predicts Player Will Choose: {predicted_move}")
ai_smart_move = get_smart_ai_move(player_move_history)
print(f"AI Chooses: {ai_smart_move} (to counter predicted move)")