import streamlit as st
import pandas as pd

# Load CSV file
@st.cache_data
def load_data():
    return pd.read_csv("horse_racing_data.csv")

df = load_data()

# Convert decimal odds to fractional odds
def decimal_to_fractional(decimal_odds):
    numerator = round(decimal_odds - 1, 1) * 10
    denominator = 10
    return f"{int(numerator)}/{int(denominator)}"

df["Fractional Odds"] = df["Bookmaker Odds"].apply(decimal_to_fractional)

# Define betting criteria
def betting_decision(row):
    win_rate = row["Horse Past Wins"] / (row["Horse Past Wins"] + 10)  # Assumed 10 previous races
    jockey_success = row["Jockey Past Wins"] / (row["Jockey Past Wins"] + 20)  # Assumed 20 previous races
    odds = row["Bookmaker Odds"]
    
    # Calculate win probability score
    probability_score = (win_rate * 0.4) + (jockey_success * 0.3) + ((1/odds) * 0.3)

    # Betting Criteria: High probability score & reasonable odds (<= 5)
    if probability_score > 0.5 and odds <= 5:
        return "Recommended Bet"
    else:
        return "Not Recommended"

# Apply betting logic
df["Win Probability"] = df.apply(betting_decision, axis=1)

# Streamlit Dashboard
st.title("Horse Racing Betting Analysis")
st.header("Horse Racing Insights")
st.write("Filter horses and assess betting worthiness.")

# Race Location Filter
selected_location = st.selectbox("Select Race Location", df["Race Location"].unique())
filtered_df = df[df["Race Location"] == selected_location]

# Odds Slider Filter
min_odds = st.slider("Minimum Odds (Decimal)", min_value=1.0, max_value=10.0, value=1.0)
filtered_df = filtered_df[filtered_df["Bookmaker Odds"] >= min_odds]

# Display results
st.write("Filtered Results:")
st.dataframe(filtered_df[["Race Location", "Horse Name", "Fractional Odds", "Win Probability"]])

# Summary of bets
recommended_bets = df[df["Win Probability"] == "Recommended Bet"]
st.write(f"Total Recommended Bets: {len(recommended_bets)}")
