import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.markdown("""
<style>
.marquee-container {
  width: 100%;
  overflow: hidden;
  position: fixed;
  top: 0;
  z-index: 9999;
  background-color: #013440;  /* Deep teal background */
  color: #f4f4f4;              /* Soft white text */
  font-size: 0.88rem;
  font-family: 'Segoe UI', sans-serif;
  padding: 0.4rem 1rem;
  border-bottom: 2px solid #0ff;
}

.marquee-text {
  display: inline-block;
  padding-left: 100%;
  animation: scroll-left 20s linear infinite;
  white-space: nowrap;
}

.marquee-container:hover .marquee-text {
  animation-play-state: paused;
}

@keyframes scroll-left {
  0% {
    transform: translateX(0%);
  }
  100% {
    transform: translateX(-100%);
  }
}
</style>

<div class="marquee-container">
  <div class="marquee-text">
    🔎 Note: This tool is part of a non-commercial academic research project. See disclaimer below.
  </div>
</div>
""", unsafe_allow_html=True)

# ---- SIDEBAR ----
st.sidebar.title("📊 ResiliLytics")
page = st.sidebar.radio("Navigate", ["About", "Dashboard", "Contact"])

# ---- HEADER ----
st.markdown("""
    <div style='text-align: left; padding: 0.5rem 0 0rem 0;'>
        <img src='https://raw.githubusercontent.com/ResiliLytics/ResiliLytics-assets/main/Logo%203.png' alt='ResiliLytics Logo 3' width='360'>
        <img src='https://raw.githubusercontent.com/ResiliLytics/ResiliLytics-assets/main/Logo%204.png' alt='ResiliLytics Logo 4' width='160'> 
        <h1 style='color: #ffffff; margin-bottom: .2rem; margin-top: -0.2rem;'>ResiliLytics Dashboard</h1>
        <h3 style='color: #bbbbbb; font-weight:400; margin-top: -0.5rem;'>Sourcing Intelligence for Resilient Supply Chains</h3>
    </div>
""", unsafe_allow_html=True)

# ---- PAGE: DASHBOARD ----
if page == "Dashboard":
    st.markdown("### Upload Your Data")
    uploaded_file = st.file_uploader("Choose a .csv or .xlsx file", type=['csv', 'xlsx'])
    st.markdown("""
    <div style='color:#ccc; font-size:0.95rem;'>
        Upload your .csv or .xlsx file with columns: Supplier, Country, Spend, Cost_Per_Unit, Historical_Costs<br>
        <a href='/mnt/data/945104ef-ae7f-4f41-bb2e-7e2b1d287db3.xlsx' download style='color:#91caff;'>Download Sample Template</a>
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
        st.markdown("### 📽️ Need Help?")
        st.markdown("""If you're unsure how to use the dashboard, watch our quick <a href='https://www.youtube.com/watch?v=YOUR_VIDEO_ID' target='_blank' style='color:#91caff;'>3-minute tutorial</a>.""", unsafe_allow_html=True)
        st.markdown("💬 [Frequently Asked Questions](https://yourfaqpage.com) — get quick answers to common issues.")
        st.image("https://github.com/ResiliLytics/ResiliLytics-assets/blob/b553fe3aa11e13bd72d77789970bc3bb3cc08147/Final%20Dashboard%20Sample.png?raw=true")

# ---- PAGE: ABOUT ----
elif page == "About":
    st.markdown("### About ResiliLytics")
    st.markdown("""
    ResiliLytics is a research-based prototype designed to help assess the resilience of supply chains using uploaded data. This academic tool allows users to upload supplier data and visualize concentration risk, geographic exposure, cost volatility, and get recommendations.
    """)
    st.image("https://github.com/ResiliLytics/ResiliLytics-assets/blob/b553fe3aa11e13bd72d77789970bc3bb3cc08147/Final%20Dashboard%20Sample.png?raw=true")

# ---- PAGE: CONTACT ----
elif page == "Contact":
    st.markdown("### 📬 Contact Us")
    st.markdown("Have feedback, suggestions, or want to collaborate? Fill out the form below.")
    
    contact_form = """
    <form action="https://formspree.io/f/xrbnaeqd" method="POST">
        <label>Your email:<br><input type="email" name="email" style="width: 100%; padding: 8px;" required></label><br><br>
        <label>Your message:<br><textarea name="message" rows="5" style="width: 100%; padding: 8px;" required></textarea></label><br>
        <input type="text" name="_gotcha" style="display:none"> <!-- honeypot -->
        <button type="submit" style="background-color:#228be6; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer;">Send</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html=True)

# ---- LEGAL DISCLAIMER ----
st.markdown("### 📜 Legal Notice")
st.markdown("---")
st.markdown("""
<div style='font-size: 0.85rem; color: #aaa; padding: 1rem 0;'>
    <strong>Disclaimer:</strong> This is a non-commercial, research-focused prototype developed solely for academic and public benefit purposes. It is part of a demonstration for showcasing technical contributions to the field of supply chain resilience and AI-driven risk analytics.
    <br><br>
    This application <strong>does not offer paid services</strong> and <strong>is not affiliated with any business entity</strong>. The developer is an F‑1 visa student and is not engaged in commercial activity. Data uploaded is processed temporarily and not stored.
    <br><br>
     No income is derived from this tool.
</div>
""", unsafe_allow_html=True)

