import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 EDA - Ecommerce Dataset")

# Load data
df = pd.read_csv("ecommerce_dataset.csv")

# Show dataset info
st.write("### Dataset Shape:", df.shape)
st.write("### Data Types and Null Values")
st.write(df.info())   # Note: df.info() prints to console, better to use describe + isnull
st.write(df.describe(include="all"))
st.write("### Missing Values")
st.write(df.isnull().sum())

# Clean Data 
if df['discount'].max() > 1:   # if discount in percentages
    df['Revenue'] = df['quantity'] * df['price'] * (1 - df['discount']/100)
else:
    df['Revenue'] = df['quantity'] * df['price'] * (1 - df['discount'])

df['order_date'] = pd.to_datetime(df['order_date'])
df['month'] = df['order_date'].dt.to_period("M").astype(str)

# Revenue by Category 
fig1 = px.bar(df.groupby("category")['Revenue'].sum().reset_index(),
              x="category", y="Revenue", color="category",
              title="📦 Revenue by Category", text_auto=True)
st.plotly_chart(fig1, use_container_width=True)

# Revenue by Region 
fig2 = px.pie(df, names="region", values="Revenue",
              title="🌍 Revenue Share by Region")
st.plotly_chart(fig2, use_container_width=True)

# Monthly Revenue Trend 
monthly = df.groupby("month")['Revenue'].sum().reset_index()
fig3 = px.line(monthly, x="month", y="Revenue", markers=True,
               title="📆 Monthly Revenue Trend")
st.plotly_chart(fig3, use_container_width=True)

# Payment Method Usage
fig4 = px.histogram(df, x="payment_method", color="payment_method",
                       title="💳 Payment Method Distribution")
st.plotly_chart(fig4, use_container_width=True)
