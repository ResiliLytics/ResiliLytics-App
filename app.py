import streamlit as st
import pandas as pd

st.set_page_config(page_title="SupplySight", layout="wide")

st.title("SupplySight (Beta)")
st.caption("AI for SME Resilience • 2025")

st.markdown("Upload a CSV or XLSX. The file must contain ONE ROW with these columns:")
st.code("Supplier_Count, Geo_Spread, Lead_Time, Cost_Volatility, Inventory_Days")

uploaded_file = st.file_uploader("Choose file", type=["csv", "xlsx"])

def calculate_resilience_score(supplier_count, geo_spread, lead_time, cost_volatility, inventory_days):
    score = (
        (supplier_count / 10) * 0.2 +
        (geo_spread / 10) * 0.2 +
        ((120 - lead_time) / 120) * 0.2 +
        ((10 - cost_volatility) / 10) * 0.2 +
        (inventory_days / 180) * 0.2
    ) * 100
    return round(score, 2)

def risk_level(score):
    if score >= 80:
        return "🟢 Low Risk"
    elif score >= 50:
        return "🟡 Medium Risk"
    else:
        return "🔴 High Risk"

if uploaded_file is None:
    st.info("Please upload a file to view dynamic metrics.")
    st.stop()

# --- Read file safely ---
try:
    if uploaded_file.name.lower().endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)  # requires openpyxl in requirements.txt
except Exception as e:
    st.error(f"Could not read file: {e}")
    st.stop()

if df.empty:
    st.error("Your uploaded file is empty.")
    st.stop()

required_cols = ["Supplier_Count", "Geo_Spread", "Lead_Time", "Cost_Volatility", "Inventory_Days"]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"Missing required columns: {missing}")
    st.stop()

# Use first row
row = df.iloc[0]

try:
    supplier_count = float(row["Supplier_Count"])
    geo_spread = float(row["Geo_Spread"])
    lead_time = float(row["Lead_Time"])
    cost_volatility = float(row["Cost_Volatility"])
    inventory_days = float(row["Inventory_Days"])
except Exception as e:
    st.error(f"Invalid values in the first row: {e}")
    st.stop()

score = calculate_resilience_score(supplier_count, geo_spread, lead_time, cost_volatility, inventory_days)

# --- Display ---
st.subheader("📈 Resilience Score")
st.metric(label="Your SME Resilience Score", value=f"{score} / 100", delta=score - 50)
st.markdown(f"**Risk Level**: {risk_level(score)}")

st.subheader("💡 Recommendations")
if score < 50:
    st.warning("High supply chain risk detected. Consider diversifying suppliers, increasing inventory coverage, or reducing lead times.")
elif score < 80:
    st.info("Moderate risk. You may benefit from regional diversification or improved cost tracking.")
else:
    st.success("Your supply chain appears resilient! Monitor your metrics to maintain this level.")

# --- Downloadable report (matches the chat-history intent, but safely) ---
st.subheader("📄 Download Your Mitigation Plan")
report = f"""SupplySight Resilience Report

Resilience Score: {score}/100
Risk Level: {risk_level(score)}

Inputs:
- Supplier Count: {supplier_count}
- Geographic Spread: {geo_spread}
- Lead Time: {lead_time} days
- Cost Volatility: {cost_volatility}/10
- Inventory Days: {inventory_days}

Mitigation Suggestions:
"""

if score < 50:
    report += "- Diversify supplier base\n- Add regional sourcing options\n- Build inventory buffer\n- Track cost drivers\n"
else:
    report += "- Maintain current strategies\n- Monitor global trends\n- Reassess quarterly\n"

st.download_button("📥 Download Plan", report, file_name="SupplySight_Report.txt")
