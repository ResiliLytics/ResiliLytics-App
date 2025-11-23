import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.set_page_config(page_title="SupplySight", layout="wide")

# ---- HEADER ----
st.markdown("""
    <div style='text-align: center; padding: 0.5rem 0 0rem 0;'>
        <img src='https://raw.githubusercontent.com/AuraFusion/supplysight-assets/main/logo.png' alt='SupplySight Logo' width='360' style='margin-bottom:-150px;'/>
        <h1 style='color: #ffffff; margin-bottom: .2rem; margin-top: -0.2rem;'>SupplySight Dashboard</h1>
        <h3 style='color: #bbbbbb; font-weight:400; margin-top: -0.5rem;'>AI-powered SME Resilience & Risk</h3>
    </div>
""", unsafe_allow_html=True)

# ---- UPLOAD SECTION ----
st.markdown("### Upload Your Data")
uploaded_file = st.file_uploader("Choose a .csv or .xlsx file", type=['csv', 'xlsx'])
st.markdown("""
<div style='color:#ccc; font-size:0.95rem;'>
    Upload your .csv or .xlsx file with columns: Supplier, Country, Spend, Cost_Per_Unit, Historical_Costs<br>
    <a href='/mnt/data/sample_template.xlsx' style='color:#91caff;'>Download Sample Template</a>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)

    total_spend = df['Spend'].sum()
    top_supplier_pct = df.groupby('Supplier')['Spend'].sum().max() / total_spend * 100
    num_countries = df['Country'].nunique()

    def compute_volatility(row):
        try:
            prices = list(map(float, str(row['Historical_Costs']).split(';')))
            return np.std(prices)
        except:
            return np.nan

    df['Volatility'] = df.apply(compute_volatility, axis=1)
    avg_volatility = df['Volatility'].mean()

    resilience_score = max(0, 100 - top_supplier_pct - (avg_volatility * 10))
    supply_risk = "High" if top_supplier_pct > 50 or avg_volatility > 0.5 else "Moderate" if avg_volatility > 0.3 else "Low"
    volatility_level = "High" if avg_volatility > 0.5 else "Moderate" if avg_volatility > 0.3 else "Low"
    risk_color = "#e74c3c" if supply_risk == "High" else "#e67e22" if supply_risk == "Moderate" else "#43a047"

    # ---- TOP ROW ----
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
            },
        ))
        fig.update_layout(height=220, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Key Metrics")
        c1, c2 = st.columns(2)
        c1.markdown(f"<div style='background:#f6c542; padding:1rem; border-radius:10px; color:#222; text-align:center;'>Supplier Concentration<br><span style='font-size:1.6em;font-weight:bold;'>{top_supplier_pct:.1f}%</span></div>", unsafe_allow_html=True)
        c2.markdown(f"<div style='background:#228be6; padding:1rem; border-radius:10px; color:#fff; text-align:center;'>Geographic Exposure<br><span style='font-size:1.6em;font-weight:bold;'>{num_countries} Countries</span></div>", unsafe_allow_html=True)
        c1.markdown(f"<div style='background:#e74c3c; padding:1rem; border-radius:10px; color:#fff; text-align:center;'>Cost Volatility<br><span style='font-size:1.2em;font-weight:bold;'>{volatility_level}</span></div>", unsafe_allow_html=True)
        c2.markdown(f"<div style='background:{risk_color}; padding:1rem; border-radius:10px; color:#fff; text-align:center;'>Supply Risk<br><span style='font-size:1.2em;font-weight:bold;'>{supply_risk}</span></div>", unsafe_allow_html=True)

    with col3:
        st.markdown("#### Recommendations")
        st.markdown("""
        <div style='background:#43a047; color:#fff; border-radius:10px; padding:1rem; margin-bottom:8px;'>✅ Evaluate alternate suppliers in East Asia</div>
        <div style='background:#f6c542; color:#111; border-radius:10px; padding:1rem; margin-bottom:8px;'>📦 Increase buffer inventory for key items</div>
        <div style='background:#228be6; color:#fff; border-radius:10px; padding:1rem; margin-bottom:8px;'>📄 Download Project Brief: Supplier Diversification</div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.dataframe(df.head())
else:
    st.markdown("<div style='color:#ffffff; font-size:1.1rem; font-weight:600;'>Please upload a file to view dynamic metrics.</div>", unsafe_allow_html=True)

st.markdown("### Dashboard Preview")
st.image("https://github.com/AuraFusion/supplysight-assets/blob/6f8185ac2c43f3798cf019254a8ad64bd1b2e007/Final%20Dashboard%20Sample.png", caption="This is what your dashboard will look like after upload", use_column_width=True)






