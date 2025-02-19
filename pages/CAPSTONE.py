import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv("CAPSTONEDATA.csv")

# Rename columns for better readability
data = data.rename(columns={
    "COUNTRY": "Country",
    "NETSALES": "Net Sales",
    "PROJDATE": "Project Date",
    "NETTAXPAYABLE": "Net Tax Payable",
    "PROFITAFTERTAX": "Profit After Tax",
    "GROSSSALES": "Gross Sales",
    "GROSSINCOME": "Gross Income"
})

# Convert columns to correct data types
data["Project Date"] = pd.to_datetime(data["Project Date"], errors="coerce")
data["Gross Sales"] = pd.to_numeric(data["Gross Sales"], errors="coerce").fillna(0)

# Convert "Project Date" to categorical format for animation
data["Date String"] = data["Project Date"].dt.strftime('%Y-%m-%d')  # Converts to 'YYYY-MM-DD'

# Streamlit UI
st.title("📈 Capstone Data Visualizations")
st.write(data)

# Date selection
st.subheader("📅 Select Date Range & Chart Type")
col1, col2, col3 = st.columns(3)

with col1:
    chart_options = ["Bar Chart", "Line Chart"]
    selected_chart = st.selectbox("📊 Select a Chart Type", chart_options)
with col2:
    start_date = st.date_input("Start Date", value=data["Project Date"].min().date())
with col3:
    end_date = st.date_input("End Date", value=data["Project Date"].max().date())

# Convert date inputs
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Validate date range
if start_date > end_date:
    st.error("⚠️ End Date must be after Start Date")
else:
    # Filter data based on selected date range
    filtered_data = data[(data["Project Date"] >= start_date) & (data["Project Date"] <= end_date)]

    # Gross Sales per Country Summary
    st.subheader("📈 Summary of Gross Sales per Country")
    country_sales = filtered_data.groupby("Country")["Gross Sales"].sum().reset_index()

    if selected_chart == "Bar Chart":
        if not country_sales.empty:
            fig, ax = plt.subplots(figsize=(13, 5))
            sns.barplot(x="Gross Sales", y="Country", data=country_sales, ax=ax, palette="Blues_r")
            ax.set_xlabel("Gross Sales")
            ax.set_ylabel("Country")
            ax.set_title("Gross Sales by Country")
            st.pyplot(fig)
        else:
            st.warning("⚠️ No data available for the selected date range.")

    elif selected_chart == "Line Chart":
        if not filtered_data.empty:
            # Aggregate sales by date & country
            time_series = filtered_data.groupby(["Date String", "Country"])["Gross Sales"].sum().reset_index()

            # Animated Line Chart
            fig = px.line(
                time_series, x="Date String", y="Gross Sales", color="Country",
                title="Animated Gross Sales Over Time",
                labels={"Date String": "Date", "Gross Sales": "Sales"},
                animation_frame="Date String",  # Animation now works properly
                markers=True
            )

            st.plotly_chart(fig)
        else:
            st.warning("⚠️ No data available for the selected date range.")
