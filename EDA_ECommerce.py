import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("ecommerce_dataset.csv")

# Basic Info
print(df.shape)
print(df.info())
print(df.describe(include="all"))
print(df.isnull().sum())

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
fig1.show()

# Revenue by Region 
fig2 = px.pie(df, names="region", values="Revenue",
              title="🌍 Revenue Share by Region")
fig2.show()

# Monthly Revenue Trend 
monthly = df.groupby("month")['Revenue'].sum().reset_index()
fig3 = px.line(monthly, x="month", y="Revenue", markers=True,
               title="📆 Monthly Revenue Trend")
fig3.show()

# Payment Method Usage
fig4 = px.histogram(df, x="payment_method", color="payment_method",
                       title="💳 Payment Method Distribution")
fig4.show()

