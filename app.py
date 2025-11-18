import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ----------- Page Setup ----------- #
st.set_page_config(page_title="SupplySight Dashboard", layout="wide")
st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
        }
        .title {
            font-size: 2rem;
            font-weight: bold;
        }
        .tile {
            padding: 1rem;
            border-radius: 10px;
            color: white;
            font-weight: bold;
            text-align: center;
        }
        .red {background-color: #e74c3c;}
        .green {background-color: #27ae60;}
        .orange {background-color: #f39c12;}
        .blue {background-color: #3498db;}
    </style>
""", unsafe_allow_html=True)

# ----------- Header ----------- #
st.markdown("<h1 style='color:#FF5733'>SupplySight</h1>", unsafe_allow_html=True)
st.markdown("<h4>AI-Driven Resilience & Action Engine for SMEs</h4>")
st.markdown("---")

# ----------- Row 1: Score, Metrics, Recommendations ----------- #
col1, col2, col3 = st.columns([1.2, 1.2, 1])

# Resilience Score
with col1:
    st.subheader("Resilience Score")
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = 68,
        gauge = {'axis': {'range': [0,100]},
                 'bar': {'color': "#2ecc71"},
                 'steps' : [
                     {'range': [0, 50], 'color': "#e74c3c"},
                     {'range': [50, 75], 'color': "#f39c12"},
                     {'range': [75, 100], 'color': "#2ecc71"}],},
        domain = {'x': [0, 1], 'y': [0, 1]}
    ))
    fig.update_layout(height=250, margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)

# Key Metrics
with col2:
    st.subheader("Key Metrics")
    colA, colB = st.columns(2)
    with colA:
        st.markdown("<div class='tile orange'>Supplier Concentration<br>57%</div>", unsafe_allow_html=True)
        st.markdown("<div class='tile blue'>Geographic Exposure<br>15 Countries</div>", unsafe_allow_html=True)
    with colB:
        st.markdown("<div class='tile red'>Cost Volatility<br>Moderate</div>", unsafe_allow_html=True)
        st.markdown("<div class='tile red'>Supply Risk<br>High</div>", unsafe_allow_html=True)

# Recommendations
with col3:
    st.subheader("Recommendations")
    st.success("✅ Evaluate alternate suppliers in East Asia")
    st.warning("📦 Increase buffer inventory for key items")
    st.info("📄 [Download Project Brief: Supplier Diversification](https://example.com/projectbrief.pdf)")

# ----------- Row 2: Charts & Mitigation ----------- #
col4, col5 = st.columns([1.2, 1])

# Risk Insights (Bar Chart)
with col4:
    st.subheader("Risk Insights")
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    values = [2, 4, 6, 8, 10, 14]
    fig2 = go.Figure(data=[go.Bar(x=months, y=values, marker_color="#3498db")])
    fig2.update_layout(height=250, margin=dict(t=10, b=10, l=10, r=10))
    st.plotly_chart(fig2, use_container_width=True)

# Supplier Diversification (Donut Charts)
    st.subheader("Supplier Diversification")
    fig3 = go.Figure()
    fig3.add_trace(go.Pie(labels=['Diversified', 'Concentrated'], values=[50, 50], hole=0.6))
    fig3.update_traces(marker=dict(colors=['#2ecc71','#95a5a6']), textinfo='label+percent')
    fig3.update_layout(height=250, margin=dict(t=10, b=10, l=10, r=10))
    st.plotly_chart(fig3, use_container_width=True)

# Mitigation Plan
with col5:
    st.subheader("Mitigation Plan")
    st.markdown("""
    <div style='padding: 1rem; border-radius: 10px; background-color: #f1c40f;'>
        <h4>📌 Diversify Supplier Base</h4>
        <ul>
            <li><strong>Objective:</strong> Reduce single-source dependency</li>
            <li><strong>Timeline:</strong> 3–6 months</li>
            <li><strong>Owner:</strong> Supply Chain Manager</li>
            <li><strong>KPIs:</strong> Supplier mix, lead time</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# File Upload Section
st.markdown("---")
st.subheader("Upload Your Supply Data")
uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=['csv', 'xlsx'])
if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")

# Template Download
st.markdown("📥 [Download Sample Data Template](https://example.com/sample_template.xlsx)")
