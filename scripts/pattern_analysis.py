# PatternAnalysis.py

import pandas as pd
import logging
from collections import Counter
from itertools import groupby


logging.basicConfig(
    filename='logs/pattern_analysis.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
    level=logging.INFO
)

def load_game_data(filename="data/game_moves.csv"):
    """Load the dataset"""

    logging.info("Function: load_game_data")
    try:
        df = pd.read_csv(filename)
        logging.info(f"\n Loaded {len(df)} rounds from {filename}")
        return df
    except FileNotFoundError:
        logging.info("\n File not found.")
        return pd.DataFrame()
    
def analyze_move_frequencies(df):
    """Move frequencies"""

    logging.info("Function: analyze_move_frequencies")
    logging.info("\n Move Frequencies:")
    logging.info(df[['Player Move', 'AI Move']].apply(pd.Series.value_counts))

def analyze_result_streaks(results):
    """Win/loss streaks"""

    logging.info("Function: analyze_result_streaks")
    streaks = [(k, sum(1 for _ in g)) for k, g in groupby(results)]
    logging.info("\n Result Streaks (in order):")
    for outcome, length in streaks:
        logging.info(f"{outcome}: {length} rounds")

def analyze_move_transitions(moves):
    """Transition analysis"""

    logging.info("Function: analyze_move_transitions")
    transitions = [(moves[i], moves[i+1]) for i in range(len(moves)-1)]
    transition_counts = Counter(transitions)
    logging.info("\n Common Move Transitions:")
    for (prev, nxt), count in transition_counts.most_common():
        logging.info(f"{prev} -> {nxt}: {count} times")

def analyze_sequential_patterns(moves, pattern_length=3):
    """Sequantial patterns (3-move cycles)"""

    logging.info(f"Function: analyze_sequential_patterns with pattern_length={pattern_length}")
    patterns = [tuple(moves[i:i+pattern_length]) for i in range(len(moves) - pattern_length + 1)]
    pattern_counts = Counter(patterns)
    logging.info(f"\n Detected {pattern_length}-Move Patterns:")
    for pattern, count in pattern_counts.most_common():
        if count > 1:
            logging.info(f"{' -> '.join(pattern)}: {count} times")

def analyze_player_tendencies(df):
    """Player tendencies"""

    logging.info("Function: analyze_player_tendencies")
    logging.info("\n Player Tendencies:")
    logging.info(f"Most common opening move: {df['Player Move'].iloc[0]}")

    responses = Counter()
    for i in range(1, len(df)):
        prev_result = df['Result'].iloc[i-1]
        curr_move = df['Player Move'].iloc[i]
        responses[(prev_result, curr_move)] += 1

    logging.info ("\n Player responses to previous round result:")
    for (prev_result, move), count in responses.most_common():
        logging.info(f"After '{prev_result}', played '{move}': {count} times")

def run_full_analysis():
    """Run everything"""

    logging.info("Function: run_full_analysis")
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