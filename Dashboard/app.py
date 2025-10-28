# ====================================================
# 📊 Telco Customer Churn Insights Dashboard
# ====================================================
import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Page setup
# -------------------------------
st.set_page_config(
    page_title="Telco Churn Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Custom CSS styling
# -------------------------------
st.markdown("""
    <style>
    .main {
        background-color: #f9fafc;
        color: #111;
        font-family: 'Segoe UI', sans-serif;
    }
    .kpi-box {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
        transition: 0.2s;
    }
    .kpi-box:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }
    .kpi-title {
        font-size: 16px;
        color: #666;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: bold;
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Load data
# -------------------------------
@st.cache_data
def load_data():
    path = r"C:\Users\jackk\Desktop\Desktop\Data Analysis, Engineering Projects\churn_predictor_eda\Data\WA_Fn-UseC_-Telco-Customer-Churn.csv"
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    # Normalize churn column
    if df["Churn"].dtype != "object":
        df["Churn"] = df["Churn"].map({1: "Yes", 0: "No"})
    return df

df = load_data()

# -------------------------------
# Sidebar filters
# -------------------------------
st.sidebar.title("🎛️ Filters")

gender_options = df["gender"].dropna().unique()
contract_options = df["Contract"].dropna().unique()
payment_options = df["PaymentMethod"].dropna().unique()

gender = st.sidebar.multiselect("Gender", gender_options, default=list(gender_options))
contract = st.sidebar.multiselect("Contract", contract_options, default=list(contract_options))
payment = st.sidebar.multiselect("Payment Method", payment_options, default=list(payment_options))

# Apply filters safely
filtered_df = df.copy()
if gender:
    filtered_df = filtered_df[filtered_df["gender"].isin(gender)]
if contract:
    filtered_df = filtered_df[filtered_df["Contract"].isin(contract)]
if payment:
    filtered_df = filtered_df[filtered_df["PaymentMethod"].isin(payment)]

# -------------------------------
# Header
# -------------------------------
st.title("📊 Telco Customer Churn Insights Dashboard")
st.markdown("Explore churn trends interactively — filter, visualize, and understand customer behavior.")

st.divider()

# -------------------------------
# KPI Section
# -------------------------------
total_customers = len(filtered_df)
churned = filtered_df[filtered_df["Churn"] == "Yes"].shape[0]
churn_rate = round((churned / total_customers) * 100, 2) if total_customers > 0 else 0
avg_tenure = round(filtered_df["tenure"].mean(), 1) if total_customers > 0 else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='kpi-box'><div class='kpi-title'>👥 Total Customers</div><div class='kpi-value'>{total_customers}</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='kpi-box'><div class='kpi-title'>📉 Churn Rate</div><div class='kpi-value'>{churn_rate}%</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='kpi-box'><div class='kpi-title'>⏱️ Avg Tenure (months)</div><div class='kpi-value'>{avg_tenure}</div></div>", unsafe_allow_html=True)

st.divider()

# -------------------------------
# Visual Insights
# -------------------------------
st.subheader("📈 Visual Insights")

colA, colB = st.columns(2)

# 1️⃣ Churn by Gender
with colA:
    fig_gender = px.histogram(filtered_df, x="gender", color="Churn", barmode="group",
                              title="Churn Distribution by Gender", color_discrete_sequence=["#0083B8", "#FF4B4B"])
    st.plotly_chart(fig_gender, use_container_width=True)

# 2️⃣ Churn by Contract
with colB:
    fig_contract = px.histogram(filtered_df, x="Contract", color="Churn", barmode="group",
                                title="Churn by Contract Type", color_discrete_sequence=["#0083B8", "#FF4B4B"])
    st.plotly_chart(fig_contract, use_container_width=True)

# 3️⃣ Tenure vs MonthlyCharges
st.subheader("💰 Tenure vs Monthly Charges")
fig_tenure = px.scatter(
    filtered_df,
    x="tenure", y="MonthlyCharges",
    color="Churn",
    title="Customer Tenure vs Monthly Charges",
    color_discrete_sequence=["#0083B8", "#FF4B4B"],
    hover_data=["Contract", "PaymentMethod"]
)
st.plotly_chart(fig_tenure, use_container_width=True)

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("Built by Jack — Data Analysis & Engineering Projects 💡")
