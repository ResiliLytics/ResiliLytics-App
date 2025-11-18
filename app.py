import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64
from io import BytesIO

st.set_page_config(page_title="SupplySight", layout="wide")

# ---- HEADER ----
st.markdown("""
    <div style='text-align: center; padding: 1rem; border-radius: 10px; background-color: #F5F7FA;'>
        <h1 style='color: #003366;'>SupplySight Dashboard</h1>
        <h4 style='color: #444;'>AI-powered SME resilience scoring + mitigation insights</h4>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---- SIDEBAR ----
st.sidebar.header("Upload Your Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

# Sample file download
def download_sample():
    sample_data = pd.DataFrame({
        'Supplier': ['ABC Corp', 'XYZ Inc', 'Delta LLC'],
        'Cost': [10000, 12000, 9000],
        'Lead Time': [12, 18, 10],
        'Geographic Risk': [3, 7, 2],
        'Dependency Score': [9, 6, 4]
    })
    buffer = BytesIO()
    sample_data.to_excel(buffer, index=False)
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="sample_template.xlsx">📥 Download Sample Template</a>'
    return href

st.sidebar.markdown(download_sample(), unsafe_allow_html=True)

# ---- MAIN LOGIC ----
if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ File successfully uploaded.")
        st.write("### Preview of Uploaded Data", df.head())

        # ---- Resilience Score Calculation ----
        df['Resilience Score'] = 100 - (
            (df['Cost'] / df['Cost'].max()) * 0.25 +
            (df['Lead Time'] / df['Lead Time'].max()) * 0.25 +
            (df['Geographic Risk'] / 10) * 0.25 +
            (df['Dependency Score'] / 10) * 0.25
        ) * 100

        # ---- Visualization ----
        fig = go.Figure()
        color_map = []

        for score in df['Resilience Score']:
            if score >= 75:
                color_map.append("green")
            elif score >= 50:
                color_map.append("orange")
            else:
                color_map.append("red")

        fig.add_trace(go.Bar(
            x=df['Supplier'],
            y=df['Resilience Score'],
            marker_color=color_map
        ))

        fig.update_layout(
            title="Supply Chain Resilience Score by Supplier",
            xaxis_title="Supplier",
            yaxis_title="Resilience Score (0–100)",
            height=400
        )

        st.plotly_chart(fig)

        # ---- Mitigation Suggestions ----
        st.markdown("### 🔧 AI-Powered Mitigation Suggestions")
        for index, row in df.iterrows():
            score = row['Resilience Score']
            if score >= 75:
                st.success(f"Supplier **{row['Supplier']}**: Low risk. Maintain current strategy.")
            elif score >= 50:
                st.warning(f"Supplier **{row['Supplier']}**: Moderate risk. Consider alternative suppliers and buffer inventory.")
            else:
                st.error(f"Supplier **{row['Supplier']}**: High risk. Urgently diversify supply chain and monitor closely.")

    except Exception as e:
        st.error("❌ Error processing file. Please check the format and column names.")
        st.exception(e)
else:
    st.info("👈 Upload a file to get started.")
