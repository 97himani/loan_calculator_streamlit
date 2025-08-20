import streamlit as st
import pandas as pd

st.title("🏦 Interactive Loan Calculator")

# User Inputs
name = st.text_input("👤 Enter your Name")
age = st.number_input("🎂 Enter your Age", min_value=18, max_value=100, value=25)
deposit = st.number_input("💰 Initial Deposit (₹)", min_value=0, value=10000, step=1000)
loan_amount = st.number_input("📌 Loan Amount (₹)", min_value=1000, value=50000, step=1000)
interest_rate = st.slider("📊 Interest Rate (%)", min_value=1.0, max_value=20.0, value=7.5, step=0.1)
duration = st.number_input("⏳ Duration (Years)", min_value=1, max_value=30, value=5)
emi_toggle = st.toggle("Show EMI Calculation")
show_dataframe = st.checkbox("Show Amortization Table")

# Loan Calculation
monthly_rate = interest_rate / 100 / 12
months = duration * 12
emi = (loan_amount * monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
total_payment = emi * months
total_interest = total_payment - loan_amount

# Output
st.subheader("📌 Loan Summary")
st.write(f"Hello **{name}**, based on your inputs:")

if emi_toggle:
    st.metric("Monthly EMI (₹)", f"{emi:,.2f}")

st.metric("Total Payment (₹)", f"{total_payment:,.2f}")
st.metric("Total Interest (₹)", f"{total_interest:,.2f}")

# Amortization Table
if show_dataframe:
    schedule = []
    balance = loan_amount
    for m in range(1, months+1):
        interest = balance * monthly_rate
        principal = emi - interest
        balance -= principal
        schedule.append([m, emi, principal, interest, balance if balance > 0 else 0])
    
    df = pd.DataFrame(schedule, columns=["Month", "EMI", "Principal", "Interest", "Balance"])
    st.dataframe(df)

    # 📉 Easy Graphs with Streamlit
    st.subheader("📊 Loan Balance Over Time")
    st.line_chart(df[["Balance"]])

    st.subheader("📊 Principal vs Interest Paid Each Month")
    st.area_chart(df[["Principal", "Interest"]])
