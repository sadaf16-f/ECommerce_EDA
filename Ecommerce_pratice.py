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
st.title("🛒 Ecommerce Data - Exploratory Data Analysis")

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
    # Dataset Overview
    # ===============================
    st.header("📊 Dataset Overview")
    st.write("Shape:", df.shape)
    st.dataframe(df.head())

    # ===============================
    # Univariate Analysis
    # ===============================
    st.header("🔹 Univariate Analysis")

    # Hist + KDE
    st.subheader("Distribution of Price, Quantity, Discount")
    fig, ax = plt.subplots(1, 3, figsize=(15,4))
    sns.histplot(df["price"], kde=True, ax=ax[0], color="skyblue")
    ax[0].set_title("Price Distribution")
    sns.histplot(df["quantity"], kde=True, ax=ax[1], color="lightgreen")
    ax[1].set_title("Quantity Distribution")
    sns.histplot(df["discount"], kde=True, ax=ax[2], color="salmon")
    ax[2].set_title("Discount Distribution")
    st.pyplot(fig)

    # Violin plot
    st.subheader("Revenue Distribution by Category")
    fig, ax = plt.subplots(figsize=(8,5))
    sns.violinplot(data=df, x="category", y="revenue", palette="pastel")
    st.pyplot(fig)

    # Treemap
    st.subheader("Revenue Share by Category (Treemap)")
    treemap = px.treemap(df, path=["category"], values="revenue", color="revenue",
                         color_continuous_scale="Tealgrn")
    st.plotly_chart(treemap, use_container_width=True)

    
    # ===============================
    # Time Series Analysis
    # ===============================
    st.header("🔹 Time Series Analysis")

    # Revenue trend + rolling avg
    st.subheader("Revenue Trend Over Time")
    time_df = df.groupby("order_date")["revenue"].sum().reset_index()
    time_df["rolling"] = time_df["revenue"].rolling(7).mean()

    fig, ax = plt.subplots(figsize=(12,5))
    ax.plot(time_df["order_date"], time_df["revenue"], label="Daily Revenue", color="teal")
    ax.plot(time_df["order_date"], time_df["rolling"], label="7-Day Rolling Avg", color="orange")
    ax.legend()
    st.pyplot(fig)

    # ===============================
    # Correlation Analysis
    # ===============================
    st.header("🔹 Correlation Analysis")
    fig, ax = plt.subplots(figsize=(8,6))
    sns.heatmap(df[["quantity","price","discount","revenue"]].corr(),
                annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)

else:
    st.info("👆 Upload your dataset to start the EDA.")

