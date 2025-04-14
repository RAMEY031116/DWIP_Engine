import streamlit as st
st.title("HELLO Iron Phantom")
st.header (" 🏇 Horse Racing Value Bet Checker")


horses = ["Thunder Bolt", "Speedy Star", "Night Runner", "Golden Hoof"]
jockeys = ["Tom Marquez", "Hollie Doyle", "Ryan Moore", "William Buick"]

st.subheader("Enter Odds (Fractional Format)")
numerator = st.number_input("Numerator (e.g., 10 in 10/1)", min_value=1)
denominator = st.number_input("Denominator (e.g., 1 in 10/1)", min_value=1)

your_estimate = st.slider("Your Estimated Chance of Winning (%)", 0, 100, 25)

if numerator and denominator and your_estimate:
    decimal_odds = numerator / denominator + 1
    implied_prob = 1 / decimal_odds * 100
    ev = your_estimate - implied_prob

    st.markdown(f"Decimal Odds:** {decimal_odds:.2f}")
    st.markdown(f"Implied Probability from Odds: {implied_prob:.2f}%")
    st.markdown(f"Your Estimated Chance:** {your_estimate:.2f}%")

    if ev > 0:
        st.success("✅ This looks like a VALUE BET based on your estimate!")
    else:
        st.warning("⚠️ Not a value bet. The odds may not be in your favor.")


st.caption("Note: This tool helps you compare your predicted chance vs. odds. It doesn't predict winners—yet 😉")