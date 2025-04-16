import streamlit as st
import pandas as pd

st.set_page_config(page_title="DWIP", page_icon="app_icon.jpg", layout="wide")

# Load the data from CSV file
@st.cache_data
def load_data():
    # Load the CSV
    df = pd.read_csv("horse_races_today.csv")  # Change this if the filename is different
    
    # Verify the columns are as expected
    if len(df.columns) == 4:
        # Set the column names as desired
        df.columns = ['Race Date', 'Race Time', 'Meeting', 'Horse Name']
    else:
        st.error(f"Expected 4 columns, but the CSV has {len(df.columns)} columns.")
        return pd.DataFrame()  # Return an empty DataFrame if columns mismatch
    
    return df

# Load the data into a DataFrame
df = load_data()

# If the DataFrame is empty due to mismatch, stop further execution
if df.empty:
    st.stop()

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
    "Race Date", "Race Time", "Meeting", "Horse Name"
]])
