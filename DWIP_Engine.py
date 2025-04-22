import streamlit as st
import pandas as pd

st.set_page_config(page_title="DWIP", page_icon="app_icon.jpg", layout="wide")

# Load the data from CSV file
@st.cache_data

# ---- Display Horses_today_result.csv Data ----
st.header("📜 Horses Today Result Data")
df_results = pd.read_csv("Horses_today_result.csv")  # Load your results CSV file
st.dataframe(df_results)  # Display all rows
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


st.header("Bet Calculator")

stake = st.number_input("Enter your stake (£)", min_value=0.0,)
fractional_odds = st.text_input("Enter the odds in fractional 5/1 or 7/2", value="0/0")

def convert_fraction_to_decimal(fraction_str):
    try:
        numerator, denominator = fraction_str.split("/")
        return round(1 +(int(numerator)/ int(denominator)), 2)
    except:
        return None
    
if st.button("calculate"):
    decimal_odds = convert_fraction_to_decimal(fractional_odds)

    if decimal_odds is None:
        st.error("Invalid fractional odds format. Please enter like 5/1 or 7/2")
    else:
        total_return = round(stake * decimal_odds, 2)
        profit = round(total_return - stake, 2)

        st.subheader(f'decimal odds: {decimal_odds}')
        st.subheader(f"total return : {total_return}")
        st.subheader(f"profit is : {profit}")

