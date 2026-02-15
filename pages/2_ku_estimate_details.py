"""
Data analysis page for KU_Estimate Details.csv — filter by Items, show Total Amt and % in tiles.
First row = title, second row = header.
"""
import streamlit as st
import pandas as pd
from pathlib import Path

# Page title = file name (no extension, capitalised)
st.set_page_config(page_title="KU Estimate Details", layout="wide")

# Default data path (project root). Try both casings for local vs Streamlit Cloud
_root = Path(__file__).parent.parent
DEFAULT_DATA_PATHS = [
    _root / "KU_Estimate Details.csv",
    _root / "ku_estimate details.csv",
]
DEFAULT_DATA_PATH = next((p for p in DEFAULT_DATA_PATHS if p.exists()), DEFAULT_DATA_PATHS[0])

# File upload or use default
st.sidebar.header("Data source")
use_upload = st.sidebar.checkbox("Upload a file", value=False)

if use_upload:
    uploaded = st.sidebar.file_uploader("Choose CSV or Excel", type=["csv", "xlsx", "xls"])
    if uploaded is None:
        st.info("Upload a CSV or Excel file to start.")
        st.stop()
    if uploaded.name.endswith(".csv"):
        raw = pd.read_csv(uploaded, header=None)
    else:
        raw = pd.read_excel(uploaded, header=None)
else:
    if not DEFAULT_DATA_PATH.exists():
        st.error(
            "Default file not found. Looked for 'KU_Estimate Details.csv'. "
            "Upload a file using the sidebar or add the CSV to your repo."
        )
        st.stop()
    raw = pd.read_csv(DEFAULT_DATA_PATH, header=None)

# First row = title, second row = header
title_row = raw.iloc[0].iloc[0] if len(raw) > 0 else ""
df = raw.iloc[1:].copy()
df.columns = df.iloc[0]
df = df.iloc[1:].reset_index(drop=True)

# Normalize column names
df.columns = df.columns.astype(str).str.strip()

# Parse Total Amt as numeric
total_amt_col = "Total Amt"
if total_amt_col in df.columns:
    df[total_amt_col] = pd.to_numeric(
        df[total_amt_col].astype(str).str.replace(",", ""), errors="coerce"
    )

# Display title at top (big)
display_title = str(title_row).strip() if title_row and str(title_row).strip() else "KU Estimate Details"
st.markdown(
    f'<p style="font-size: 2.25rem; font-weight: 700; margin: 0 0 1.5rem 0; line-height: 1.3;">{display_title}</p>',
    unsafe_allow_html=True,
)

# Filter by Items
items_col = "Items"
if items_col not in df.columns:
    items_col = next((c for c in df.columns if "item" in c.lower()), None)

if items_col and items_col in df.columns:
    st.sidebar.header("Filters")
    all_items = sorted(df[items_col].dropna().astype(str).unique().tolist())
    selected_items = st.sidebar.multiselect(
        f"**{items_col}**",
        options=all_items,
        default=all_items,
    )
    if selected_items:
        filtered_df = df[df[items_col].astype(str).isin(selected_items)].copy()
    else:
        filtered_df = df.copy()
    include_lumpsum = st.sidebar.checkbox("Include Lumpsum in total", value=True)
else:
    filtered_df = df.copy()
    include_lumpsum = True

# Data for total calculation (exclude Lumpsum when checkbox unchecked)
if items_col and items_col in filtered_df.columns and not include_lumpsum:
    items_stripped = df[items_col].astype(str).str.strip()
    filt_items_stripped = filtered_df[items_col].astype(str).str.strip()
    df_for_total = df[items_stripped != "Lumpsum"]
    filtered_for_total = filtered_df[filt_items_stripped != "Lumpsum"]
else:
    df_for_total = df
    filtered_for_total = filtered_df

# Tiles: Total Amt and % of total (for all filtered items only)
if total_amt_col in filtered_df.columns:
    total_filtered = filtered_for_total[total_amt_col].sum()
    total_all = df_for_total[total_amt_col].sum()
    pct_of_total = (total_filtered / total_all * 100) if total_all > 0 else 0

    st.markdown("""
    <style>
    .tile-amt { background: linear-gradient(135deg, #1e88e5 0%, #42a5f5 100%); color: white; padding: 1rem 1.25rem; border-radius: 10px; margin-bottom: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .tile-pct { background: linear-gradient(135deg, #43a047 0%, #66bb6a 100%); color: white; padding: 1rem 1.25rem; border-radius: 10px; margin-bottom: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .tile-label { font-size: 0.85rem; opacity: 0.95; }
    .tile-value { font-size: 1.5rem; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

    st.subheader("Filtered totals")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f'<div class="tile-amt"><div class="tile-label">Total Amt (filtered)</div><div class="tile-value">{total_filtered:,.0f}</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="tile-pct"><div class="tile-label">% of Total</div><div class="tile-value">{pct_of_total:.1f}%</div></div>',
            unsafe_allow_html=True,
        )

st.subheader("Filtered data")
st.dataframe(filtered_df, use_container_width=True)
