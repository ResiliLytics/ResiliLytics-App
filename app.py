import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="ResiliLytics", layout="wide")

# --- Styling ---
st.markdown("""
<style>
@keyframes scroll-left {
  0% { transform: translateX(100%); }
  100% { transform: translateX(-100%); }
}
.scrolling-banner {
  width: 100%;
  background: #003f50;
  padding: 0.5rem 0;
  overflow: hidden;
  white-space: nowrap;
  box-sizing: border-box;
}
.scrolling-text {
  display: inline-block;
  color: #ffffff;
  font-size: 0.88rem;
  font-weight: 500;
  animation: scroll-left 18s linear infinite;
}
.scrolling-banner:hover .scrolling-text {
  animation-play-state: paused;
}
</style>
<div class="scrolling-banner">
  <div class="scrolling-text">
    🔎 Note: This tool is part of a non-commercial academic research project. See disclaimer below.
  </div>
</div>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div style='display: flex; align-items: center; background-color: #0e1117; padding: 1rem; border-radius: 10px; margin-bottom: 3rem;'>
    <img src='https://github.com/ResiliLytics/ResiliLytics-assets/blob/d3dc6cd2011816b6fe359d1867b286f4e7b07fa4/Logo%204.png?raw=true' width='120' style='margin-right: 20px;'/>
    <div>
        <h1 style='color: #fdf6e3; font-size: 3.5rem; margin: 0;'>ResiliLytics Dashboard</h1>
        <h3 style='color: #e0e0e0; font-weight: 400; margin-top: -0.95rem;'>Sourcing Intelligence for Resilient Supply Chains</h3>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["Dashboard", "Help & FAQ", "Contact"])

# --------------- TAB 1: Dashboard ---------------
if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)

    # --- Clean & Compute ---
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

    # --------- Risk Insights, Supplier Diversification, Mitigation Plan ----------
    st.markdown("### 📊 Risk Insights | 🌍 Supplier Diversification | 🛡️ Mitigation Plan")
    col1, col2, col3 = st.columns([1, 1, 1])

    # --- 📊 Risk Insights ---
    with col1:
        st.markdown("##### 📊 Risk Insights")
        try:
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                df['Month'] = df['Date'].dt.strftime('%b')
                alerts_per_month = df['Month'].value_counts().reindex(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], fill_value=0)
            else:
                df['Alert'] = (df['Volatility'] > 0.5) | (df['Spend'] > (0.5 * df['Spend'].max()))
                alerts_per_month = df['Alert'].value_counts().rename(index={True: 'Alerts', False: 'No Alerts'})

            fig_risk = go.Figure(data=[go.Bar(
                x=alerts_per_month.index, 
                y=alerts_per_month.values,
                marker_color='#228be6'
            )])
            fig_risk.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_risk, use_container_width=True)
        except Exception as e:
            st.warning("Unable to generate dynamic chart. Please check your data format.")

    # --- 🌍 Supplier Spend by Region ---
    with col2:
        st.markdown("##### 🌍 Supplier Spend by Region")
        region_map = {
            "China": "Asia", "Japan": "Asia", "India": "Asia", "Vietnam": "Asia",
            "USA": "Americas", "Canada": "Americas", "Mexico": "Americas",
            "Germany": "Europe", "France": "Europe", "UK": "Europe", "Italy": "Europe"
        }
        df["Region"] = df["Country"].map(region_map).fillna("Other")
        region_breakdown = df.groupby("Region")["Spend"].sum()
        fig_donut = go.Figure(data=[go.Pie(
            labels=region_breakdown.index,
            values=region_breakdown.values,
            hole=0.5,
            textinfo='label+percent'
        )])
        fig_donut.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_donut, use_container_width=True)

    # --- 🛡️ Mitigation Plan (AI-Like Logic) ---
    with col3:
        st.markdown("##### 🛡️ Mitigation Plan")
        if resilience_score < 60:
            objective = "Strengthen supply diversification"
            timeline = "6 – 12 months"
            owner = "Supply Chain Director"
            kpis = "Supplier diversity index, lead time, delivery performance"
        elif top_supplier_pct > 50:
            objective = "Reduce single-source dependency"
            timeline = "3 – 6 months"
            owner = "Procurement Lead"
            kpis = "Top supplier share, sourcing options"
        else:
            objective = "Maintain current risk level"
            timeline = "Quarterly reviews"
            owner = "Operations Manager"
            kpis = "On-time delivery, volatility control"

        st.markdown(f"""
        <div style="background-color:#f8f9fa; padding:1.5rem; border-radius:12px; color:#000; border:1px solid #ccc;">
            <p><strong>🎯 Objective:</strong> {objective}</p>
            <p><strong>📅 Timeline:</strong> {timeline}</p>
            <p><strong>👤 Owner:</strong> {owner}</p>
            <p><strong>📊 KPIs:</strong> {kpis}</p>
        </div>
        """, unsafe_allow_html=True)

# --------------- TAB 2: About ---------------
with tab2:
    st.markdown("##  Help & FAQ")

    st.markdown("###  How It Works")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="background:#228be6; padding:1rem; border-radius:10px; color:white;">
            <h4> Upload Your File</h4>
            Upload your CSV or Excel file with basic supplier data.
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background:#20c997; padding:1rem; border-radius:10px; color:white;">
            <h4> Analyze</h4>
            Instantly see resilience scores, risks, and exposure metrics.
        </div>
        """, unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("""
        <div style="background:#f76707; padding:1rem; border-radius:10px; color:white;">
            <h4> Get Recommendations</h4>
            View mitigation suggestions tailored to your results.
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div style="background:#ae3ec9; padding:1rem; border-radius:10px; color:white;">
            <h4> Export or Explore</h4>
            Download your report or try alternate data for comparison.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("###  Learn More")

    with st.expander(" Watch Quick Tutorial Video"):
        st.video("https://www.youtube.com/embed/YOUR_VIDEO_ID")  # Replace with real ID

    with st.expander(" Download or View User Manual"):
        st.markdown("""
        -  [Download the Guide (PDF)](https://yourwebsite.com/resililytics-guide.pdf)
        -  [Open the Online Manual](https://yourwebsite.com/help-doc)
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ❓ Frequently Asked Questions")

    with st.expander("What data do I need to use the app?"):
        st.write("A simple file (CSV or Excel) with supplier names, spend, country, and historical cost values. You can download a template from the homepage.")

    with st.expander("Is my data private?"):
        st.write("Yes. This tool runs entirely in your browser session. Your data is not stored or shared.")

    with st.expander("What happens after I upload my file?"):
        st.write("The system calculates your resilience score, evaluates risk, and gives actionable mitigation suggestions — all instantly.")

    with st.expander("How are resilience metrics calculated?"):
        st.write("Visit the README on GitHub or scroll to the bottom of the app for a full breakdown of formulas and logic.")

    st.markdown("---")
    st.markdown("Still have questions? 👉 [**Contact Us Here**](https://resililytics-app.streamlit.app/#contact)")

  # ---------------------- HELP & FAQ SECTION ----------------------
with tab2:
    st.markdown("## ❓ Help & FAQ")

with st.expander("📂 What file types can I upload?"):
    st.markdown("""
    You can upload `.csv` or `.xlsx` files. Use the [sample template](https://github.com/ResiliLytics/ResiliLytics-App/blob/41880325b28d159778df68a25b3d6ade9fc2aa61/sample%20supplier%20template.xlsx.csv) to structure your data correctly.
    """)

with st.expander("📊 How is the Resilience Score calculated?"):
    st.markdown("""
    The Resilience Score is calculated based on:
    - **Supplier concentration** (how dependent you are on one supplier)
    - **Geographic exposure** (how globally spread your suppliers are)
    - **Cost volatility** (how much historical costs vary)
    """)

with st.expander("🛡️ What are Mitigation Plans?"):
    st.markdown("""
    Mitigation plans are AI-assisted recommendations generated based on your uploaded data. They help you proactively reduce supply chain risk.
    """)

with st.expander("📤 Can I export the results?"):
    st.markdown("""
    Yes. Scroll down to download your full supplier data with risk scores as a `.csv` file.
    """)

with st.expander("📩 What if I have a question or issue?"):
    st.markdown("""
    Reach out through the **Contact** section below. We are here to help!
    """)
# --------------- TAB 3: Contact ---------------
with tab3:
    st.markdown("---")
st.markdown("## 📬 Contact")

col1, col2 = st.columns([1, 2])

with col1:
    st.image("https://resililytics.com/favicon.png", width=80)

with col2:
    st.markdown("""
    **ResiliLytics Support**  
    📧 Email: [support@resililytics.com](mailto:support@resililytics.com)  
    🌐 Website: [resililytics.com](https://resililytics.com)  
    📘 GitHub: [ResiliLytics-App](https://github.com/ResiliLytics/ResiliLytics-App)
    """)

# ---- LEGAL & NON-COMMERCIAL USE DISCLAIMER ----
st.markdown("""
<hr style='margin-top: 3rem; margin-bottom: 1rem;'>

<div style='background-color: #121212; padding: 1.5rem 2rem; border-radius: 12px; border: 1px solid #333;'>

<h3 style='color:#f7c948; font-size: 1.5rem; margin-bottom: 1rem;'>📜 Legal Notice</h3>

<p style='color: #ddd; font-size: 0.95rem; line-height: 1.6;'>
<strong>Disclaimer:</strong> This application is a non-commercial, research-focused prototype developed solely for academic and public-benefit purposes. It is intended to demonstrate a novel approach to SME supply chain resilience using AI and analytics.

The developer is not engaged in any commercial activity.
No services are sold or monetized through this platform.
All uploaded data is used for live computation only and is not stored or retained.
This tool is part of a public contribution portfolio used in support of a research project.
All content is provided “as is” without warranty of any kind.
</p>

<p style='color: #ddd; font-size: 0.95rem; line-height: 1.6;'>
This application <strong>does not offer paid services</strong> and <strong>is not affiliated with any business entity</strong>. The developer is not engaged in commercial activity.
Data uploaded is processed temporarily and not stored.
</p>

</div>
""", unsafe_allow_html=True)
