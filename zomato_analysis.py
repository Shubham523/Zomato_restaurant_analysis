import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('zomato_cleaned.csv')

# Page config
st.set_page_config(page_title="Zomato Bangalore Dashboard", layout="wide")
st.title("🍽️ Zomato Bangalore Restaurant Intelligence Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
location = st.sidebar.multiselect("Location", sorted(df['location'].unique()))
rest_type = st.sidebar.multiselect(
    "Restaurant Type", 
    sorted(df['rest_type'].dropna().unique())
)
online = st.sidebar.radio("Online Order", ["All", "Yes", "No"])

# Apply filters
if location:
    df = df[df['location'].isin(location)]
if rest_type:
    df = df[df['rest_type'].isin(rest_type)]
if online != "All":
    df = df[df['online_order'] == online]

# KPI Metrics
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Restaurants", len(df))

if len(df) > 0:
    col2.metric("Average Rating", round(df['rate'].mean(), 2))
    col3.metric("Avg Cost for Two", f"₹{int(df['cost'].mean())}")
    col4.metric("Locations Covered", df['location'].nunique())
else:
    col2.metric("Average Rating", "N/A")
    col3.metric("Avg Cost for Two", "N/A")
    col4.metric("Locations Covered", "N/A")

st.markdown("---")

# Key Insights
st.subheader("💡 Key Insights")
st.markdown("""
- 🏆 **Lavelle Road** is Bangalore's highest rated area with an average rating of **4.14**
- 📦 Restaurants with **online ordering** rate higher on average (**3.72 vs 3.66**)
- 🍕 **Pizza + Cafe + Italian** is the highest rated cuisine combination (**4.41 avg**)
- 💰 **Casual Dining** costs 2.4x more than Quick Bites but rates only 0.19 points higher
- 🧇 **Belgian Waffle Factory** is the top budget pick — **4.9 rating under ₹400**
""")

st.markdown("---")

# Chart 1 — Top locations by rating
df_original = pd.read_csv('zomato_cleaned.csv')
st.subheader("📍 Top 10 Locations by Average Rating")
loc_df = df_original.groupby('location')['rate'].mean().reset_index()
loc_df = loc_df.sort_values('rate', ascending=False).head(10)
fig1 = px.bar(loc_df, x='location', y='rate', color='rate',
              color_continuous_scale='reds')
st.plotly_chart(fig1, use_container_width=True)

# Chart 2 — Online order impact
st.subheader("📦 Online Ordering Impact on Ratings")
online_df = df.groupby('online_order')['rate'].mean().reset_index()
fig2 = px.bar(online_df, x='online_order', y='rate', color='online_order',
              range_y=[3.5, 3.9])
st.plotly_chart(fig2, use_container_width=True)

# Chart 3 — Cost vs Rating
st.subheader("💸 Cost vs Rating")
fig3 = px.scatter(df.sample(min(2000, len(df))), x='cost', y='rate',
                  color='rest_type', opacity=0.6,
                  labels={'cost': 'Cost for Two (₹)', 'rate': 'Rating'})
st.plotly_chart(fig3, use_container_width=True)

# Chart 4 — Restaurant type distribution
st.subheader("🍴 Restaurant Type Distribution")
type_df = df['rest_type'].value_counts().reset_index().head(8)
type_df.columns = ['rest_type', 'count']
fig4 = px.pie(type_df, values='count', names='rest_type', hole=0.4)
st.plotly_chart(fig4, use_container_width=True)

# Chart 5 — Rating distribution
st.subheader("⭐ Rating Distribution")
fig5 = px.histogram(df, x='rate', nbins=20, color_discrete_sequence=['#e23744'])
st.plotly_chart(fig5, use_container_width=True)