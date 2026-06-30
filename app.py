import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Sales & Revenue Dashboard", layout="wide")
@st.cache_data
def load_data():
    df = pd.read_csv('sales.csv', parse_dates=['OrderDate'])
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    df['Month'] = df['OrderDate'].dt.to_period('M').astype(str)
    df['Year'] = df['OrderDate'].dt.year
    return df
df = load_data()
st.sidebar.header("Filters")
regions = st.sidebar.multiselect("Region", df['Region'].unique(), default=df['Region'].unique())
categories = st.sidebar.multiselect("Category", df['Category'].unique(), default=df['Category'].unique())
years = st.sidebar.multiselect("Year", sorted(df['Year'].unique()), default=sorted(df['Year'].unique()))
df_filtered = df[df['Region'].isin(regions) & df['Category'].isin(categories) & df['Year'].isin(years)]
st.title("JPMC Task 2: Sales & Revenue Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales Units", f"{df_filtered['Quantity'].sum():,}")
col2.metric("Total Revenue", f"${df_filtered['Revenue'].sum():,.0f}")
col3.metric("Avg Order Value", f"${df_filtered['Revenue'].mean():,.0f}")
colA, colB = st.columns(2)
with colA: st.plotly_chart(px.line(df_filtered.groupby('Month')['Revenue'].sum().reset_index(), x='Month', y='Revenue', title='Revenue Trend'), use_container_width=True)
with colB: st.plotly_chart(px.bar(df_filtered.groupby('Product')['Revenue'].sum().nlargest(5).reset_index(), x='Product', y='Revenue', title='Top 5 Products'), use_container_width=True)
colC, colD = st.columns(2)
with colC: st.plotly_chart(px.pie(df_filtered.groupby('Region')['Revenue'].sum().reset_index(), names='Region', values='Revenue', title='Revenue by Region'), use_container_width=True)
with colD: st.plotly_chart(px.bar(df_filtered.groupby('Category')['Revenue'].sum().reset_index(), x='Category', y='Revenue', title='Revenue by Category'), use_container_width=True)
