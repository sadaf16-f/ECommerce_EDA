import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("EDA - Ecommerce Dataset")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Show basic info
    st.subheader("Dataset Overview")
    st.write("Shape:", df.shape)
    st.write("Missing Values per Column:")
    st.write(df.isnull().sum())

    st.subheader("Summary Statistics")
    st.write(df.describe(include="all"))

    # Clean Data
    if df['discount'].max() > 1:  # if discount in percentages
        df['Revenue'] = df['quantity'] * df['price'] * (1 - df['discount'] / 100)
    else:
        df['Revenue'] = df['quantity'] * df['price'] * (1 - df['discount'])

    df['order_date'] = pd.to_datetime(df['order_date'])
    df['month'] = df['order_date'].dt.to_period("M").astype(str)

    # Revenue by Category
    st.subheader("📦 Revenue by Category")
    fig1 = px.bar(
        df.groupby("category")['Revenue'].sum().reset_index(),
        x="category", y="Revenue", color="category",
        title="Revenue by Category", text_auto=True
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Revenue by Region
    st.subheader("🌍 Revenue Share by Region")
    fig2 = px.pie(df, names="region", values="Revenue", title="Revenue Share by Region")
    st.plotly_chart(fig2, use_container_width=True)

    # Monthly Revenue Trend
    st.subheader("📆 Monthly Revenue Trend")
    monthly = df.groupby("month")['Revenue'].sum().reset_index()
    fig3 = px.line(monthly, x="month", y="Revenue", markers=True, title="Monthly Revenue Trend")
    st.plotly_chart(fig3, use_container_width=True)

    # Payment Method Usage
    st.subheader("💳 Payment Method Distribution")
    fig4 = px.histogram(df, x="payment_method", color="payment_method", title="Payment Method Distribution")
    st.plotly_chart(fig4, use_container_width=True)

else:
    st.info("👆 Please upload a CSV file to begin analysis.")
