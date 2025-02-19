import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import plotly.express as px

# Load data
data = pd.read_csv("tips (1).csv")

# Convert "billdate" to datetime format
data["billdate"] = pd.to_datetime(data["billdate"])

# Rename columns for better readability
data = data.rename(columns={
    "billdate": "Bill Date",
    "total_bill": "Total Bill",
    "tip": "Tip",
    "day": "Day"
})

# Display DataFrame
st.subheader("📊 Data Overview")
st.dataframe(data)  # Display the dataset as a table

# Daily Sales Chart
st.subheader("📈 Daily Sales Chart")
st.line_chart(data, x="Bill Date", y="Total Bill")

st.divider()  # Divider for each chart

# Scatter Chart: Tip vs. Total Bill
st.subheader("📉 Scatter Plot: Tip vs. Total Bill")
st.scatter_chart(data, x="Tip", y="Total Bill")

st.divider()  # Divider for each chart

# Histogram using Seaborn
st.subheader("📊 Histogram: Total Bill")

fig, ax = plt.subplots(figsize=(13, 5))
sns.histplot(data["Total Bill"], bins=20, kde=True, color="teal", edgecolor="black", alpha=0.8, ax=ax)

# Styling Labels
ax.set_xlabel("Total Bill Amount", fontsize=12, fontweight="bold", color="darkblue")
ax.set_title("Total Bill Distribution", fontsize=14, fontweight="bold", color="black")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
# Show in Streamlit
st.pyplot(fig)

st.divider()  # Divider for each chart

st.title("💰 Salary & Tax Calculator")

# User Inputs
a = st.number_input("Enter your Salary", min_value=0.0, step=100.0, format="%.2f")
b = st.number_input("Enter your Tax Amount", min_value=0.0, step=10.0, format="%.2f")

# Button to calculate net salary
if st.button("Calculate Net Salary"):
    net_salary = a - b if a >= b else 0  # Prevent negative values

    # Display Results
    st.divider()
    st.subheader("📊 Salary Breakdown")

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Salary", f"₱{a:,.2f}")
    col2.metric("💸 Tax", f"₱{b:,.2f}")
    col3.metric("🏦 Net Salary", f"₱{net_salary:,.2f}", delta=-b)

    if net_salary == 0:
        st.warning("Your tax is equal to or greater than your salary!")
    st.success(f"Your net salary is ₱ {net_salary:,.2f}")

