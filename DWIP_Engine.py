import streamlit as st
import pandas as pd
from fractions import Fraction

# Load CSV file
@st.cache_data
def load_data():
    return pd.read_csv("horse_racing_data.csv")  # Ensure this CSV file is in the same directory

# Convert decimal odds to fractional odds
def decimal_to_fractional(decimal_odds):
    fraction = Fraction(decimal_odds - 1).limit_denominator(100)
    return f"{fraction.numerator}/{fraction.denominator}"

# Load data and preprocess
df = load_data()
df["Fractional Odds"] = df["Bookmaker Odds"].apply(decimal_to_fractional)

# Calculate probability based on performance and odds
def calculate_win_probability(row):
    horse_win_rate = row["Horse Past Wins"] / (row["Horse Past Wins"] + 10)  # Assumed 10 previous races
    jockey_success = row["Jockey Past Wins"] / (row["Jockey Past Wins"] + 20)  # Assumed 20 previous races
    odds_prob = 1 / row["Bookmaker Odds"]  # Convert odds to probability

    # Weighted probability score
    probability_score = (horse_win_rate * 0.4) + (jockey_success * 0.3) + (odds_prob * 0.3)
    
    # Betting recommendation
    if probability_score > 0.5:
        return "High Probability ✅"
    elif probability_score > 0.3:
        return "Moderate Probability ⚠️"
    else:
        return "Low Probability ❌"

# Apply the probability calculation
df["Betting Advice"] = df.apply(calculate_win_probability, axis=1)

# Streamlit Dashboard setup
st.set_page_config(
    page_title="DWIP – Winning Insights",  # Page title
    page_icon="🐎",  # Keep the horse emoji as the icon
    layout="wide"
)

st.title("Horse Racing Betting Analysis")

# Automatically filter the results for the best betting advice
best_bets = df[df["Betting Advice"] == "High Probability ✅"]

# Display the best bets
st.write("### Best Bets:")
st.dataframe(best_bets[["Race Location", "Horse Name", "Jockey Name", "Fractional Odds", "Betting Advice"]])

# Summary of the best betting results
st.write(f"Total High Probability Bets: {len(best_bets)} ✅")
