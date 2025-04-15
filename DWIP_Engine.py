import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Load CSV file
@st.cache_data
def load_data():
    return pd.read_csv("horse_racing_data.csv")

df = load_data()

# Define betting criteria
def betting_decision(row):
    win_rate = row["Horse Past Wins"] / (row["Horse Past Wins"] + 10)  # 10 is an assumed number of previous races
    jockey_success = row["Jockey Past Wins"] / (row["Jockey Past Wins"] + 20)  # Assumed number of races
    odds = row["Bookmaker Odds"]
    
    # Betting Criteria: High win rate, experienced jockey, and reasonable odds (<= 5)
    if win_rate > 0.5 and jockey_success > 0.5 and odds <= 5:
        return "Recommended Bet"
    else:
        return "Not Recommended"

# Apply betting logic
df["Betting Advice"] = df.apply(betting_decision, axis=1)

# Streamlit Dashboard
st.title("Horse Racing Betting Analysis")
st.write("Filter horses and assess betting worthiness.")

# Display filtered data
st.dataframe(df)

# Add filters
min_odds = st.slider("Minimum odds", min_value=1.0, max_value=10.0, value=1.0)
filtered_df = df[df["Bookmaker Odds"] >= min_odds]
st.write("Filtered Results:")
st.dataframe(filtered_df)

# Summary
recommended_bets = df[df["Betting Advice"] == "Recommended Bet"]
st.write(f"Total Recommended Bets: {len(recommended_bets)}")
