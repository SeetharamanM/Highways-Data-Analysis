"""
Data analysis page for CRIDP 2026-27 Proposal.xlsx.
First row is the header. Filter by Category, Road, Work Type.
Show Length and Cost with totals in tiles.
"""
import streamlit as st
import pandas as pd
from pathlib import Path

# Page title
st.set_page_config(page_title="CRIDP 2026-27 Proposal", layout="wide")

# Default data path (project root). Try common casings for local vs Linux
_root = Path(__file__).parent.parent
DEFAULT_DATA_PATHS = [
    _root / "CRIDP 2026-27 Proposal.xlsx",
    _root / "cridp 2026-27 proposal.xlsx",
]
DEFAULT_DATA_PATH = next((p for p in DEFAULT_DATA_PATHS if p.exists()), DEFAULT_DATA_PATHS[0])

st.title("CRIDP 2026-27 Proposal")

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
            "Default file not found. Looked for 'CRIDP 2026-27 Proposal.xlsx' in the app folder. "
            "Upload a file using the sidebar or add the Excel file to your repo."
        )
        st.stop()
    df = pd.read_excel(DEFAULT_DATA_PATH)

# Normalize column names
df.columns = df.columns.astype(str).str.strip()

# Expected columns
category_col = "Category"
road_col = "Road"
work_type_col = "Work Type"
# Use the Excel column names after stripping spaces
length_col = "Length in KM"
cost_col = "Cost in Lakhs"

# Coerce numeric for Length and Cost
for col in (length_col, cost_col):
    if col in df.columns:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(",", ""), errors="coerce"
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
for col in (category_col, road_col, work_type_col):
    apply_multiselect(col)

# Tiles: totals for Length and Cost (filtered)
st.markdown(
    """
    <style>
    .tile-len { background: linear-gradient(135deg, #1e88e5 0%, #42a5f5 100%); color: white; padding: 1rem 1.25rem; border-radius: 10px; margin-bottom: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .tile-cost { background: linear-gradient(135deg, #43a047 0%, #66bb6a 100%); color: white; padding: 1rem 1.25rem; border-radius: 10px; margin-bottom: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .tile-label { font-size: 0.85rem; opacity: 0.95; }
    .tile-value { font-size: 1.5rem; font-weight: 700; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.subheader("Filtered totals")

c1, c2 = st.columns(2)

total_length = filtered_df[length_col].sum() if length_col in filtered_df.columns else None
total_cost = filtered_df[cost_col].sum() if cost_col in filtered_df.columns else None

with c1:
    if total_length is not None:
        st.markdown(
            f'<div class="tile-len"><div class="tile-label">Total Length in KM (filtered)</div>'
            f'<div class="tile-value">{total_length:,.2f}</div></div>',
            unsafe_allow_html=True,
        )
with c2:
    if total_cost is not None:
        st.markdown(
            f'<div class="tile-cost"><div class="tile-label">Total Cost in Lakhs (filtered)</div>'
            f'<div class="tile-value">{total_cost:,.2f}</div></div>',
            unsafe_allow_html=True,
        )

# Tiles grouped by Category, Work Type
if all(col in filtered_df.columns for col in (category_col, work_type_col, length_col, cost_col)):
    st.subheader("Totals by Category, Work Type (filtered)")
    grouped = (
        filtered_df
        .groupby([category_col, work_type_col], as_index=False)[[length_col, cost_col]]
        .sum()
        .sort_values(cost_col, ascending=False)
    )

    n_per_row = 3
    for start in range(0, len(grouped), n_per_row):
        chunk = grouped.iloc[start : start + n_per_row]
        cols = st.columns(len(chunk))
        for j, (_, row) in enumerate(chunk.iterrows()):
            with cols[j]:
                header = f"{row[category_col]} / {row[work_type_col]}"
                st.markdown(
                    f'<div class="tile-len"><div class="tile-label">{header} — Length in KM</div>'
                    f'<div class="tile-value">{row[length_col]:,.2f}</div></div>'
                    f'<div class="tile-cost"><div class="tile-label">{header} — Cost in Lakhs</div>'
                    f'<div class="tile-value">{row[cost_col]:,.2f}</div></div>',
                    unsafe_allow_html=True,
                )

st.subheader("Filtered data")
st.dataframe(filtered_df, use_container_width=True)

