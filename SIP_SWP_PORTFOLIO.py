import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Function to calculate SIP returns
def calculate_sip(monthly_investment, interest_rate, months):
    rate = (interest_rate / 100) / 12
    future_value = 0
    
    for _ in range(months):
        future_value = (future_value + monthly_investment) * (1 + rate)
    
    return future_value

# Function to calculate SWP returns
def calculate_swp(starting_value, withdrawal_amount, interest_rate, months):
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
sip_years = st.number_input("Enter SIP Duration (in Years)", min_value=1, max_value=100, value=20)

# Inflation Adjustment Option
adjust_inflation = st.checkbox("Enable Inflation Adjustment")
if adjust_inflation:
    inflation_rate = st.number_input("Enter Expected Inflation Rate (%)", min_value=0.0, max_value=20.0, value=6.0)
else:
    inflation_rate = 0

# ✅ SIP Calculation (before SWP starts)
sip_months = sip_years * 12
sip_value = calculate_sip(sip_amount, sip_rate, sip_months)

# Display SIP Results
st.write(f"**Total Investment:** ₹{sip_amount * sip_years * 12:,.2f}")
st.write(f"**Portfolio Value at End of SIP:** ₹{sip_value:,.2f}")

# SWP Section
st.subheader("🏦 SWP (Systematic Withdrawal Plan)")

# SWP Start Option
start_swp_after_years = st.number_input("Start SWP After How Many Years?", min_value=1, max_value=sip_years, value=5)

# Manual input for SWP values
swp_amount = st.number_input("Enter Monthly Withdrawal Amount (₹)", min_value=0, max_value=int(1e15), value=5000)
swp_rate = st.number_input("Enter Expected Annual Interest Rate for SWP (%)", min_value=0.0, max_value=100.0, value=7.0)
swp_years = st.number_input("Enter SWP Duration (in Years)", min_value=1, max_value=100, value=10)

# ✅ Option to continue SIP during SWP
continue_sip = st.checkbox("Continue SIP During SWP")

# 🧠 Step 1: SIP Calculation Before SWP Starts
months_before_swp = start_swp_after_years * 12
sip_value_before_swp = calculate_sip(sip_amount, sip_rate, months_before_swp)

# 🧠 Step 2: SIP Calculation During SWP (if applicable)
months_after_swp_start = (sip_years - start_swp_after_years) * 12

if continue_sip:
    sip_value_during_swp = calculate_sip(sip_amount, sip_rate, months_after_swp_start)
else:
    sip_value_during_swp = 0

# ✅ Total Starting Value for SWP
starting_value = sip_value_before_swp + sip_value_during_swp

# 🧠 Step 3: SWP Calculation
swp_months = swp_years * 12
final_value, balance_history = calculate_swp(starting_value, swp_amount, swp_rate, swp_months)

# Display Results
st.write(f"**Starting Value for SWP:** ₹{starting_value:,.2f}")
st.write(f"**Portfolio Value at End of SWP:** ₹{final_value:,.2f}")

# 📊 Portfolio Tracker
st.subheader("📊 Portfolio Tracker")

# Prepare Portfolio Value Over Time
portfolio_value = []
current_value = starting_value

for i in range(swp_months):
    if continue_sip:
        current_value = (current_value + sip_amount) * (1 + (swp_rate / 100) / 12) - swp_amount
    else:
        current_value = (current_value * (1 + (swp_rate / 100) / 12)) - swp_amount
    portfolio_value.append(current_value)
    if current_value <= 0:
        break

# Plot Portfolio Value Over Time
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(portfolio_value, label="Portfolio Value", color='blue', linewidth=2)
ax.axhline(0, color='red', linestyle='--', label="Zero Balance")
ax.set_xlabel("Months")
ax.set_ylabel("Portfolio Value (₹)")
ax.set_title("Portfolio Value Over Time (SIP + SWP)")
ax.legend()
st.pyplot(fig)

# 📋 Summary Table
st.subheader("📋 Summary Table")

# Format conversion options
conversion_options = {
    "None (₹)": 1,
    "Lakhs (₹)": 1e5,
    "Crores (₹)": 1e7,
    "Millions ($)": 1e6,
    "Billions ($)": 1e9
}

conversion_choice = st.selectbox("Convert values to:", list(conversion_options.keys()))

conversion_factor = conversion_options[conversion_choice]

# ✅ Format values directly when creating the DataFrame:
summary_data = {
    "Parameter": [
        "Total SIP Investment",
        "Portfolio Value After SIP",
        "Total SWP Withdrawal",
        "Portfolio Value After SWP"
    ],
    "Value (₹)": [
        f"{(sip_amount * sip_years * 12) / conversion_factor:,.2f}",
        f"{sip_value_before_swp / conversion_factor:,.2f}",
        f"{(swp_amount * swp_years * 12) / conversion_factor:,.2f}",
        f"{final_value / conversion_factor:,.2f}"
    ]
}

summary_df = pd.DataFrame(summary_data)

# ✅ Directly use st.table() without `.style.format()`:
st.table(summary_df)


# ✅ Final Summary
st.markdown("""
### 💡 Key Insights:
- SIP and SWP calculations are based on compounding interest.
- SIP continues growing even during SWP if selected.
- Inflation adjustment reduces real value over time.
""")

# Footer
st.caption("Designed by Paramjeet")

