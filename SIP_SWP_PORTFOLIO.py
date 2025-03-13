import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Function to calculate SIP returns
def calculate_sip(monthly_investment, interest_rate, years, inflation_rate=0, adjust_inflation=False):
    months = years * 12
    rate = (interest_rate / 100) / 12
    future_value = 0
    
    for _ in range(months):
        future_value = (future_value + monthly_investment) * (1 + rate)
    
    if adjust_inflation:
        future_value = future_value / ((1 + (inflation_rate / 100)) ** years)
    
    return future_value

# Function to calculate SWP (Systematic Withdrawal Plan)
def calculate_swp(starting_value, withdrawal_amount, interest_rate, years):
    months = years * 12
    rate = (interest_rate / 100) / 12
    balance = starting_value
    balance_history = []

    for _ in range(months):
        balance = (balance * (1 + rate)) - withdrawal_amount
        balance_history.append(balance)
        if balance <= 0:
            break
    
    return balance, balance_history

# Streamlit UI Setup
st.set_page_config(page_title="SIP + SWP Calculator", layout="wide")

# Title
st.title("📈 SIP + SWP Calculator")

# SIP Section
st.subheader("💰 SIP (Systematic Investment Plan)")

# Manual input for SIP values
sip_amount = st.number_input("Enter Monthly SIP Investment (₹)", min_value=0, max_value=int(1e15), value=5000)
sip_rate = st.number_input("Enter Expected Annual Interest Rate for SIP (%)", min_value=0.0, max_value=100.0, value=8.0)
sip_years = st.number_input("Enter SIP Duration (in Years)", min_value=1, max_value=100, value=5)

# Inflation Adjustment Option
adjust_inflation = st.checkbox("Enable Inflation Adjustment")
if adjust_inflation:
    inflation_rate = st.number_input("Enter Expected Inflation Rate (%)", min_value=0.0, max_value=20.0, value=6.0)
else:
    inflation_rate = 0

# ✅ SIP Calculation
sip_value = calculate_sip(sip_amount, sip_rate, sip_years, inflation_rate, adjust_inflation)

# Display SIP Results
st.write(f"**Total Investment:** ₹{sip_amount * sip_years * 12:.2f}")
st.write(f"**Portfolio Value at End of SIP:** ₹{sip_value:.2f}")

# SWP Section
st.subheader("🏦 SWP (Systematic Withdrawal Plan)")

# Manual input for SWP values
swp_amount = st.number_input("Enter Monthly Withdrawal Amount (₹)", min_value=0, max_value=int(1e15), value=5000)
swp_rate = st.number_input("Enter Expected Annual Interest Rate for SWP (%)", min_value=0.0, max_value=100.0, value=7.0)
swp_years = st.number_input("Enter SWP Duration (in Years)", min_value=1, max_value=100, value=10)

# ✅ Option to continue SIP during SWP
continue_sip = st.checkbox("Continue SIP During SWP")

# Adjust starting value for SWP if SIP continues
if continue_sip:
    sip_value_during_swp = calculate_sip(sip_amount, sip_rate, swp_years, inflation_rate, adjust_inflation)
else:
    sip_value_during_swp = 0

# ✅ Total Starting Value for SWP
starting_value = sip_value + sip_value_during_swp

# ✅ SWP Calculation
final_value, balance_history = calculate_swp(starting_value, swp_amount, swp_rate, swp_years)

# Display Results
st.write(f"**Starting Value for SWP:** ₹{starting_value:.2f}")
st.write(f"**Portfolio Value at End of SWP:** ₹{final_value:.2f}")

# 📊 Portfolio Tracker
st.subheader("📊 Portfolio Tracker")

# Plot Portfolio Value Over Time
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(balance_history, label="Portfolio Value", color='blue', linewidth=2)
ax.axhline(0, color='red', linestyle='--', label="Zero Balance")
ax.set_xlabel("Months")
ax.set_ylabel("Portfolio Value (₹)")
ax.set_title("Portfolio Value Over Time (SIP + SWP)")
ax.legend()
st.pyplot(fig)

# 📋 Summary Table
st.write("### 📋 Summary Table")
summary_data = {
    "Parameter": [
        "Total SIP Investment",
        "Portfolio Value After SIP",
        "Total SWP Withdrawal",
        "Portfolio Value After SWP"
    ],
    "Value (₹)": [
        sip_amount * sip_years * 12,
        sip_value,
        swp_amount * swp_years * 12,
        final_value
    ]
}

summary_df = pd.DataFrame(summary_data)
st.table(summary_df)

# ✅ Final Summary
st.markdown("""
### 💡 Key Insights:
- SIP and SWP calculations are based on compounding interest.
- SIP continues growing even during SWP if selected.
- Inflation adjustment reduces real value over time.
""")

# Footer
st.caption("Designed with ❤️ by ChatGPT")

