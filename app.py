# SupplySight Updated Streamlit App
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(page_title="SupplySight Dashboard", layout="wide")

# ---------- Sample Resilience Score Gauge ----------
resilience_score = 68

fig_gauge = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = resilience_score,
    title = {'text': "Resilience Score"},
    gauge = {
        'axis': {'range': [0, 100]},
        'bar': {'color': "darkblue"},
        'steps': [
            {'range': [0, 50], 'color': 'tomato'},
            {'range': [50, 75], 'color': 'gold'},
            {'range': [75, 100], 'color': 'lightgreen'}
        ]
    }))

# ---------- Key Metrics Cards ----------
def metric_card(title, value, color):
    st.markdown(f"""
        <div style='background-color:{color}; padding: 1rem; border-radius: 10px; text-align:center'>
            <h4 style='color:white'>{title}</h4>
            <h2 style='color:white'>{value}</h2>
        </div>
    """, unsafe_allow_html=True)

# ---------- Risk Insights Bar Chart ----------
risk_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
risk_values = [2, 4, 6, 8, 10, 14]
fig_risk = go.Figure([go.Bar(x=risk_months, y=risk_values, marker_color='dodgerblue')])
fig_risk.update_layout(title="Risk Insights", margin=dict(t=30))

# ---------- Supplier Diversification ----------
fig_div1 = go.Figure(go.Pie(values=[50, 50], labels=["Diversified", "Concentrated"], hole=0.5))
fig_div2 = go.Figure(go.Pie(values=[40, 30, 30], labels=["Asia", "Europe", "Americas"], hole=0.5))

# ---------- Recommendations Panel ----------
def recommendation_card(text, color):
    st.markdown(f"""
        <div style='background-color:{color}; padding: 1rem; border-radius: 10px; margin-bottom: 0.5rem;'>
            <b style='color:white'>{text}</b>
        </div>
    """, unsafe_allow_html=True)

# ---------- Mitigation Plan ----------
def mitigation_plan():
    st.markdown("""
        <div style='background-color:#FCD440; padding: 1rem; border-radius: 10px;'>
            <h4>📌 <b>Diversify Supplier Base</b></h4>
            <ul>
                <li><b>Objective:</b> Reduce single-source dependency</li>
                <li><b>Timeline:</b> 3–6 months</li>
                <li><b>Owner:</b> Supply Chain Manager</li>
                <li><b>KPIs:</b> Supplier mix, lead time</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# ---------- Layout ----------
st.title("📊 SupplySight: AI-Powered Resilience Dashboard")

col1, col2, col3 = st.columns([1, 1, 1])
col1.plotly_chart(fig_gauge, use_container_width=True)
with col2:
    metric_card("Supplier Concentration", "57%", "#F9A825")
    metric_card("Cost Volatility", "Moderate", "#EF6C00")
with col3:
    metric_card("Geographic Exposure", "15 Countries", "#0288D1")
    metric_card("Supply Risk", "High", "#D32F2F")

col4, col5, col6 = st.columns([1, 1, 1])
col4.plotly_chart(fig_risk, use_container_width=True)
col5.plotly_chart(fig_div1, use_container_width=True)
col6.plotly_chart(fig_div2, use_container_width=True)

st.subheader("✅ Recommendations")
recommendation_card("Evaluate alternate suppliers in East Asia", "#43A047")
recommendation_card("Increase buffer inventory for key items", "#FB8C00")
recommendation_card("Download Project Brief: Supplier Diversification", "#1E88E5")

st.subheader("📁 Mitigation Plan")
mitigation_plan()

# ---------- File Upload & Template ----------
with st.sidebar:
    st.header("Upload Your Data")
    uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])
    st.markdown("[📄 Download Sample Template](https://example.com/template.xlsx)")

    if uploaded_file:
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.write("### Preview Uploaded Data")
        st.dataframe(df.head())
