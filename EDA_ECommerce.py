import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio

# -------------------------
# Global theme + colorway
# -------------------------
# choose a palette: e.g., px.colors.qualitative.Vivid, Bold, Pastel, Set2, Prism, etc.
colorway = px.colors.qualitative.Vivid

# set template default (nice options: "plotly", "plotly_dark", "ggplot2", "seaborn", ...)
pio.templates.default = "plotly_dark"

# ensure the template uses our colorway (robust)
pio.templates[pio.templates.default].layout.colorway = colorway

# also set px.defaults so new px figures pick them up
px.defaults.template = pio.templates.default
px.defaults.color_discrete_sequence = colorway

# optional: show what defaults are (for debugging)
st.write("Plotly template:", pio.templates.default)
st.write("px.defaults:", {k: v for k, v in px.defaults.items() if k in ("template", "color_discrete_sequence")})

# -------------------------
# App header + load data
# -------------------------
st.title("📊 EDA - Ecommerce Dataset (with global theme)")

df = pd.read_csv("ecommerce_dataset.csv")
df['order_date'] = pd.to_datetime(df['order_date'])
if df['discount'].max() > 1:
    df['Revenue'] = df['quantity'] * df['price'] * (1 - df['discount']/100)
else:
    df['Revenue'] = df['quantity'] * df['price'] * (1 - df['discount'])
df['month'] = df['order_date'].dt.to_period("M").astype(str)

st.write("Dataset shape:", df.shape)
st.write(df.head())

# -------------------------
# Figures
# -------------------------
# 1) Revenue by Category (categorical -> uses colorway)
fig1 = px.bar(
    df.groupby("category")['Revenue'].sum().reset_index(),
    x="category", y="Revenue", color="category",
    title="📦 Revenue by Category", text_auto=True
)
# reinforce colorway on the figure level if needed
fig1.update_layout(colorway=colorway)
st.plotly_chart(fig1, use_container_width=True)

# 2) Revenue by Region (pie -> categorical -> uses colorway)
fig2 = px.pie(df, names="region", values="Revenue", title="🌍 Revenue Share by Region")
fig2.update_layout(colorway=colorway)
st.plotly_chart(fig2, use_container_width=True)

# 3) Monthly Revenue Trend (single series — set the line color explicitly)
monthly = df.groupby("month")['Revenue'].sum().reset_index().sort_values("month")
fig3 = px.line(monthly, x="month", y="Revenue", markers=True, title="📆 Monthly Revenue Trend")
# single-line: force the color to the first color in our colorway
fig3.update_traces(line=dict(color=colorway[0], width=3), marker=dict(size=6))
fig3.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig3, use_container_width=True)

# 4) Payment Method Usage
fig4 = px.histogram(df, x="payment_method", color="payment_method",
                    title="💳 Payment Method Distribution", barmode="group")
fig4.update_layout(colorway=colorway)
st.plotly_chart(fig4, use_container_width=True)
