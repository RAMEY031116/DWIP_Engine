import streamlit as st

st.title("HELLO Iron Phantom, this is Our app (DWIP)-   Data for Winning Insights and Probability  ")
st.header("🏇 Horse Racing Value Bet Checker")
st.image("https://i.gifer.com/origin/91/9196e905121e63d49072c720225ac3aa_w200.gif", caption="$$$$$$$$$$$$$$")

# Horse and jockey options
horses = ["Thunder Bolt", "Speedy Star", "Night Runner", "Golden Hoof"]
jockeys = ["Tom Marquez", "Hollie Doyle", "Ryan Moore", "William Buick"]

# Select horse and jockey
horse = st.selectbox("Select Horse", horses)
jockey = st.selectbox("Select Jockey", jockeys)

# Enter odds
st.subheader("Enter Odds (Fractional Format)")
numerator = st.number_input("Numerator (e.g., 10 in 10/1)", min_value=1)
denominator = st.number_input("Denominator (e.g., 1 in 10/1)", min_value=1)

# Input your estimated win probability (using number_input)
your_estimate = st.number_input("Enter Your Estimated Chance of Winning (%)", min_value=0, max_value=100, value=25)

# Calculation logic
if numerator and denominator and your_estimate is not None:
    decimal_odds = numerator / denominator + 1
    implied_prob = 1 / decimal_odds * 100
    ev = your_estimate - implied_prob

    # Display results
    st.markdown(f"Decimal Odds: **{decimal_odds:.2f}**")
    st.markdown(f"Implied Probability from Odds: **{implied_prob:.2f}%**")
    st.markdown(f"Your Estimated Chance: **{your_estimate:.2f}%**")

    # Check if it's a value bet
    if ev > 0:
        st.success("✅ This looks like a VALUE BET based on your estimate!")
    else:
        st.warning("⚠️ Not a value bet. The odds may not be in your favor.")

# Additional caption
st.caption("Note: This tool helps you compare your predicted chance vs. odds. It doesn't predict winners—yet 😉")
