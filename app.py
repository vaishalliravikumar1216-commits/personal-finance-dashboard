import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Personal Finance Dashboard",
    page_icon="💰",
    layout="wide"
)

# Title
st.title("💰 Personal Finance Dashboard")
st.markdown("Track your spending patterns and stay on top of your budget.")
st.divider()

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/expenses.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.strftime('%B %Y')
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
categories = st.sidebar.multiselect(
    "Select Categories",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

months = st.sidebar.multiselect(
    "Select Month",
    options=df['Month'].unique(),
    default=df['Month'].unique()
)

filtered_df = df[
    (df['Category'].isin(categories)) &
    (df['Month'].isin(months))
]

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Spent", f"₹{filtered_df['Amount'].sum():,.0f}")

with col2:
    st.metric("Avg per Transaction", f"₹{filtered_df['Amount'].mean():,.0f}")

with col3:
    st.metric("Highest Expense", f"₹{filtered_df['Amount'].max():,.0f}")

with col4:
    st.metric("Total Transactions", len(filtered_df))

st.divider()

# Charts Row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("Spending by Category")
    cat_data = filtered_df.groupby('Category')['Amount'].sum().reset_index()
    fig1 = px.pie(cat_data, values='Amount', names='Category',
                  hole=0.4, color_discrete_sequence=px.colors.qualitative.Set3)
    fig1.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Monthly Spending Trend")
    month_data = filtered_df.groupby('Month')['Amount'].sum().reset_index()
    fig2 = px.bar(month_data, x='Month', y='Amount',
                  color='Amount', color_continuous_scale='Blues',
                  text='Amount')
    fig2.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
    st.plotly_chart(fig2, use_container_width=True)

# Charts Row 2
col3, col4 = st.columns(2)

with col3:
    st.subheader("Category-wise Monthly Breakdown")
    pivot = filtered_df.groupby(['Month', 'Category'])['Amount'].sum().reset_index()
    fig3 = px.bar(pivot, x='Month', y='Amount', color='Category',
                  barmode='group', color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("Spending Over Time")
    fig4 = px.line(filtered_df.sort_values('Date'), x='Date', y='Amount',
                   color='Category', markers=True)
    st.plotly_chart(fig4, use_container_width=True)

# Data Table
st.subheader("Transaction Details")
st.dataframe(filtered_df.sort_values('Date', ascending=False), use_container_width=True)