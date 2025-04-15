import streamlit as st
import pandas as pd


st.set_page_config(
    page_title=("DWIP",  page_icon="🐎", layout="wide")

# Load the data from CSV file
@st.cache_data
def load_data():
    # Make sure this file is in the same folder or provide the full path
    return pd.read_csv("horse_racing_data.csv")

# Load the data into a DataFrame
df = load_data()

# Function to calculate a simple betting probability score
def calculate_betting_advice(row):
    # Estimate how good the horse and jockey are (0 to 1 scale)
    horse_score = row["Horse Past Wins"] / (row["Horse Past Wins"] + 10)
    jockey_score = row["Jockey Past Wins"] / (row["Jockey Past Wins"] + 20)

    # Combine them into a simple score
    score = (horse_score * 0.6) + (jockey_score * 0.4)

    # Return betting advice based on the score
    if score > 0.5:
        return "High Probability ✅"
    elif score > 0.3:
        return "Moderate Probability ⚠️"
    else:
        return "Low Probability ❌"

# Apply the betting advice function to each row
df["Betting Advice"] = df.apply(calculate_betting_advice, axis=1)

# ---- Streamlit User Interface ----

# App title
st.title("🐎 DWIP - Data for Winning Insights and Probability")

# Intro text
st.write("This app gives you simple betting advice based on horse and jockey past performance.")

# Filters for location, horse, jockey, and race distance
location = st.selectbox("Choose a Race Location:", df["Race Location"].unique())
horse = st.selectbox("Choose a Horse:", df["Horse Name"].unique())
jockey = st.selectbox("Choose a Jockey:", df["Jockey Name"].unique())

distance = st.slider("Minimum Race Distance (meters):",
                     min_value=int(df["Race Distance"].min()),
                     max_value=int(df["Race Distance"].max()),
                     value=int(df["Race Distance"].min()))

# Filter the data based on selections
filtered_data = df[
    (df["Race Location"] == location) &
    (df["Horse Name"] == horse) &
    (df["Jockey Name"] == jockey) &
    (df["Race Distance"] >= distance)
]

# Display the results
st.subheader("🎯 Filtered Race Results")
st.dataframe(filtered_data[[
    "Race Location", "Race Date", "Horse Name", "Jockey Name", 
    "Horse Past Wins", "Jockey Past Wins", "Race Distance", 
    "Is Favorite?", "Final Result", "Betting Advice"
]])

# Count high probability picks
high_prob = filtered_data[filtered_data["Betting Advice"] == "High Probability ✅"]
st.success(f"High Probability Picks Found: {len(high_prob)} ✅")
