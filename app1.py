import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Stroke Risk Analytics", layout="wide", page_icon="🏥")

# Title and Description
st.title("🏥Hospital Patient Data: Heart Stroke Risk Analysis")
st.markdown("(Python for Data Analysis Project)")
st.divider()

# Load Featured Data
@st.cache_data
def load_data():
    return pd.read_csv("data/featured_healthcare.csv")

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("User Controls")
age_filter = st.sidebar.slider("Select Age Range", int(df.age.min()), int(df.age.max()), (20, 80))
stroke_only = st.sidebar.checkbox("Show Stroke Patients Only")

# Apply Filters
filtered_df = df[(df['age'] >= age_filter[0]) & (df['age'] <= age_filter[1])]
if stroke_only:
    filtered_df = filtered_df[filtered_df['stroke'] == 1]

# --- KEY METRICS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Patients", len(filtered_df))
col2.metric("Avg Glucose", f"{filtered_df['avg_glucose_level'].mean():.1f} mg/dL")
col3.metric("Avg Risk Score", f"{filtered_df['risk_score'].mean():.1f}")
col4.metric("Stroke Cases", filtered_df['stroke'].sum())

# --- INTERACTIVE CHARTS ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("📍 Pattern: Glucose vs Age")
    fig = px.scatter(filtered_df, x="age", y="avg_glucose_level", color="stroke",
                     color_discrete_map={0: "teal", 1: "tomato"},
                     title="Hover to see Patient Details")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("📊 Distribution: Risk Score")
    fig2 = px.histogram(filtered_df, x="risk_score", color="stroke",
                        marginal="box", title="Risk Frequency")
    st.plotly_chart(fig2, use_container_width=True)

# --- DATA TABLE ---
st.subheader("📋 Patient Data Snapshot")
st.dataframe(filtered_df.head(100), use_container_width=True)

st.success("Dashboard ready for presentation!")
