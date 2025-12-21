import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(layout="wide")

# --- PAGE TABS ---
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "❓ Help & FAQ", "📬 Contact"])

# === TAB 1: DASHBOARD ===
with tab1:
    st.markdown("<h1 style='text-align:center;'>ResiliLytics Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center; color: gray;'>Sourcing Intelligence for Resilient Supply Chains</h4>", unsafe_allow_html=True)

    st.markdown("""
    ### 📂 Upload Your Data
    Upload your **.csv** or **.xlsx** file and review your resilience profile instantly.
    
    [📥 Download Sample Template](https://github.com/ResiliLytics/ResiliLytics-App/raw/main/sample%20supplier%20template.xlsx)
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choose a .csv or .xlsx file", type=['csv', 'xlsx'], key="main_data_upload")

    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)

        # --- Preprocessing ---
        df['Spend'] = pd.to_numeric(df['Spend'], errors='coerce')
        df['Country'] = df['Country'].astype(str)
        total_spend = df['Spend'].sum()
        top_supplier_pct = df.groupby('Supplier')['Spend'].sum().max() / total_spend * 100
        num_countries = df['Country'].nunique()

        # --- Volatility Calculation ---
        def compute_volatility(row):
            try:
                prices = list(map(float, str(row['Historical_Costs']).split(';')))
                return np.std(prices)
            except:
                return np.nan

        df['Volatility'] = df.apply(compute_volatility, axis=1)
        avg_volatility = df['Volatility'].mean()

        # --- Resilience Score ---
        resilience_score = max(0, 100 - top_supplier_pct - (avg_volatility * 10))

        # --- Risk Level ---
        supply_risk = "High" if top_supplier_pct > 50 or avg_volatility > 0.5 else "Moderate" if avg_volatility > 0.3 else "Low"
        volatility_level = "High" if avg_volatility > 0.5 else "Moderate" if avg_volatility > 0.3 else "Low"
        risk_color = "#e74c3c" if supply_risk == "High" else "#e67e22" if supply_risk == "Moderate" else "#43a047"

        # --- Row 1 ---
        col1, col2, col3 = st.columns([1.1, 1.2, 1])

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
                    ]
                }
            ))
            fig.update_layout(height=250, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### Key Metrics")
            c1, c2 = st.columns(2)
            c1.markdown(f"""
                <div style='background:#f6c542; padding:1rem; border-radius:10px; color:#222; text-align:center;'>
                Supplier Concentration<br><span style='font-size:1.6em;font-weight:bold;'>{top_supplier_pct:.1f}%</span></div>
            """, unsafe_allow_html=True)
            c2.markdown(f"""
                <div style='background:#228be6; padding:1rem; border-radius:10px; color:#fff; text-align:center;'>
                Geographic Exposure<br><span style='font-size:1.6em;font-weight:bold;'>{num_countries} Countries</span></div>
            """, unsafe_allow_html=True)
            c1.markdown(f"""
                <div style='background:#e74c3c; padding:1rem; border-radius:10px; color:#fff; text-align:center;'>
                Cost Volatility<br><span style='font-size:1.2em;font-weight:bold;'>{volatility_level}</span></div>
            """, unsafe_allow_html=True)
            c2.markdown(f"""
                <div style='background:{risk_color}; padding:1rem; border-radius:10px; color:#fff; text-align:center;'>
                Supply Risk<br><span style='font-size:1.2em;font-weight:bold;'>{supply_risk}</span></div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("#### Recommendations")
            st.markdown("""
                <div style='background:#43a047; color:#fff; border-radius:10px; padding:1rem; margin-bottom:8px;'>✅ Evaluate alternate suppliers in East Asia</div>
                <div style='background:#f6c542; color:#111; border-radius:10px; padding:1rem; margin-bottom:8px;'>📦 Increase buffer inventory for key items</div>
                <div style='background:#228be6; color:#fff; border-radius:10px; padding:1rem; margin-bottom:8px;'>📄 Download Project Brief: Supplier Diversification</div>
            """, unsafe_allow_html=True)

        # --- Row 2: Risk Insights | Pie | Mitigation ---
        st.markdown("### Risk Insights | Supplier Diversification | Mitigation Plan")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("##### 📊 Risk Insights")
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df['Month'] = df['Date'].dt.strftime('%b')
            df['Risk_Alert'] = df['Volatility'] > 0.5
            risk_counts = df[df['Risk_Alert']].groupby('Month').size()
            months_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
            risk_counts = risk_counts.reindex(months_order, fill_value=0)
            fig_risk = go.Figure(data=[go.Bar(x=risk_counts.index, y=risk_counts.values, marker_color='#228be6')])
            fig_risk.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_risk, use_container_width=True)

        with col2:
            st.markdown("##### 🌍 Supplier Diversification")
            region_map = {
                "China": "Asia", "Japan": "Asia", "India": "Asia", "Vietnam": "Asia",
                "USA": "Americas", "Canada": "Americas", "Mexico": "Americas",
                "Germany": "Europe", "France": "Europe", "UK": "Europe", "Italy": "Europe"
            }
            df['Region'] = df['Country'].map(region_map).fillna("Other")
            region_breakdown = df.groupby("Region")["Spend"].sum()
            fig_donut = go.Figure(data=[go.Pie(labels=region_breakdown.index, values=region_breakdown.values, hole=0.5)])
            fig_donut.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_donut, use_container_width=True)

        with col3:
            st.markdown("##### 🛡️ Mitigation Plan")
            objective = "Reduce single-source dependency" if top_supplier_pct > 50 else "Diversify supplier base"
            mitigation_html = f"""
            <div style="background-color:#f8f9fa; padding:1.5rem; border-radius:12px; color:#000; border:1px solid #ccc;">
                <p><strong>🎯 Objective:</strong> {objective}</p>
                <p><strong>📅 Timeline:</strong> 3 – 8 months</p>
                <p><strong>👤 Owner:</strong> Supply Chain Manager</p>
                <p><strong>📊 KPIs:</strong> Supplier mix, lead time, risk reduction</p>
            </div>
            """
            st.markdown(mitigation_html, unsafe_allow_html=True)

# === TAB 2: HELP & FAQ ===
with tab2:
    st.markdown("## ❓ Help & FAQ")
    st.markdown("""
    **Q: What file formats are supported?**  
    A: You can upload .csv or .xlsx files containing supplier data.

    **Q: What are the required columns?**  
    A: 'Supplier', 'Spend', 'Country', 'Historical_Costs', 'Date'

    **Q: What does Resilience Score mean?**  
    A: It's a composite indicator based on supplier concentration and volatility.
    """)

# === TAB 3: CONTACT ===
with tab3:
    st.markdown("## 📬 Contact Us")
    st.markdown("""
    If you have questions, suggestions, or need support, fill the form below:
    """)
    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message")
        submitted = st.form_submit_button("Send")
        if submitted:
            st.success("Thank you! Your message has been received.")
