import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="CERF Dashboard", layout="wide")

# Load data
df = pd.read_csv("cleaned_data.csv")

# Title
st.title(" CERF Donor Contributions Dashboard")

# Sidebar filters
st.sidebar.header(" Filter Data")

selected_country = st.sidebar.selectbox(
    "Select Country", df["Country"].unique()
)

selected_year = st.sidebar.slider(
    "Select Year",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max()))
)

# Filter data
filtered_df = df[
    (df["Country"] == selected_country) &
    (df["Year"] >= selected_year[0]) &
    (df["Year"] <= selected_year[1])
]

# Add KPI
st.subheader(" Key Insights")

col1, col2, col3 = st.columns(3)

total_contribution = filtered_df["Contribution"].sum()
avg_contribution = filtered_df["Contribution"].mean()
max_contribution = filtered_df["Contribution"].max()

col1.metric(" Total Contribution", f"{total_contribution:,.0f}")
col2.metric(" Average Contribution", f"{avg_contribution:,.0f}")
col3.metric(" Max Contribution", f"{max_contribution:,.0f}")

# Line chart for contribution trend
st.subheader(" Contribution Trend Over Years")

trend = filtered_df.groupby("Year")["Contribution"].sum()
st.line_chart(trend)

# Bar chart for top donor countries
st.subheader(" Top Donor Countries")

top_countries = (
    df.groupby("Country")["Contribution"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_countries)

# Pie chart for contribution distribution
import matplotlib.pyplot as plt

st.subheader(" Contribution Distribution")

pie_data = (
    df.groupby("Country")["Contribution"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

fig, ax = plt.subplots()
ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%')
ax.set_title("Top 5 Donor Contribution Share")

st.pyplot(fig)

# Data Table
st.subheader("Filtered Data")
st.dataframe(filtered_df)











