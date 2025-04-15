import streamlit as st
import pandas as pd
from fractions import Fraction

# Load the data from CSV file
@st.cache_data
def load_data():
    # Replace with your actual file name
    return pd.read_csv("horse_racing_data.csv")

df = load_data()

# Function to convert decimal odds to fractional odds (e.g., 4.5 → 7/2)
def decimal_to_fractional(decimal_odds):
    fraction = Fraction(decimal_odds - 1).limit_denominator(100)
    return f"{fraction.numerator}/{fraction.denominator}"

# Apply the conversion to the column
df["Fractional Odds"] = df["Bookmaker Odds"].apply(decimal_to_fractional)

# Function to calculate win probability and betting advice
def calculate_betting_advice(row):
    # Basic estimated win rates
    horse_rate = row["Horse Past Wins"] / (row["Horse Past Wins"] + 10)
    jockey_rate = row["Jockey Past Wins"] / (row["Jockey Past Wins"] + 20)
    odds_probability = 1 / row["Bookmaker Odds"]

    # Combine them with weights
    score = (horse_rate * 0.4) + (jockey_rate * 0.3) + (odds_probability * 0.3)

    # Return advice based on score
    if score > 0.5:
        return "High Probability ✅"
    elif score > 0.3:
        return "Moderate Probability ⚠️"
    else:
        return "Low Probability ❌"

# Create new column with advice
df["Betting Advice"] = df.apply(calculate_betting_advice, axis=1)

# ---- Streamlit User Interface ----

# App title
st.title("🐎 Horse Racing Betting Guide")

# Header text
st.write("This app helps you evaluate horses based on their past wins, jockey stats, and odds.")

# User selections
location = st.selectbox("Choose a Race Location:", df["Race Location"].unique())
horse = st.selectbox("Choose a Horse:", df["Horse Name"].unique())
jockey = st.selectbox("Choose a Jockey:", df["Jockey Name"].unique())

# Race distance filter
distance = st.slider("Minimum Race Distance (meters):", 
                     int(df["Race Distance"].min()), 
                     int(df["Race Distance"].max()), 
                     int(df["Race Distance"].min()))

# Filter data based on user input
filtered_data = df[
    (df["Race Location"] == location) &
    (df["Horse Name"] == horse) &
    (df["Jockey Name"] == jockey) &
    (df["Race Distance"] >= distance)
]

# Show filtered table
st.subheader("🎯 Filtered Race Info")
st.dataframe(filtered_data[["Race Location", "Horse Name", "Jockey Name", "Fractional Odds", "Betting Advice"]])

# Optional: Summary of strong bets
high_prob_bets = filtered_data[filtered_data["Betting Advice"] == "High Probability ✅"]
st.success(f"High Probability Bets Found: {len(high_prob_bets)}")
