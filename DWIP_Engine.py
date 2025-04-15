import streamlit as st
import pandas as pd
from fractions import Fraction

# Load CSV file
@st.cache_data
def load_data():
    return pd.read_csv("horse_racing_data.csv")

df = load_data()

# Convert decimal odds to fractional odds
def decimal_to_fractional(decimal_odds):
    fraction = Fraction(decimal_odds - 1).limit_denominator(100)
    return f"{fraction.numerator}/{fraction.denominator}"

df["Fractional Odds"] = df["Bookmaker Odds"].apply(decimal_to_fractional)

# Calculate probability
def calculate_win_probability(row):
    horse_win_rate = row["Horse Past Wins"] / (row["Horse Past Wins"] + 10)  # Assumed 10 previous races
    jockey_success = row["Jockey Past Wins"] / (row["Jockey Past Wins"] + 20)  # Assumed 20 previous races
    odds_prob = 1 / row["Bookmaker Odds"]  # Convert odds to probability

    # Weighted probability score
    probability_score = (horse_win_rate * 0.4) + (jockey_success * 0.3) + (odds_prob * 0.3)
    
    # Betting recommendation
    if probability_score > 0.5:
        return "High Probability - Recommended Bet ✅"
    elif probability_score > 0.3:
        return "Moderate Probability - Proceed with Caution ⚠️"
    else:
        return "Low Probability - Not Recommended ❌"

df["Betting Advice"] = df.apply(calculate_win_probability, axis=1)

# Streamlit Dashboard
st.title("Horse Racing Betting Probability Analysis")
st.header("Assess Betting Worthiness with Data!")
st.write("Filter horses based on race history, odds, and jockey performance.")

# Filters
selected_location = st.selectbox("Select Race Location", df["Race Location"].unique())
selected_horse = st.selectbox("Select Horse Name", df["Horse Name"].unique())
selected_jockey = st.selectbox("Select Jockey Name", df["Jockey Name"].unique())
race_distance = st.slider("Filter by Race Distance", min_value=int(df["Race Distance"].min()), 
                          max_value=int(df["Race Distance"].max()), value=int(df["Race Distance"].min()))

# Apply filters dynamically
filtered_df = df[
    (df["Race Location"] == selected_location) &
    (df["Horse Name"] == selected_horse) &
    (df["Jockey Name"] == selected_jockey) &
    (df["Race Distance"] >= race_distance)
]

# Display results
st.write("Filtered Results:")
st.dataframe(filtered_df[["Race Location", "Horse Name", "Jockey Name", "Fractional Odds", "Betting Advice"]])

# Summary of bets
recommended_bets = filtered_df[filtered_df["Betting Advice"].str.contains("Recommended Bet")]
st.write(f"Total High Probability Bets: {len(recommended_bets)} ✅")
