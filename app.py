import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="ResiliLytics", layout="wide")

# --- LOGO ---
logo_url = "https://raw.githubusercontent.com/ResiliLytics/ResiliLytics-assets/main/Logo.png"
st.image(logo_url, width=80)

# --- TABS ---
tab1, tab2 = st.tabs(["🏠 Home", "📊 Dashboard"])

# -------------------------
# HOME TAB
# -------------------------
with tab1:
    st.markdown("## ResiliLytics Dashboard")
    st.markdown("### Sourcing Intelligence for Resilient Supply Chains")

    st.markdown("""
    ResiliLytics is a next-generation platform designed to help **Small and Medium Enterprises (SMEs)** monitor and improve supply chain resilience using intelligent risk-to-action insights.

    Powered by data and guided by insight, ResiliLytics:
    - Analyzes supplier risk exposure.
    - Recommends mitigation strategies.
    - Translates supply chain complexity into clear, actionable plans.
    
    ---
    
    ### 🧠 What Makes It Unique?
    ResiliLytics brings together:
    - 📦 **Supply chain analytics**
    - ⚠️ **Risk classification**
    - 🤖 **AI-assisted insights**
    - 🎯 **Decision-ready recommendations**

    All in one simple, accessible tool — created for real-world SME challenges.

    ---

    ### 🧪 Original Contribution
    ResiliLytics introduces a novel approach to:
    - Supply chain visualization.
    - Dynamic diversification metrics.
    - End-to-end data-to-action transformation — not previously available in one open-access interface.
    
    The platform is developed in support of ongoing academic and professional research on improving SME supply-chain resilience through intelligent systems.

    ---
    """, unsafe_allow_html=True)

    # Dashboard preview
    dashboard_url = "https://raw.githubusercontent.com/ResiliLytics/ResiliLytics-assets/main/ResiliLytics-Dashboard-Snapshot.png"
    st.image(dashboard_url, caption="Preview: ResiliLytics Dashboard", use_column_width=True)

# -------------------------
# DASHBOARD TAB
# -------------------------
with tab2:
    st.markdown("## Upload Your Data")
    st.markdown("Upload your `.csv` or `.xlsx` file to generate custom insights.")

    uploaded_file = st.file_uploader("Choose file", type=["csv", "xlsx"])

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

        # --- Risk Logic ---
        resilience_score = max(0, 100 - top_supplier_pct - (avg_volatility * 20))
        supply_risk = "High" if top_supplier_pct > 60 or avg_volatility > 0.5 else "Moderate" if avg_volatility > 0.3 else "Low"
        volatility_level = "High" if avg_volatility > 0.5 else "Moderate" if avg_volatility > 0.3 else "Low"
        risk_color = "#e74c3c" if supply_risk == "High" else "#f6c542" if supply_risk == "Moderate" else "#43a047"

        # --- Layout ---
        col1, col2, col3 = st.columns([1, 1, 1.2])

        # --- Gauge ---
        with col1:
            st.markdown("### Resilience Score")
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
            fig.update_layout(height=250, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)

        # --- Metrics ---
        with col2:
            st.markdown("### Key Metrics")
            c1, c2 = st.columns(2)
            c1.metric("Supplier Concentration", f"{top_supplier_pct:.1f}%")
            c2.metric("Geographic Exposure", f"{num_countries} Countries")
            c1.metric("Cost Volatility", volatility_level)
            c2.metric("Supply Risk", supply_risk)

        # --- AI Recommendations ---
        with col3:
            st.markdown("### Mitigation Plan")
            st.markdown(f"""
            <div style='background:#43a047; color:#fff; border-radius:10px; padding:1rem; margin-bottom:8px;'>✅ Evaluate alternate suppliers in East Asia<br><span style='font-size:0.8em;'>Timeline: 3–6 months</span></div>
            <div style='background:#f6c542; color:#111; border-radius:10px; padding:1rem; margin-bottom:8px;'>📦 Increase buffer inventory for key items<br><span style='font-size:0.8em;'>Timeline: 6 months</span></div>
            <div style='background:#228be6; color:#fff; border-radius:10px; padding:1rem;'>📄 Supplier Diversification Plan<br><span style='font-size:0.8em;'>Region: Europe</span></div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.dataframe(df)

        st.markdown("<small>Replace demo values with calculations after approval.</small>", unsafe_allow_html=True)
    else:
        st.info("📂 Upload your dataset above to begin.")

tab1, tab2, tab3 = st.tabs(["🏠 Home", "📊 Dashboard", "📬 Contact"])

# ---- CONTACT TAB ----
with tab3:
    st.markdown("## 📫 Contact Us")
    st.markdown("Fill out the form below. We'll get back to you as soon as possible.")

    contact_form = """
    https://formspree.io/f/xrbnaeqd
        <label for="name">Your Name</label><br>
        <input type="text" name="name" required style="width:100%;"><br><br>
        <label for="email">Your Email</label><br>
        <input type="email" name="_replyto" required style="width:100%;"><br><br>
        <label for="message">Your Message</label><br>
        <textarea name="message" rows="5" style="width:100%;" required></textarea><br><br>
        <button type="submit">Send</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html=True)
