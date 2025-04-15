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

# Define betting criteria
def betting_decision(row):
    win_rate = row["Horse Past Wins"] / (row["Horse Past Wins"] + 10)  # Assumed 10 previous races
    jockey_success = row["Jockey Past Wins"] / (row["Jockey Past Wins"] + 20)  # Assumed 20 previous races
    odds_prob = 1 / row["Bookmaker Odds"]  # Convert odds to probability

    # Calculate win probability score
    probability_score = (win_rate * 0.4) + (jockey_success * 0.3) + (odds_prob * 0.3)

    # Betting Criteria: High probability score & reasonable odds (<= 5)
    if probability_score > 0.5 and row["Bookmaker Odds"] <= 5:
        return "Recommended Bet"
    else:
        return "Not Recommended"

# Apply betting logic
df["Win Probability"] = df.apply(betting_decision, axis=1)

# Streamlit Dashboard
st.title("Horse Racing Betting Analysis")
st.header("Horse Racing Insights")
st.write("Filter horses based on race data, odds, jockey history, and more!")

# **New Filters Added**
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
st.dataframe(filtered_df[["Race Location", "Horse Name", "Jockey Name", "Fractional Odds", "Win Probability"]])

# Summary of bets
recommended_bets = filtered_df[filtered_df["Win Probability"] == "Recommended Bet"]
st.write(f"Total Recommended Bets: {len(recommended_bets)}")
