import streamlit as st
import pandas as pd

st.set_page_config(page_title="DWIP", page_icon="app_icon.jpg", layout="wide")

# Load the data from CSV file
@st.cache_data
def load_data():
    # Load the CSV and rename columns to match the headers you want
    df = pd.read_csv("horse_races_today.csv")
    
    # Rename columns to "Race Time", "Meeting", and "Horse Name"
    df.columns = ['Race Time', 'Meeting', 'Horse Name']
    
    return df

# Load the data into a DataFrame
df = load_data()

# ---- Streamlit User Interface ----

# App title
st.title("🐎 DWIP - Data for Winning Insights and Probability")

# Intro text
st.write("This app gives you simple betting advice based on horse past performance.")

# Filters for Race Time, Meeting, and Horse Name
race_time = st.selectbox("Choose a Race Time:", df["Race Time"].unique())
meeting = st.selectbox("Choose a Meeting:", df["Meeting"].unique())
horse = st.selectbox("Choose a Horse:", df["Horse Name"].unique())

# Filter the data based on selections
filtered_data = df[
    (df["Race Time"] == race_time) &
    (df["Meeting"] == meeting) &
    (df["Horse Name"] == horse)
]

# Display the results
st.subheader("🎯 Filtered Race Results")
st.dataframe(filtered_data[[
    "Race Time", "Meeting", "Horse Name"
]])

