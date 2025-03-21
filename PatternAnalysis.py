# PatternAnalysis.py

import pandas as pd
from collections import Counter
from itertools import groupby



def load_game_data(filename="game_moves.csv"):
    """Load the dataset"""

    try:
        df = pd.read_csv(filename)
        print(f"\n Loaded {len(df)} rounds from {filename}")
        return df
    except FileNotFoundError:
        print("\n File not found.")
        return pd.DataFrame()
    
def analyze_move_frequencies(df):
    """Move frequencies"""

    print("\n Move Frequencies:")
    print(df[['Player Move', 'AI Move']].apply(pd.Series.value_counts))

def analyze_result_streaks(results):
    """Win/loss streaks"""

    streaks = [(k, sum(1 for _ in g)) for k, g in groupby(results)]
    print("\n Result Streaks (in order):")
    for outcome, length in streaks:
        print(f"{outcome}: {length} rounds")

def analyze_move_transitions(moves):
    """Transition analysis"""

    transitions = [(moves[i], moves[i+1]) for i in range(len(moves)-1)]
    transition_counts = Counter(transitions)
    print("\n Common Move Transitions:")
    for (prev, nxt), count in transition_counts.most_common():
        print(f"{prev} -> {nxt}: {count} times")

def analyze_sequential_patterns(moves, pattern_length=3):
    """Sequantial patterns (3-move cycles)"""

    patterns = [tuple(moves[i:i+pattern_length]) for i in range(len(moves) - pattern_length + 1)]
    pattern_counts = Counter(patterns)
    print(f"\n Detected {pattern_length}-Move Patterns:")
    for pattern, count in pattern_counts.most_common():
        if count > 1:
            print(f"{' -> '.join(pattern)}: {count} times")

def analyze_player_tendencies(df):
    """Player tendencies"""

    print("\n Player Tendencies:")
    print(f"Most common opening move: {df['Player Move'].iloc[0]}")

    responses = Counter()
    for i in range(1, len(df)):
        prev_result = df['Result'].iloc[i-1]
        curr_move = df['Player Move'].iloc[i]
        responses[(prev_result, curr_move)] += 1

    print ("\n Player responses to previous round result:")
    for (prev_result, move), count in responses.most_common():
        print(f"After '{prev_result}', played '{move}': {count} times")

def run_full_analysis():
    """Run everything"""

    df = load_game_data()
    if df.empty:
        return
    
    analyze_move_frequencies(df)
    analyze_result_streaks(df['Result'].tolist())
    analyze_move_transitions(df['Player Move'].tolist())
    analyze_sequential_patterns(df['Player Move'].tolist())
    analyze_player_tendencies(df)



if __name__ == "__main__":

    run_full_analysis()