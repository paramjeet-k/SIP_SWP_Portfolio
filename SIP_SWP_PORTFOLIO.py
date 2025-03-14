import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Streamlit UI Setup
st.set_page_config(page_title="SIP + SWP Calculator", layout="wide")

# Function to calculate SIP + SWP together
def calculate_sip_swp(monthly_investment, sip_rate, swp_amount, swp_rate, sip_months, swp_start_month, swp_months):
    rate_sip = (sip_rate / 100) / 12
    rate_swp = (swp_rate / 100) / 12
    balance = 0
    balance_history = []
    
    for month in range(sip_months):
        # SIP contribution (if SIP is still active)
        balance = (balance + monthly_investment) * (1 + rate_sip)
        
        # Start SWP if within the SWP window
        if swp_start_month <= month < swp_start_month + swp_months:
            balance -= swp_amount
            
        # Store balance for tracking
        balance_history.append(balance)
        
        # If balance becomes negative, stop withdrawals
        if balance <= 0:
            break
    
    return balance, balance_history

# Title
st.title("📈 SIP + SWP Calculator")

# SIP Section
st.subheader("💰 SIP (Systematic Investment Plan)")

sip_amount = st.number_input("Enter Monthly SIP Investment (₹)", min_value=0, max_value=int(1e15), value=5000)
sip_rate = st.number_input("Enter Expected Annual Interest Rate for SIP (%)", min_value=0.0, max_value=100.0, value=8.0)
sip_years = st.number_input("Enter SIP Duration (in Years)", min_value=1, max_value=100, value=20)

# Inflation Adjustment Option
adjust_inflation = st.checkbox("Enable Inflation Adjustment")
if adjust_inflation:
    inflation_rate = st.number_input("Enter Expected Inflation Rate (%)", min_value=0.0, max_value=20.0, value=6.0)
else:
    inflation_rate = 0

# SWP Section
st.subheader("🏦 SWP (Systematic Withdrawal Plan)")

# SWP Start Point Option
swp_start_year = st.number_input("Start SWP After How Many Years?", min_value=1, max_value=sip_years, value=5)

swp_amount = st.number_input("Enter Monthly Withdrawal Amount (₹)", min_value=0, max_value=int(1e15), value=5000)
swp_rate = st.number_input("Enter Expected Annual Interest Rate for SWP (%)", min_value=0.0, max_value=100.0, value=7.0)
swp_years = st.number_input("Enter SWP Duration (in Years)", min_value=1, max_value=sip_years, value=10)

# Convert years to months
sip_months = sip_years * 12
swp_start_month = swp_start_year * 12
swp_months = swp_years * 12

# ✅ Run SIP + SWP Calculation Together
final_value, balance_history = calculate_sip_swp(sip_amount, sip_rate, swp_amount, swp_rate, sip_months, swp_start_month, swp_months)

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

conversion_factor = float(conversion_options[conversion_choice])

# Convert and format values directly
summary_data = {
    "Parameter": [
        "Total SIP Investment",
        "Total SWP Withdrawal",
        "Portfolio Value After SIP + SWP"
    ],
    "Value (₹)": [
        f"{(sip_amount * sip_years * 12) / conversion_factor:,.2f}",
        f"{(swp_amount * swp_years * 12) / conversion_factor:,.2f}",
        f"{final_value / conversion_factor:,.2f}"
    ]
}

# Create DataFrame
summary_df = pd.DataFrame(summary_data)

# Display the table
st.table(summary_df)

# ✅ Final Summary
st.markdown("""
### 💡 Key Insights:
- SIP and SWP calculations are based on compounding interest.
- SIP and SWP can now overlap and operate simultaneously.
- Inflation adjustment reduces real value over time.
- If the portfolio value becomes negative, withdrawals will stop.
""")

# Footer
st.caption("Designed by Paramjeet")
