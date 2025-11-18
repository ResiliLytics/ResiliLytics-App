import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="SupplySight", layout="wide")

# ---- HEADER WITH LOGO ----
st.markdown("""
    <div style='display:flex; align-items:center; gap:1rem; padding: 1rem 0 1rem 0;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Logo_transparent.png/120px-Logo_transparent.png' style='height:60px;'>
        <div>
            <h1 style='color: #ffffff; margin: 0;'>SupplySight Dashboard</h1>
            <h3 style='color: #d0d8e8; font-weight:400; margin:0;'>AI-powered SME Resilience & Risk</h3>
        </div>
    </div>
""", unsafe_allow_html=True)

# ---- TOP ROW ----
col1, col2, col3 = st.columns([1.1, 1, 1])

with col1:
    st.markdown("#### Resilience Score")
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=68,
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#238823"},
            "steps": [
                {"range": [0, 50], "color": "#e74c3c"},
                {"range": [50, 75], "color": "#f6c542"},
                {"range": [75, 100], "color": "#43a047"},
            ],
        },
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    fig.update_layout(height=220, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### Key Metrics")
    c1, c2 = st.columns(2)
    c1.markdown("<div style='background:#f6c542; padding:1rem; border-radius:12px; color:#222; margin-bottom:6px; text-align:center;'>Supplier Concentration<br><span style='font-size:1.6em;font-weight:bold;'>57%</span></div>", unsafe_allow_html=True)
    c2.markdown("<div style='background:#228be6; padding:1rem; border-radius:12px; color:#fff; margin-bottom:6px; text-align:center;'>Geographic Exposure<br><span style='font-size:1.6em;font-weight:bold;'>15 Countries</span></div>", unsafe_allow_html=True)
    c1.markdown("<div style='background:#e74c3c; padding:1rem; border-radius:12px; color:#fff; margin-bottom:6px; text-align:center;'>Cost Volatility<br><span style='font-size:1.2em;font-weight:bold;'>Moderate</span></div>", unsafe_allow_html=True)
    c2.markdown("<div style='background:#e67e22; padding:1rem; border-radius:12px; color:#fff; margin-bottom:6px; text-align:center;'>Supply Risk<br><span style='font-size:1.2em;font-weight:bold;'>High</span></div>", unsafe_allow_html=True)

with col3:
    st.markdown("#### Recommendations")
    st.markdown("""
    <div style='background:#43a047; color:#fff; border-radius:10px; padding:1rem; margin-bottom:8px;'>✅ Evaluate alternate suppliers in East Asia</div>
    <div style='background:#f6c542; color:#111; border-radius:10px; padding:1rem; margin-bottom:8px;'>📦 Increase buffer inventory for key items</div>
    <div style='background:#228be6; color:#fff; border-radius:10px; padding:1rem; margin-bottom:8px;'>📄 Download Project Brief: Supplier Diversification</div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---- MID ROW ----
mid1, mid2, mid3 = st.columns([1, 1, 1])

with mid1:
    st.markdown("#### Risk Insights")
    fig2 = go.Figure(go.Bar(
        x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        y=[2, 4, 6, 8, 10, 14],
        marker_color="#228be6"
    ))
    fig2.update_layout(height=200, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig2, use_container_width=True)

with mid2:
    st.markdown("#### Supplier Diversification")
    fig3 = go.Figure(go.Pie(
        values=[40, 35, 25],
        labels=['Asia', 'Europe', 'Americas'],
        hole=0.6
    ))
    fig3.update_traces(marker=dict(colors=['#43a047', '#f6c542', '#228be6']))
    fig3.update_layout(showlegend=True, height=200, margin=dict(t=30, b=10, l=10, r=10))
    st.plotly_chart(fig3, use_container_width=True)

with mid3:
    st.markdown("#### Mitigation Plan")
    st.markdown("""
    <div style='background:#fff3cd; border-radius:10px; padding:1.2rem; border:1px solid #ffe066; color:#222;'>
        <b>Objective:</b> Reduce single source dependency<br>
        <b>Timeline:</b> 3–6 months<br>
        <b>Owner:</b> Supply Chain Manager<br>
        <b>KPIs:</b> Supplier mix, lead time
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---- BOTTOM: Upload Section ----
st.markdown("### Upload Your Data")
st.info("""
    <span style='color:white;'>Upload your <code>.csv</code> or <code>.xlsx</code> file below.</span>
    <a href='https://yourdomain.com/sample_template.xlsx' style='color:lightblue;' target='_blank'>Download Sample Template</a>
""", unsafe_allow_html=True)

st.file_uploader("Choose file", type=['csv', 'xlsx'])

st.caption("Beta dashboard UI preview — layout matches approved mockup. Replace demo values with calculations after layout approval.")
