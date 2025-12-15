import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="ResiliLytics")

# Styling + banner
st.markdown("""
<style>
/* Scrolling banner styling */
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

# ---- HEADER ----
st.markdown("""
<div style='display: flex; align-items: center; background-color: #0e1117; padding: 1rem; border-radius: 10px; margin-bottom: 3rem;'>
    <img src='https://github.com/ResiliLytics/ResiliLytics-assets/blob/d3dc6cd2011816b6fe359d1867b286f4e7b07fa4/Logo%204.png?raw=true' alt='ResiliLytics Logo' width='120' style='margin-right: 20px;'/>
    <div>
        <h1 style='color: #fdf6e3; font-size: 3.5rem; margin: 0;'>ResiliLytics Dashboard</h1>
        <h3 style='color: #e0e0e0; font-weight: 400; margin-top: -0.95rem;'>Sourcing Intelligence for Resilient Supply Chains</h3>
    </div>
</div>
""", unsafe_allow_html=True)

# ---- TABS ----
tab1, tab2, tab3 = st.tabs([" Dashboard", " Help & FAQ", " Contact"])

# --------------- TAB 1: Dashboard ---------------
with tab1:
    # ---- HEADER BLOCK ----
    st.markdown("""
    <div style='display: flex; align-items: center; background-color: #0e1117; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
        <img src='https://github.com/ResiliLytics/ResiliLytics-assets/blob/d3dc6cd2011816b6fe359d1867b286f4e7b07fa4/Logo%204.png?raw=true' alt='ResiliLytics Logo' width='110' style='margin-right: 20px;'/>
        <div>
            <h1 style='color: #fdf6e3; font-size: 2.8rem; margin: 0;'>ResiliLytics Dashboard</h1>
            <h4 style='color: #e0e0e0; font-weight: 400;'>Sourcing Intelligence for Resilient Supply Chains</h4>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---- DESCRIPTION ----
    st.markdown("## About ResiliLytics")
    st.markdown("ResiliLytics is a free next-gen platform to help SMEs monitor & improve supply chain resilience with intelligent risk-to-action insights.")

    with st.expander("Read full description"):
        st.markdown("""
        **ResiliLytics**:
        - Analyzes supplier risk exposure
        - Recommends mitigation strategies
        - Translates supply chain complexity into clear plans

        **What Makes It Unique?**
        - Supply chain analytics
        - Risk classification
        - AI-assisted insights
        - Decision-ready recommendations
        """)

    # ---- DATA UPLOAD ----
    st.markdown("### Upload Your Data")
    st.markdown("Upload your **.csv** or **.xlsx** file and instantly generate your risk profile.")

    st.markdown("""
        - [📥 Download Sample Template (Excel)](https://github.com/ResiliLytics/ResiliLytics-App/raw/main/sample%20supplier%20template.xlsx.csv)
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
    "Choose a .csv or .xlsx file",
    type=['csv', 'xlsx'],
    key="main_data_upload"
)

    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)

        # --- BASIC COMPUTATIONS ---
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
        risk_color = "#e74c3c" if supply_risk == "High" else "#f6c542" if supply_risk == "Moderate" else "#43a047"

        # --- ALERT CHART LOGIC (Bar) ---
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df['Month'] = df['Date'].dt.strftime('%b')
            monthly_alerts = df['Month'].value_counts().reindex(["Jan", "Feb", "Mar", "Apr", "May", "Jun"], fill_value=0)
        else:
            df['Alert'] = (df['Volatility'] > 0.5) | (df.groupby('Supplier')['Spend'].transform('sum') / total_spend > 0.5)
            df['Month'] = np.random.choice(["Jan", "Feb", "Mar", "Apr", "May", "Jun"], size=len(df))
            monthly_alerts = df[df['Alert'] == True]['Month'].value_counts().reindex(["Jan", "Feb", "Mar", "Apr", "May", "Jun"], fill_value=0)

        # --- REGION LOGIC ---
        region_map = {
            "China": "Asia", "India": "Asia", "Vietnam": "Asia", "Japan": "Asia",
            "USA": "Americas", "Brazil": "Americas", "Mexico": "Americas",
            "Germany": "Europe", "France": "Europe", "UK": "Europe", "Italy": "Europe"
        }
        df['Region'] = df['Country'].map(region_map).fillna("Other")
        region_counts = df.groupby('Region')['Spend'].sum()
        region_colors = {'Asia': '#43a047', 'Europe': '#f6c542', 'Americas': '#228be6', 'Other': '#999999'}

        # --- VISUAL BLOCKS ---
        col1, col2, col3 = st.columns([1.1, 1, 1])
        with col1:
            st.markdown("#### Resilience Score")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=resilience_score,
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#00cc44"},
                    "steps": [
                        {"range": [0, 50], "color": "#e74c3c"},
                        {"range": [50, 75], "color": "#f6c542"},
                        {"range": [75, 100], "color": "#43a047"},
                    ],
                }
            ))
            fig.update_layout(height=250, paper_bgcolor="#0e1117", font=dict(color="white"))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### Key Metrics")
            c1, c2 = st.columns(2)
            c1.markdown(f"🧩 **Supplier Concentration:** {top_supplier_pct:.1f}%")
            c2.markdown(f"🌍 **Countries:** {num_countries}")
            c1.markdown(f"📉 **Cost Volatility:** {volatility_level}")
            c2.markdown(f"⚠️ **Supply Risk:** `{supply_risk}`")

        with col3:
            st.markdown("#### Recommendations")
            st.markdown("- ✅ Evaluate alternate suppliers in East Asia")
            st.markdown("- 📦 Increase buffer inventory")
            st.download_button("📄 Download Project Brief", "Sample project text here.", file_name="supplier_plan.txt")

        # --- Insights ---
        col4, col5 = st.columns(2)
        with col4:
            st.markdown("#### 📊 Risk Insights (Monthly Alerts)")
            st.bar_chart(monthly_alerts)

        with col5:
            st.markdown("#### 🧭 Supplier Diversification")
            st.plotly_chart(px.pie(
                names=region_counts.index,
                values=region_counts.values,
                color=region_counts.index,
                color_discrete_map=region_colors,
                hole=0.4
            ).update_layout(showlegend=True), use_container_width=True)

        # --- Mitigation Plan ---
        st.markdown("### 🛠️ Mitigation Plan")
        st.markdown("""
        <div style='background:#f5f5dc;padding:1rem;border-radius:10px;'>
        <b>Objective:</b> Reduce single-source reliance<br>
        <b>Timeline:</b> 3–8 months<br>
        <b>Owner:</b> Supply Chain Manager<br>
        <b>KPIs:</b> Supplier mix, lead time
        </div>
        """, unsafe_allow_html=True)

        # --- Export Data Button ---
        st.download_button("📤 Download Full Report", df.to_csv(index=False), file_name="resililytics_output.csv")

# --------------- TAB 2: About ---------------
with tab2:
    st.markdown("## 📖 Help & FAQ")

    st.markdown("### 🛠️ How It Works")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="background:#228be6; padding:1rem; border-radius:10px; color:white;">
            <h4>📤 Upload Your File</h4>
            Upload your CSV or Excel file with basic supplier data.
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background:#20c997; padding:1rem; border-radius:10px; color:white;">
            <h4>📈 Analyze</h4>
            Instantly see resilience scores, risks, and exposure metrics.
        </div>
        """, unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("""
        <div style="background:#f76707; padding:1rem; border-radius:10px; color:white;">
            <h4>💡 Get Recommendations</h4>
            View mitigation suggestions tailored to your results.
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div style="background:#ae3ec9; padding:1rem; border-radius:10px; color:white;">
            <h4>📄 Export or Explore</h4>
            Download your report or try alternate data for comparison.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📺 Learn More")

    with st.expander("▶️ Watch Quick Tutorial Video"):
        st.video("https://www.youtube.com/embed/YOUR_VIDEO_ID")  # Replace with real ID

    with st.expander("📄 Download or View User Manual"):
        st.markdown("""
        - 📥 [Download the Guide (PDF)](https://yourwebsite.com/resililytics-guide.pdf)
        - 📘 [Open the Online Manual](https://yourwebsite.com/help-doc)
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

# --------------- TAB 3: Contact ---------------
with tab3:
    st.markdown("## Contact Us")
    st.markdown("Have feedback or want to collaborate? Fill out the form below.")
    contact_form = """
    <form action="https://formspree.io/f/xrbnaeqd" method="POST">
        <label>Your email:<br><input type="email" name="email" style="width: 100%; padding: 8px;" required></label><br><br>
        <label>Your message:<br><textarea name="message" rows="5" style="width: 100%; padding: 8px;" required></textarea></label><br>
        <input type="text" name="_gotcha" style="display:none"> <!-- honeypot -->
        <button type="submit" style="background-color:#228be6; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer;">Send</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html=True)

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
