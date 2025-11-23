import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.set_page_config(page_title="SupplySight", layout="wide")

# ---- HEADER ----
st.markdown("""
    <div style='text-align: center; padding: 1rem 0 .25rem 0;'>
        <img src='https://raw.githubusercontent.com/AuraFusion/SupplySight/main/logo.png' alt='SupplySight Logo' width='90' style='margin-bottom:-8px;'/>
        <h1 style='color: #ffffff;'>SupplySight Dashboard</h1>
        <h3 style='color: #bbbbbb; font-weight:400;'>AI-powered SME Resilience & Risk</h3>
    </div>
""", unsafe_allow_html=True)

# ---- UPLOAD SECTION ----
st.markdown("### Upload Your Data")
uploaded_file = st.file_uploader("Choose a .csv or .xlsx file", type=['csv', 'xlsx'])
st.markdown("""
<div style='color:#ccc; font-size:0.95rem; margin-bottom:1rem;'>
    Upload your file with columns: <b>Supplier, Country, Spend, Cost_Per_Unit, Historical_Costs</b><br>
    <a href='https://aurafusion-supplysight.streamlit.app/SupplySight_Sample_Template.xlsx' style='color:#91caff;'>Download Sample Template</a>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)

    # ---- METRIC CALCULATIONS ----
    total_spend = df['Spend'].sum()

    top_supplier_pct = df.groupby('Supplier')['Spend'].sum().max() / total_spend * 100
    num_countries = df['Country'].nunique()

    # Cost Volatility: Average std dev of historical costs
    def compute_volatility(row):
        try:
            prices = list(map(float, str(row['Historical_Costs']).split(';')))
            return np.std(prices)
        except:
            return np.nan

    df['Volatility'] = df.apply(compute_volatility, axis=1)
    avg_volatility = df['Volatility'].mean()

    # Define thresholds
    resilience_score = max(0, 100 - top_supplier_pct - (avg_volatility * 10))

    supply_risk = "High" if top_supplier_pct > 50 or avg_volatility > 0.5 else "Moderate" if avg_volatility > 0.3 else "Low"
    volatility_level = "High" if avg_volatility > 0.5 else "Moderate" if avg_volatility > 0.3 else "Low"

    # ---- VISUALS ----
    col1, col2, col3 = st.columns([1.1, 1, 1])

    with col1:
        st.markdown("#### Resilience Score")
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=resilience_score,
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#238823"},
                "steps": [
                    {"range": [0, 50], "color": "#e74c3c"},
                    {"range": [50, 75], "color": "#f6c542"},
                    {"range": [75, 100], "color": "#43a047"},
                ],
            }
        ))
        fig.update_layout(height=220, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Key Metrics")
        c1, c2 = st.columns(2)
        c1.markdown(f"<div style='background:#f6c542; padding:1rem; border-radius:10px; color:#222; text-align:center;'>Supplier Concentration<br><span style='font-size:1.6em;font-weight:bold;'>{top_supplier_pct:.1f}%</span></div>", unsafe_allow_html=True)
        c2.markdown(f"<div style='background:#228be6; padding:1rem; border-radius:10px; color:#fff; text-align:center;'>Geographic Exposure<br><span style='font-size:1.6em;font-weight:bold;'>{num_countries} Countries</span></div>", unsafe_allow_html=True)
        c1.markdown(f"<div style='background:#e74c3c; padding:1rem; border-radius:10px; color:#fff; text-align:center;'>Cost Volatility<br><span style='font-size:1.2em;font-weight:bold;'>{volatility_level}</span></div>", unsafe_allow_html=True)
        risk_color = "#e74c3c" if supply_risk == "High" else "#e67e22" if supply_risk == "Moderate" else "#43a047"
        c2.markdown(f"<div style='background:{risk_color}; padding:1rem; border-radius:10px; color:#fff; text-align:center;'>Supply Risk<br><span style='font-size:1.2em;font-weight:bold;'>{supply_risk}</span></div>", unsafe_allow_html=True)

    with col3:
        st.markdown("#### Recommendations")
        st.markdown("""
        <div style='background:#43a047; color:#fff; border-radius:10px; padding:1rem; margin-bottom:8px;'>✅ Evaluate alternate suppliers in East Asia</div>
        <div style='background:#f6c542; color:#111; border-radius:10px; padding:1rem; margin-bottom:8px;'>📦 Increase buffer inventory for key items</div>
        <div style='background:#228be6; color:#fff; border-radius:10px; padding:1rem; margin-bottom:8px;'>📄 Download Project Brief: Supplier Diversification</div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Optional: preview data
    st.markdown("### Preview Uploaded Data")
    st.dataframe(df.head())
else:
    st.info("Please upload a file to view dynamic metrics.")
