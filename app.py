import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="CERF Dashboard", layout="wide")

# Load data
df = pd.read_csv("cleaned_data.csv")

# Title
st.title("🌍 CERF Donor Contributions Dashboard")

st.markdown(""""
Explore global humanitarian funding contributions.  
Use filters on the left to analyse trends and insights.
""")

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

# KPIs 
st.subheader("Key Insights")

col1, col2, col3, col4 = st.columns(4)

total_contribution = filtered_df["Contribution"].sum()
avg_contribution = filtered_df["Contribution"].mean()
max_contribution = filtered_df["Contribution"].max()

top_country = (
    filtered_df.groupby("Country")["Contribution"]
    .sum()
    .idxmax()
)

col1.metric(" Total", f"${total_contribution:,.0f}")
col2.metric(" Average", f"${avg_contribution:,.0f}")
col3.metric(" Max", f"${max_contribution:,.0f}")
col4.metric(" Top Country", top_country)



# Line chart for contribution trends
st.subheader(" Contribution Trend Over Years")

trend = filtered_df.groupby("Year")["Contribution"].sum()
st.line_chart(trend)

st.markdown("🔍 Contributions vary over time depending on global humanitarian needs.")

# Bar chart for top donor countries
st.subheader(" Top Donor Countries")

top_countries = (
    df.groupby("Country")["Contribution"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_countries)

st.markdown("🔍 A small number of countries dominate total contributions.")

# Pie chart for contribution distribution
st.subheader(" Contribution Distribution")

pie_data = (
    df.groupby("Country")["Contribution"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

colors = ["#4C4EAF", '#2196F3', "#07E2FF", "#9F22FF", "#B02792"]

fig, ax = plt.subplots()
ax.pie(
    pie_data,
    labels=pie_data.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors
)
ax.axis('equal')
ax.set_title("Top 5 Donor Contribution Share")

st.pyplot(fig)

st.markdown("🔍 Contribution distribution is highly concentrated among top donors.")

# Map visualization for geographic distribution
st.subheader(" Global Contribution Map")

# Create sample coordinates (simplified mapping)
country_coords = {
    "United States": [37.0902, -95.7129],
    "United Kingdom": [55.3781, -3.4360],
    "Germany": [51.1657, 10.4515],
    "Canada": [56.1304, -106.3468],
    "Australia": [-25.2744, 133.7751],
}

map_data = df.groupby("Country")["Contribution"].sum().reset_index()

map_data["lat"] = map_data["Country"].map(lambda x: country_coords.get(x, [0, 0])[0])
map_data["lon"] = map_data["Country"].map(lambda x: country_coords.get(x, [0, 0])[1])

st.map(map_data[['lat', 'lon']])

st.markdown("🔍 Map shows geographic distribution of major donor countries.")

# Data table
st.subheader(" Filtered Data")
st.dataframe(filtered_df)










