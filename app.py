# SupplySight: AI-Powered SME Resilience Dashboard

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="SupplySight Dashboard", layout="wide")

# Header
st.markdown("""
    <div style='background: linear-gradient(to right, #f12711, #f5af19); padding: 1.5rem; border-radius: 8px;'>
        <h1 style='color: white; margin-bottom: 0;'>📊 SupplySight</h1>
        <p style='color: white; margin-top: 0;'>AI-Driven Resilience & Action Engine for SMEs</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# File Upload
with st.sidebar:
    st.header("Upload Data")
    uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])
    with open("sample_data.csv", "w") as f:
        f.write("Supplier,Country,Spend,LeadTime\nABC Inc,USA,50000,30\nXYZ Ltd,China,30000,45")
    with open("sample_data.csv", "rb") as file:
        st.download_button("📥 Download Sample Template", file, file_name="sample_data.csv")

# Dummy risk score and metrics
resilience_score = 68
supplier_concentration = 57
geo_exposure = 15
supply_risk = "High"
cost_volatility = "Moderate"

# Layout setup
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.subheader("Resilience Score")
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=resilience_score,
        title={'text': "Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 50], 'color': "#ff4d4d"},
                {'range': [50, 75], 'color': "#ffcc00"},
                {'range': [75, 100], 'color': "#28a745"}
            ]
        }))
    st.plotly_chart(fig_gauge, use_container_width=True)

with col2:
    st.subheader("Key Metrics")
    st.markdown("""
        <div style='display: flex; flex-wrap: wrap; gap: 10px;'>
            <div style='flex: 1; padding: 10px; background-color: #ffcc80; border-radius: 8px;'>
                <b>Supplier Concentration</b><br>57%
            </div>
            <div style='flex: 1; padding: 10px; background-color: #ef9a9a; border-radius: 8px;'>
                <b>Cost Volatility</b><br>Moderate
            </div>
            <div style='flex: 1; padding: 10px; background-color: #90caf9; border-radius: 8px;'>
                <b>Geographic Exposure</b><br>15 Countries
            </div>
            <div style='flex: 1; padding: 10px; background-color: #ef5350; border-radius: 8px;'>
                <b>Supply Risk</b><br>High
            </div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.subheader("Recommendations")
    st.markdown("""
        <ul style='list-style-type: none;'>
            <li>🌍 Evaluate alternate suppliers in East Asia</li>
            <li>📦 Increase buffer inventory for key items</li>
            <li>📄 <a href='#' download style='color: #1f77b4;'>Download Project Brief</a></li>
        </ul>
    """, unsafe_allow_html=True)

st.markdown("---")

# Risk Insights (Dummy bar chart)
st.subheader("📈 Risk Insights")
fig_risk = go.Figure()
fig_risk.add_trace(go.Bar(x=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                          y=[2, 4, 6, 8, 10, 14],
                          marker_color="#1f77b4"))
fig_risk.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0))
st.plotly_chart(fig_risk, use_container_width=True)

# Supplier Diversification (Dummy donut)
col4, col5 = st.columns(2)
with col4:
    st.subheader("Supplier Diversification")
    fig_donut = go.Figure(data=[
        go.Pie(labels=["A", "B", "C", "D"], values=[40, 20, 25, 15], hole=.5)
    ])
    fig_donut.update_traces(marker=dict(colors=["#FFA07A", "#20B2AA", "#87CEFA", "#FF69B4"]))
    st.plotly_chart(fig_donut, use_container_width=True)

# Mitigation Plan
with col5:
    st.subheader("Mitigation Plan")
    st.markdown("""
        <div style='background-color: #ffeb99; padding: 1rem; border-radius: 10px;'>
            <b>🛠️ Diversify Supplier Base</b><br>
            <ul>
                <li><b>Objective:</b> Reduce single-source dependency</li>
                <li><b>Timeline:</b> 3–6 months</li>
                <li><b>Owner:</b> Supply Chain Manager</li>
                <li><b>KPIs:</b> Supplier mix, lead time</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("🔒 Beta version for testing. All data remains confidential.")
