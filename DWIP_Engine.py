# import streamlit as st
# import pandas as pd

# st.set_page_config(page_title="DWIP", page_icon="app_icon.jpg", layout="wide")

# # ---- Load Data Function with Error Handling ----
# @st.cache_data
# def load_data(file_name):
#     try:
#         # Try to load the CSV file
#         df = pd.read_csv(file_name)

#         # Check the number of columns and assign appropriate column names
#         if len(df.columns) == 7:
#             df.columns = ["Date", 'Meeting', 'Race Class', 'Distance', 'no. & Horse Name ', 'Position', 'Odds']
#         elif len(df.columns) == 4:
#             df.columns = ['Race Date', 'Race Time', 'Meeting', 'Horse Name']
#         else:
#             st.error(f"Expected 4 or 6 columns, but the CSV has {len(df.columns)} columns.")
#             return pd.DataFrame()

#         return df

#     except FileNotFoundError:
#         st.error(f"File '{file_name}' not found. Make sure it's in your GitHub repo and Streamlit Cloud folder.")
#         return pd.DataFrame()

#     except Exception as e:
#         st.error(f"Error loading '{file_name}': {e}")
#         return pd.DataFrame()

# # ---- Load Main Data ----
# df = load_data("horse_races_today.csv")

# if df.empty:
#     st.stop()  # Stop app if no data found

# # ---- Load Results Data ----
# st.header("📜 Horses Result of last 20 days")
# df_results = load_data("Horses_today_result.csv")

# if df_results.empty:
#     st.warning("No race results found. Please check your data file.")
# else:
#     st.dataframe(df_results)

# # ---- Streamlit Interface ----
# st.title("🐎 DWIP - Data for Winning Insights and Probability")
# st.write("This app gives you simple betting advice based on past horse performance.")

# # Dropdown filters
# race_time = st.selectbox("Choose a Race Time:", df["Race Time"].unique())
# meeting = st.selectbox("Choose a Meeting:", df["Meeting"].unique())
# horse = st.selectbox("Choose a Horse:", df["Horse Name"].unique())

# # Filter and show selected data
# filtered_data = df[
#     (df["Race Time"] == race_time) &
#     (df["Meeting"] == meeting) &
#     (df["Horse Name"] == horse)
# ]

# st.subheader("🎯 Filtered Race Results")
# st.dataframe(filtered_data)

# # ---- Bet Calculator ----
# st.header("💰 Bet Calculator")

# stake = st.number_input("Enter your stake (£)", min_value=0.0)
# fractional_odds = st.text_input("Enter the odds in fractional format (e.g., 5/1, 7/2)", value="0/0")

# # Convert Fractional Odds to Decimal
# def convert_fraction_to_decimal(fraction_str):
#     try:
#         numerator, denominator = map(int, fraction_str.split("/"))
#         return round(1 + (numerator / denominator), 2)
#     except:
#         return None

# if st.button("Calculate"):
#     decimal_odds = convert_fraction_to_decimal(fractional_odds)

#     if decimal_odds is None:
#         st.error("Invalid fractional odds format. Please enter them like 5/1 or 7/2.")
#     else:
#         total_return = round(stake * decimal_odds, 2)
#         profit = round(total_return - stake, 2)

#         st.subheader(f"📈 Decimal Odds: {decimal_odds}")
#         st.subheader(f"💷 Total Return: £{total_return}")
#         st.subheader(f"💵 Profit: £{profit}")



i# 🐎 DWIP Streamlit App
import streamlit as st
import pandas as pd
import datetime
from horses_result_today import todays_results  # Make sure this exists

# ---- App Config ----
st.set_page_config(page_title="DWIP", page_icon="app_icon.jpg", layout="wide")

# ---- Update hours setup ----
UPDATE_HOURS = [9, 15, 21]  # 9 AM, 3 PM, 9 PM

# ---- Function to Update Data ----
def update_all_data():
    st.info("Updating all data... please wait.")
    todays_results()
    st.success("All data updated successfully!")

# ---- Get current hour ----
now = datetime.datetime.now()
current_hour = now.hour

# ---- Automatic update if correct time ----
if current_hour in UPDATE_HOURS:
    update_all_data()
else:
    st.success("Using existing data (no update needed now).")

# ---- Load Data Function ----
@st.cache_data
def load_data(file_name):
    try:
        df = pd.read_csv(file_name)

        # Adjust column names based on number of columns
        if len(df.columns) == 7:
            df.columns = ["Date", "Meeting", "Race Class", "Distance", "Horse Name", "Position", "Odds"]
        elif len(df.columns) == 4:
            df.columns = ["Race Date", "Race Time", "Meeting", "Horse Name"]
        else:
            st.error(f"❌ Expected 4 or 7 columns, but found {len(df.columns)} in {file_name}.")
            return pd.DataFrame()

        return df

    except FileNotFoundError:
        st.error(f"❌ File '{file_name}' not found. Make sure it's uploaded properly.")
        return pd.DataFrame()

    except Exception as e:
        st.error(f"❌ Error loading '{file_name}': {e}")
        return pd.DataFrame()

# ---- Load Main Data (Today's Races) ----
st.header("📜 Today's Horse Races")

df_today = load_data("horse_races_today.csv")

if df_today.empty:
    st.warning("⚠️ No today's races data found!")
else:
    st.dataframe(df_today)

# ---- Load Results Data (Past Results) ----
st.header("📜 Horses Results (Last 20 Days)")

df_results = load_data("Horse_results.csv")  # Make sure correct file name is here!

if df_results.empty:
    st.warning("⚠️ No race results found!")
else:
    st.dataframe(df_results)

# ---- Streamlit Interface ----
st.title("🐎 DWIP - Data for Winning Insights and Probability")
st.write("This app gives you simple betting advice based on past horse performance.")

# ---- Dropdown Filters ----
if not df_today.empty:
    race_times = df_today["Race Time"].unique() if "Race Time" in df_today.columns else []
    meetings = df_today["Meeting"].unique() if "Meeting" in df_today.columns else []
    horses = df_today["Horse Name"].unique() if "Horse Name" in df_today.columns else []

    race_time = st.selectbox("Choose a Race Time:", race_times)
    meeting = st.selectbox("Choose a Meeting:", meetings)
    horse = st.selectbox("Choose a Horse:", horses)

    # ---- Filter and show selected data ----
    filtered_data = df_today[
        (df_today["Race Time"] == race_time) &
        (df_today["Meeting"] == meeting) &
        (df_today["Horse Name"] == horse)
    ]

    st.subheader("🎯 Filtered Race Result")
    st.dataframe(filtered_data)

# ---- Bet Calculator ----
st.header("💰 Bet Calculator")

stake = st.number_input("Enter your stake (£)", min_value=0.0, value=10.0)
fractional_odds = st.text_input("Enter the odds (fractional format, e.g., 5/1):", value="5/1")

def convert_fraction_to_decimal(fraction_str):
    try:
        numerator, denominator = map(int, fraction_str.split("/"))
        return round(1 + (numerator / denominator), 2)
    except Exception:
        return None

if st.button("Calculate"):
    decimal_odds = convert_fraction_to_decimal(fractional_odds)

    if decimal_odds is None:
        st.error("❌ Invalid fractional odds format. Please enter like 5/1 or 7/2.")
    else:
        total_return = round(stake * decimal_odds, 2)
        profit = round(total_return - stake, 2)

        st.subheader(f"📈 Decimal Odds: {decimal_odds}")
        st.subheader(f"💷 Total Return: £{total_return}")
        st.subheader(f"💵 Profit: £{profit}")
