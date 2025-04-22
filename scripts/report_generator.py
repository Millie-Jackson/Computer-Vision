# report_generator.py



import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from itertools import groupby
from matplotlib.backends.backend_pdf import PdfPages
import os
from datetime import datetime
import textwrap



sns.set(style="whitegrid")

# Test data or normal data
#data_file = "data/game_moves.csv"
data_file = "data/simulated_game_moves_for_testing.csv"

def load_data(filename=data_file):
    """Loads data"""

    if not os.path.exists(filename):
        raise FileNotFoundError("No data found")
    
    return pd.read_csv(filename)

def get_outcome_stats(df):
    """Basic stats"""

    outcome_counts = df['Result'].value_counts()

    return outcome_counts

def win_rate_per_move(df):
    """Win % per move"""

    move_win_counts = df[df['Result'] == 'Player Wins']['Player Move'].value_counts()
    move_total_counts = df['Player Move'].value_counts()
    win_rates = (move_win_counts / move_total_counts).fillna(0) * 100

    return win_rates.round(1)

def get_streaks(results):
    """Streak analysis"""

    return [(key, sum(1 for _ in group)) for key, group in groupby(results)]

def ensure_reports_folder():
    """Ensures reports are placed into a folder"""

    if not os.path.exists("reports"):
        os.makedirs("reports")

def cleanup_old_charts():
    """Removes out of date charts"""

    for fname in ["outcome.png", "winrate.png", "start_end.png"]:
        if os.path.exists(fname):
            os.remove(fname)

def plot_outcome_distribution(df, save_path):
    """Plot outcome distributions"""

    plt.figure(figsize=(6, 4))
    outcome_counts = get_outcome_stats(df)
    sns.barplot(x=outcome_counts.index, y=outcome_counts.values, palette="Set2")
    plt.title("Game Outcomes")
    plt.ylabel("Count")
    plt.xlabel("Outcome")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_winrate_by_move(df, save_path):
    """Plots win rate per move"""

    win_rates = win_rate_per_move(df)
    plt.figure(figsize=(6, 4))
    sns.barplot(x=win_rates.index, y=win_rates.values, palette="coolwarm")
    plt.title("Player Win Rate by Move")
    plt.ylabel("Win Rate (%)")
    plt.xlabel("Move")
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_start_vs_end(df, save_path):
    """Plot start vs end performance"""

    third = len(df) // 3
    start = df.iloc[:third]
    end = df.iloc[-third:]

    start_win = start['Result'].value_counts(normalize=True) * 100
    end_win = end['Result'].value_counts(normalize=True)

    data = pd.DataFrame({'Start': start_win, 'End': end_win}).fillna(0)
    data = data.T

    data.plot(kind='bar', figsize=(6, 4), color=["#4CAF50", "#F44336", "#9E9E9E"])
    plt.title("Start VS End Performance")
    plt.ylabel("Percentage")
    plt.xlabel("Game Phase")
    plt.legend(title="Results")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()



def generate_pdf_report(df, filename="reports/rps_report.pdf"):
    """Generates pdf report"""

    with PdfPages(filename) as pdf:

        # 1. Outcomes
        plot_outcome_distribution(df, "reports/outcome.png")
        img = plt.imread("reports/outcome.png")
        fig, ax = plt.subplots()
        ax.imshow(img)
        ax.axis('off')
        pdf.savefig(fig)
        plt.close(fig)

        # 2. Win % by move
        plot_winrate_by_move(df, "reports/winrate.png")
        img = plt.imread("reports/winrate.png")
        fig, ax = plt.subplots()
        ax.imshow(img)
        ax.axis('off')
        pdf.savefig(fig)
        plt.close(fig)

        # 3. Start VS End
        plot_start_vs_end(df, "reports/start_end.png")
        img = plt.imread("reports/start_end.png")
        fig, ax = plt.subplots()
        ax.imshow(img)
        ax.axis('off')
        pdf.savefig(fig)
        plt.close(fig)

        # 4. Text summary page
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis('off')

        # Prepare report content
        outcomes = get_outcome_stats(df)
        win_rates = win_rate_per_move(df)
        streaks = get_streaks(df['Result'].tolist())
        formatted_streaks = "\n".join([f"{label:<12} : {count}" for label, count in streaks])
        formated_win_rates = win_rates.rename_axis(None)

        # Build summar string
        summary = f"""
===========================
 Rock-Paper-Scissors Report
===========================

Total Rounds: {len(df)}

---------------------------
 Outcome Breakdown
---------------------------
{outcomes.to_string(index=True)}

---------------------------
 Player Win Rate Per Move
---------------------------
{win_rates.to_string(index=True)}

---------------------------
 Win/Loss/Draw Streaks
---------------------------
{formatted_streaks}

---------------------------
 Notes
---------------------------
- The charts summarize outcome distribution, player effectiveness by move and consistency across the game.
- Win streacks indicate momentum, while start/end comparison reveals pressure performance.
"""

        # Display summary on PDF page
        ax.text(
            0.05, 1.0, summary,
            va='top', ha='left',
            fontsize=9, family='monospace',
            wrap=True
        )
        pdf.savefig(fig)
        plt.close()
    
    print(f"PDF report saved as {filename}")

def generate_html_report(df, filename="reports/rps_report.html"):
    """Generate html report"""

    outcome_img = "reports/outcome.png"
    winrate_img = "reports/winrate.png"
    startend_img = "reports/start_end.png"

    plot_outcome_distribution(df, outcome_img)
    plot_winrate_by_move(df, winrate_img)
    plot_start_vs_end(df, startend_img)

    html = f"""
    <html>
    <head><title>RPS Game Report<h1>
    <h2>1. Game Outcomes</h2>
    <img src="{outcome_img}" width="500">
    <h2>2. Player Win Rate Per move</h2>
    <img src="{winrate_img}" width="500">
    <h2>3. Start VS End Game Performance<\h2>
    <img src="{startend_img}" width="500">
    </body>
    </html>
    """

    with open(filename, "w") as f:
        f.write(html)

    print(f"HTML report saves as {filename}")



if __name__ == "__main__":
    
    ensure_reports_folder()
    cleanup_old_charts()
    df = load_data()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    pdf_filename = f"reports/rps_report_{timestamp}.pdf"
    html_filename = f"reports/rps_report_{timestamp}.html"

    generate_pdf_report(df)
    generate_html_report(df)