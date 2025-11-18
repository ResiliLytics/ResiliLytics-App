import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import base64

st.set_page_config(layout="wide", page_title="SupplySight Dashboard")

# --- CUSTOM LOGO + HEADER ---
logo_svg = """
<svg width="40" height="40" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="45" fill="#FFD700" />
  <path d="M30 50 A20 20 0 0 1 70 50" stroke="#00BFFF" stroke-width="10" fill="none"/>
  <circle cx="50" cy="50" r="5" fill="#FF4500"/>
</svg>
"""

st.markdown(
    f"""
    <div style='display: flex; align-items: center; gap: 1rem; padding-bottom: 1rem;'>
        {logo_svg}
        <div>
            <h1 style='color: #ffffff; margin: 0;'>SupplySight Dashboard</h1>
            <h4 style='color: #cccccc; margin-top: 0.2rem;'>AI-powered SME Resilience & Risk</h4>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- METRICS MOCK DATA ---
resilience_score = 68
supplier_concentration = "57%"
cost_volatility = "Moderate"
geo_exposure = "15 Countries"
supply_risk = "High"

# --- MOCK DIVERSIFICATION DATA ---
diversification_data = {"Asia": 40, "Europe": 25, "Americas": 35}

# --- LAYOUT START ---
col1, col2, col3 = st.columns([2, 3, 3])

# --- RESILIENCE SCORE GAUGE ---
with col1:
    st.markdown("### Resilience Score")
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=resilience_score,
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "#D9534F"},
                {'range': [50, 70], 'color': "#F0AD4E"},
                {'range': [70, 100], 'color': "#5CB85C"},
            ],
        }
    ))
    fig.update_layout(height=250, margin=dict(t=30, b=10))
    st.plotly_chart(fig, use_container_width=True)

# --- KEY METRICS ---
with col2:
    st.markdown("### Key Metrics")
    st.markdown(
        """
        <div style="display: flex; flex-wrap: wrap; gap: 1rem;">
            <div style="flex: 1; background-color: #FFC107; padding: 1rem; border-radius: 8px;">
                <strong>Supplier Concentration</strong><br><span style="font-size: 1.5rem;">57%</span>
            </div>
            <div style="flex: 1; background-color: #007BFF; padding: 1rem; border-radius: 8px;">
                <strong>Geographic Exposure</strong><br><span style="font-size: 1.5rem;">15 Countries</span>
            </div>
            <div style="flex: 1; background-color: #DC3545; padding: 1rem; border-radius: 8px; color: white;">
                <strong>Cost Volatility</strong><br><span style="font-size: 1.5rem;">Moderate</span>
            </div>
            <div style="flex: 1; background-color: #FD7E14; padding: 1rem; border-radius: 8px; color: white;">
                <strong>Supply Risk</strong><br><span style="font-size: 1.5rem;">High</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- RECOMMENDATIONS ---
with col3:
    st.markdown("### Recommendations")
    st.markdown(
        """
        <ul style="list-style: none; padding-left: 0;">
            <li style="background-color: #28a745; color: white; padding: 0.5rem; margin-bottom: 0.5rem; border-radius: 6px;">
                ✅ Evaluate alternate suppliers in East Asia
            </li>
            <li style="background-color: #ffc107; color: black; padding: 0.5rem; margin-bottom: 0.5rem; border-radius: 6px;">
                📄 Increase buffer inventory for key items
            </li>
            <li style="background-color: #007bff; color: white; padding: 0.5rem; border-radius: 6px;">
                ⬇️ Download Project Brief: Supplier Diversification
            </li>
        </ul>
        """,
        unsafe_allow_html=True
    )

# --- RISK INSIGHTS ---
col4, col5, col6 = st.columns([2, 2, 3])

with col4:
    st.markdown("### Risk Insights")
    bar_fig = go.Figure()
    bar_fig.add_trace(go.Bar(x=["Jan", "Feb", "Mar", "Apr", "May", "Jun"], y=[2, 4, 6, 8, 10, 14], marker_color='dodgerblue'))
    bar_fig.update_layout(height=300, margin=dict(t=20, b=20))
    st.plotly_chart(bar_fig, use_container_width=True)

# --- SUPPLIER DIVERSIFICATION ---
with col5:
    st.markdown("### Supplier Diversification")
    pie_fig = go.Figure(data=[go.Pie(
        labels=list(diversification_data.keys()),
        values=list(diversification_data.values()),
        hole=.4
    )])
    pie_fig.update_traces(marker=dict(line=dict(color='#000000', width=1)))
    pie_fig.update_layout(height=300, showlegend=True)
    st.plotly_chart(pie_fig, use_container_width=True)

# --- MITIGATION PLAN ---
with col6:
    st.markdown("### Mitigation Plan")
    st.markdown(
        """
        <div style="background-color: #FFF3CD; color: #333; padding: 1rem; border-radius: 8px;">
            <strong>Diversify Supplier Base</strong><br>
            <em>Objective:</em> Reduce single-source dependency<br>
            <em>Timeline:</em> 3–6 months<br>
            <em>Owner:</em> Supply Chain Manager<br>
            <em>KPIs:</em> Supplier mix, lead time
        </div>
        """,
        unsafe_allow_html=True
    )

# --- FILE UPLOAD SECTION ---
st.markdown("---")
st.markdown("### Upload Your Data")

st.markdown(
    "<span style='color: #cccccc;'>Upload your .csv or .xlsx file below. <a href='#' style='color: #4da6ff;'>Download Sample Template</a></span>",
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Choose file", type=["csv", "xlsx"])
if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    st.dataframe(df)
