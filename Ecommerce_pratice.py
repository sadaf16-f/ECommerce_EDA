# 📘 Ecommerce Dataset - Detailed EDA
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ===============================
# 1. Page Config
# ===============================
st.set_page_config(page_title="Ecommerce EDA", layout="wide")
st.title("🛒 Ecommerce Data - Exploratory Data Analysis")

# ===============================
# 2. File Upload
# ===============================
uploaded_file = st.file_uploader("📂 Upload your ecommerce_dataset.csv", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # ===============================
    # Dataset Overview
    # ===============================
    st.header("📊 Dataset Overview")
    st.write("Shape:", df.shape)
    st.write(df.head())

    # ===============================
    # Summary Statistics
    # ===============================
    st.subheader("🔎 Summary Statistics")
    st.write(df.describe(include="all"))

    # ===============================
    # Univariate Analysis
    # ===============================
    st.header("📌 Univariate Analysis")

    cat_cols = ["category", "region", "payment_method"]
    num_cols = ["quantity", "price", "discount"]

    for col in cat_cols:
        fig, ax = plt.subplots(figsize=(6,4))
        sns.countplot(data=df, x=col, order=df[col].value_counts().index, ax=ax, palette="pastel")
        ax.set_title(f"Distribution of {col}")
        plt.xticks(rotation=30)
        st.pyplot(fig)

    st.subheader("Distribution of Numerical Columns")
    fig, ax = plt.subplots(figsize=(10,6))
    df[num_cols].hist(bins=20, ax=ax)
    st.pyplot(fig)

    # ===============================
    # Feature Engineering
    # ===============================
    df["revenue"] = df["quantity"] * df["price"] * (1 - df["discount"])

    # ===============================
    # Bivariate Analysis
    # ===============================
    st.header("📌 Bivariate Analysis")

    st.subheader("Revenue by Category")
    fig, ax = plt.subplots(figsize=(8,4))
    sns.barplot(data=df, x="category", y="revenue", estimator=sum, ci=None, palette="pastel", ax=ax)
    st.pyplot(fig)

    st.subheader("Revenue by Region")
    fig, ax = plt.subplots(figsize=(8,4))
    sns.barplot(data=df, x="region", y="revenue", estimator=sum, ci=None, palette="pastel", ax=ax)
    st.pyplot(fig)

    st.subheader("Revenue Distribution by Payment Method")
    fig, ax = plt.subplots(figsize=(8,4))
    sns.boxplot(data=df, x="payment_method", y="revenue", palette="pastel", ax=ax)
    st.pyplot(fig)

    # ===============================
    # Time Series
    # ===============================
    st.header("📌 Time Series Analysis")
    df["order_date"] = pd.to_datetime(df["order_date"])
    time_df = df.groupby("order_date")["revenue"].sum().reset_index()

    fig, ax = plt.subplots(figsize=(12,5))
    sns.lineplot(data=time_df, x="order_date", y="revenue", color="teal", ax=ax)
    ax.set_title("Revenue Trend Over Time")
    st.pyplot(fig)

    # ===============================
    # Interactive Plotly Visuals
    # ===============================
    st.header("📌 Interactive Visualizations")

    st.plotly_chart(px.bar(df, x="category", y="revenue", color="category", title="Revenue by Category", text_auto=True))
    st.plotly_chart(px.pie(df, names="region", values="revenue", title="Revenue Share by Region"))
    st.plotly_chart(px.box(df, x="payment_method", y="revenue", color="payment_method", title="Revenue Distribution by Payment Method"))

    # ===============================
    # Correlation Heatmap
    # ===============================
    st.header("📌 Correlation Analysis")
    fig, ax = plt.subplots(figsize=(8,6))
    sns.heatmap(df[["quantity","price","discount","revenue"]].corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)
else:
    st.info("👆 Upload your dataset to start the EDA.")

