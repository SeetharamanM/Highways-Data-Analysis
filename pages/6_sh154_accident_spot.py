"""
SH-154 Accident Spot Estimate page.
"""
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="SH-154 Accident Spot Estimate", layout="wide")

st.title("SH-154 Accident Spot Estimate")

# Get the directory of the current script
SCRIPT_DIR = Path(__file__).parent.parent

# Load data
@st.cache_data
def load_data():
    file_path = SCRIPT_DIR / "SH-154 Accident spot AS.xlsx"
    
    # Read reference from first row
    df_header = pd.read_excel(file_path, header=None, nrows=1)
    reference_text = str(df_header.iloc[0, 1]) if not df_header.empty else ""
    
    # Read actual data from row 2 onwards
    df = pd.read_excel(file_path, header=1)
    
    # Clean data - remove empty rows and total row
    df = df[df['SI.No'].notna()]
    df = df[~df['Name ofwork'].astype(str).str.contains('Total', na=False)]
    
    # Convert SI.No to integer
    df['SI.No'] = df['SI.No'].astype(int)
    
    return df, reference_text

df, reference_text = load_data()

# Display reference information
if reference_text and reference_text != 'nan':
    st.info(f"**Reference:** {reference_text}")

# Summary Cards
st.subheader("Estimate Summary")

total_amount = df['Est Amount (in Lakhs)'].sum()
total_works = len(df)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="**Total Estimate Amount**",
        value=f"₹ {total_amount} Lakhs"
    )

with col2:
    st.metric(
        label="**Total Works**",
        value=f"{total_works}"
    )

# Display data table
st.subheader("Accident Spot Improvement Works")
st.dataframe(df, use_container_width=True, hide_index=True)

# Visualizations
st.subheader("Visualizations")

# Amount by work chart
st.bar_chart(df.set_index('Name ofwork')['Est Amount (in Lakhs)'])

# Download button
st.subheader("Download Data")
csv = df.to_csv(index=False)
st.download_button(
    label="Download as CSV",
    data=csv,
    file_name="sh154_accident_spot_estimate.csv",
    mime="text/csv"
)
