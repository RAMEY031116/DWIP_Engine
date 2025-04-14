import streamlit as st
st.title("HELLO Iron Phantom")
st.header (" 🏇 Horse Racing Value Bet Checker")
st.image("https://www.google.com/url?sa=i&url=https%3A%2F%2Fgifer.com%2Fen%2Fgifs%2Fdonkeys&psig=AOvVaw2URUFqEfL8OgaqIe1cq4z4&ust=1744750605371000&source=images&cd=vfe&opi=89978449&ved=0CBMQjRxqGAoTCOCo1Mq02IwDFQAAAAAdAAAAABCoAQ", caption="$$$$$$$$$$$$$$")



horses = ["Thunder Bolt", "Speedy Star", "Night Runner", "Golden Hoof"]
jockeys = ["Tom Marquez", "Hollie Doyle", "Ryan Moore", "William Buick"]


horse = st.selectbox("Select Horse", horses)
jockey = st.selectbox("Select Jockey", jockeys)


st.subheader("Enter Odds (Fractional Format)")
numerator = st.number_input("Numerator (e.g., 10 in 10/1)", min_value=1)
denominator = st.number_input("Denominator (e.g., 1 in 10/1)", min_value=1)



if numerator and denominator and your_estimate:
    decimal_odds = numerator / denominator + 1
    implied_prob = 1 / decimal_odds * 100
    ev = your_estimate - implied_prob

    st.markdown(f"Decimal Odds:** {decimal_odds:.2f}")
    st.markdown(f"Implied Probability from Odds: {implied_prob:.2f}%")
    st.markdown(f"Your Estimated Chance: {your_estimate:.2f}%")

    if ev > 0:
        st.success("✅ This looks like a VALUE BET based on your estimate!")
    else:
        st.warning("⚠️ Not a value bet. The odds may not be in your favor.")


st.caption("Note: This tool helps you compare your predicted chance vs. odds. It doesn't predict winners—yet 😉")