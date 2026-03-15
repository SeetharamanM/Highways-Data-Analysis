"""
Data analysis page for SH Junction Details.xlsx.
First row is the header. Filter by Main Road, Branch Road, Type of Junction.
Show sum of No of Junctions (filtered and overall) in tiles.
"""
import streamlit as st
import pandas as pd
from pathlib import Path

# Page title
st.set_page_config(page_title="SH Junction Details", layout="wide")

st.title("SH Junction Details")

# Default data path (project root). Try common casings for local vs Linux
_root = Path(__file__).parent.parent
DEFAULT_DATA_PATHS = [
    _root / "SH Junction Details.xlsx",
    _root / "sh junction details.xlsx",
]
DEFAULT_DATA_PATH = next((p for p in DEFAULT_DATA_PATHS if p.exists()), DEFAULT_DATA_PATHS[0])

# File upload or use default
st.sidebar.header("Data source")
use_upload = st.sidebar.checkbox("Upload a file", value=False)

if use_upload:
    uploaded = st.sidebar.file_uploader("Choose Excel file", type=["xlsx", "xls"])
    if uploaded is None:
        st.info("Upload an Excel file to start.")
        st.stop()
    df = pd.read_excel(uploaded)
else:
    if not DEFAULT_DATA_PATH.exists():
        st.error(
            "Default file not found. Looked for 'SH Junction Details.xlsx' in the app folder. "
            "Upload a file using the sidebar or add the Excel file to your repo."
        )
        st.stop()
    df = pd.read_excel(DEFAULT_DATA_PATH)

# Normalize column names
df.columns = df.columns.astype(str).str.strip()

# Expected columns
main_road_col = "Main Road"
branch_road_col = "Branch Road"
junction_type_col = "Type of Junction"

# Find the junction count column robustly (in case of spacing/case differences)
junctions_col = None
for c in df.columns:
    if "no" in c.lower() and "junction" in c.lower():
        junctions_col = c
        break

# Coerce numeric for No of Junctions
if junctions_col:
    df[junctions_col] = pd.to_numeric(
        df[junctions_col].astype(str).str.replace(",", ""), errors="coerce"
    )

st.sidebar.header("Filters")

filtered_df = df.copy()

def apply_multiselect(col_name: str) -> None:
    global filtered_df
    if col_name in filtered_df.columns:
        values = sorted(filtered_df[col_name].dropna().astype(str).unique().tolist())
        selected = st.sidebar.multiselect(
            f"**{col_name}**",
            options=values,
            default=values,
        )
        if selected:
            filtered_df = filtered_df[filtered_df[col_name].astype(str).isin(selected)]

# Apply filters
for col in (main_road_col, branch_road_col, junction_type_col):
    apply_multiselect(col)

# Tiles: totals for No of Junctions (filtered and overall)
st.markdown(
    """
    <style>
    .tile-main { background: linear-gradient(135deg, #1e88e5 0%, #42a5f5 100%); color: white; padding: 1rem 1.25rem; border-radius: 10px; margin-bottom: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .tile-overall { background: linear-gradient(135deg, #43a047 0%, #66bb6a 100%); color: white; padding: 1rem 1.25rem; border-radius: 10px; margin-bottom: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .tile-label { font-size: 0.85rem; opacity: 0.95; }
    .tile-value { font-size: 1.5rem; font-weight: 700; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.subheader("Totals")

c1, c2 = st.columns(2)

total_filtered = filtered_df[junctions_col].sum() if junctions_col in filtered_df.columns else None
total_all = df[junctions_col].sum() if junctions_col in df.columns else None

with c1:
    if total_filtered is not None:
        st.markdown(
            f'<div class="tile-main"><div class="tile-label">No of Junctions (filtered)</div>'
            f'<div class="tile-value">{total_filtered:,.0f}</div></div>',
            unsafe_allow_html=True,
        )
with c2:
    if total_all is not None:
        st.markdown(
            f'<div class="tile-overall"><div class="tile-label">No of Junctions (all items)</div>'
            f'<div class="tile-value">{total_all:,.0f}</div></div>',
            unsafe_allow_html=True,
        )

st.subheader("Filtered data")
st.dataframe(filtered_df, use_container_width=True)

