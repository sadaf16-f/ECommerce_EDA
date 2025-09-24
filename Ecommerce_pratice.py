# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ===============================
# Page Config
# ===============================
st.set_page_config(page_title="Ecommerce EDA", layout="wide")
st.markdown(
    """
    <style>
    body {background-color: #111111; color: #f0f0f0;}
    .stApp {background-color: #111111;}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🛒 Ecommerce Data - Exploratory Data Analysis (Dark Theme)")

# ===============================
# File Upload
# ===============================
uploaded_file = st.file_uploader("📂 Upload your ecommerce_dataset.csv", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Feature engineering
    df["revenue"] = df["quantity"] * df["price"] * (1 - df["discount"])
    df["order_date"] = pd.to_datetime(df["order_date"])

    # ===============================
    # KPIs
    # ===============================
    st.header("📊 Key Performance Indicators")

    total_revenue = df["revenue"].sum()
    total_orders = df["order_id"].nunique()
    avg_order_value = df["revenue"].mean()
    avg_discount = df["discount"].mean() * 100

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
    kpi2.metric("📦 Total Orders", f"{total_orders:,}")
    kpi3.metric("📈 Avg Order Value", f"${avg_order_value:,.2f}")
    kpi4.metric("🏷️ Avg Discount %", f"{avg_discount:.1f}%")

    # ===============================
    # Univariate Analysis
    # ===============================
    st.header("🔹 Univariate Analysis")

    fig, ax = plt.subplots(1, 3, figsize=(15,4), facecolor="#111111")
    sns.histplot(df["price"], kde=True, ax=ax[0], color="cyan")
    ax[0].set_title("Price Distribution", color="white")
    sns.histplot(df["quantity"], kde=True, ax=ax[1], color="magenta")
    ax[1].set_title("Quantity Distribution", color="white")
    sns.histplot(df["discount"], kde=True, ax=ax[2], color="orange")
    ax[2].set_title("Discount Distribution", color="white")
    for a in ax: 
        a.set_facecolor("#111111")
        a.tick_params(colors="white")
        a.title.set_color("white")
    st.pyplot(fig)

    # Violin plot
    st.subheader("Revenue Distribution by Category")
    fig, ax = plt.subplots(figsize=(8,5), facecolor="#111111")
    sns.violinplot(data=df, x="category", y="revenue", palette="Set2", ax=ax)
    ax.set_facecolor("#111111")
    ax.tick_params(colors="white")
    ax.title.set_color("white")
    st.pyplot(fig)

    # ===============================
    # Bivariate Analysis
    # ===============================
    st.header("🔹 Bivariate Analysis")

    st.subheader("Revenue by Category and Region")
    bar_chart = px.bar(df.groupby(["category","region"])["revenue"].sum().reset_index(),
                       x="category", y="revenue", color="region", barmode="group",
                       title="Revenue by Category & Region", 
                       color_discrete_sequence=px.colors.sequential.Viridis)
    st.plotly_chart(bar_chart, use_container_width=True)

    st.subheader("Revenue Distribution by Payment Method")
    fig, ax = plt.subplots(figsize=(8,5), facecolor="#111111")
    sns.boxplot(data=df, x="payment_method", y="revenue", palette="Set3", ax=ax)
    ax.set_facecolor("#111111")
    ax.tick_params(colors="white")
    ax.title.set_color("white")
    st.pyplot(fig)

    # ===============================
    # Time Series Analysis
    # ===============================
    st.header("🔹 Time Series Analysis")
    time_df = df.groupby("order_date")["revenue"].sum().reset_index()
    time_df["rolling"] = time_df["revenue"].rolling(7).mean()

    fig, ax = plt.subplots(figsize=(12,5), facecolor="#111111")
    ax.plot(time_df["order_date"], time_df["revenue"], label="Daily Revenue", color="cyan")
    ax.plot(time_df["order_date"], time_df["rolling"], label="7-Day Rolling Avg", color="magenta")
    ax.legend(facecolor="#111111", labelcolor="white")
    ax.set_facecolor("#111111")
    ax.tick_params(colors="white")
    ax.title.set_color("white")
    ax.set_title("Revenue Trend Over Time")
    st.pyplot(fig)

    # ===============================
    # Correlation Heatmap
    # ===============================
    st.header("🔹 Correlation Analysis")
    fig, ax = plt.subplots(figsize=(8,6), facecolor="#111111")
    sns.heatmap(df[["quantity","price","discount","revenue"]].corr(),
                annot=True, cmap="coolwarm", fmt=".2f", ax=ax, cbar=True)
    ax.set_facecolor("#111111")
    st.pyplot(fig)

else:
    st.info("👆 Upload your dataset to start the EDA.")


