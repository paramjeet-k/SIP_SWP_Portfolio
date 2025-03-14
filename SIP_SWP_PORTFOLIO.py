import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Streamlit UI Setup
st.set_page_config(page_title="SIP + SWP Calculator", layout="wide")

# Function to calculate SIP + SWP together and generate cash flow breakdown
def calculate_sip_swp(monthly_investment, sip_rate, swp_amount, swp_rate, sip_months, swp_start_month, swp_months):
    rate_sip = (sip_rate / 100) / 12
    rate_swp = (swp_rate / 100) / 12
    balance = 0
    
    # DataFrame to store monthly details
    cashflow_data = []
    
    for month in range(sip_months):
        sip_contribution = monthly_investment if month < sip_months else 0
        
        # Interest earned before withdrawal
        interest_earned = balance * rate_sip
        
        # Update balance based on SIP and interest earned
        balance = (balance + sip_contribution) * (1 + rate_sip)
        
        # SWP withdrawal
        swp_withdrawal = 0
        if swp_start_month <= month < swp_start_month + swp_months:
            swp_withdrawal = swp_amount
            balance -= swp_withdrawal
        
        # Store cash flow data
        cashflow_data.append({
            'Month': month + 1,
            'SIP Contribution': sip_contribution,
            'SWP Withdrawal': swp_withdrawal,
            'Interest Earned': interest_earned,
            'Net Balance': balance
        })
        
        if balance <= 0:
            break
    
    # Convert to DataFrame
    cashflow_df = pd.DataFrame(cashflow_data)
    
    return balance, cashflow_df

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
final_value, cashflow_df = calculate_sip_swp(sip_amount, sip_rate, swp_amount, swp_rate, sip_months, swp_start_month, swp_months)

# 📊 Portfolio Tracker
st.subheader("📊 Portfolio Tracker")

# Plot Portfolio Value Over Time
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(cashflow_df['Month'], cashflow_df['Net Balance'], label="Portfolio Value", color='blue', linewidth=2)
ax.axhline(0, color='red', linestyle='--', label="Zero Balance")
ax.set_xlabel("Month")
ax.set_ylabel("Portfolio Value (₹)")
ax.set_title("Portfolio Value Over Time (SIP + SWP)")
ax.legend()
st.pyplot(fig)

# 📋 Growth Table (Detailed Monthly Breakdown)
if st.checkbox("Show Growth Table"):
    st.write(cashflow_df)

# ✅ Option to Show Pie Chart
if st.checkbox("Show Pie Chart of Contributions"):
    total_sip = cashflow_df['SIP Contribution'].sum()
    total_swp = cashflow_df['SWP Withdrawal'].sum()
    total_interest = cashflow_df['Interest Earned'].sum()
    
    pie_labels = ['Total SIP Contribution', 'Total SWP Withdrawal', 'Total Interest Earned']
    pie_values = [total_sip, total_swp, total_interest]
    
    fig, ax = plt.subplots()
    ax.pie(pie_values, labels=pie_labels, autopct='%.1f%%', startangle=90)
    ax.set_title("Contribution Breakdown (SIP vs SWP vs Interest)")
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

# Create Summary Table
summary_data = {
    "Parameter": [
        "Total SIP Investment",
        "Total SWP Withdrawal",
        "Total Interest Earned",
        "Portfolio Value After SIP + SWP"
    ],
    "Value (₹)": [
        f"{(cashflow_df['SIP Contribution'].sum()) / conversion_factor:,.2f}",
        f"{(cashflow_df['SWP Withdrawal'].sum()) / conversion_factor:,.2f}",
        f"{(cashflow_df['Interest Earned'].sum()) / conversion_factor:,.2f}",
        f"{final_value / conversion_factor:,.2f}"
    ]
}

summary_df = pd.DataFrame(summary_data)

# Display the table
st.table(summary_df)

# ✅ Final Summary
st.markdown("""
### 💡 Key Insights:
- SIP and SWP calculations are based on compounding interest.
- SIP and SWP can now overlap and operate simultaneously.
- Inflation adjustment reduces real value over time.
- Cash flow details are visible in the growth table.
- Pie chart provides a clear breakdown of total contribution.
""")

# Footer
st.caption("Designed by Paramjeet")
