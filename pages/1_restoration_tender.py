"""
Data analysis page for restoration tender.csv — filters, tiles, contractor sums.
"""
import streamlit as st
import pandas as pd
from pathlib import Path

# Page title = file name (no extension, capitalised)
st.set_page_config(page_title="Restoration Tender", layout="wide")

st.title("Restoration Tender")

# Default data path (project root, one level up from pages/)
DEFAULT_DATA_PATH = Path(__file__).parent.parent / "restoration tender.csv"

# File upload or use default
st.sidebar.header("Data source")
use_upload = st.sidebar.checkbox("Upload a file", value=False)

if use_upload:
    uploaded = st.sidebar.file_uploader("Choose CSV or Excel", type=["csv", "xlsx", "xls"])
    if uploaded is None:
        st.info("Upload a CSV or Excel file to start.")
        st.stop()
    if uploaded.name.endswith(".csv"):
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_excel(uploaded)
else:
    if not DEFAULT_DATA_PATH.exists():
        st.error(f"Default file not found: {DEFAULT_DATA_PATH}. Upload a file or place data there.")
        st.stop()
    df = pd.read_csv(DEFAULT_DATA_PATH)

# Normalize column names (strip spaces)
df.columns = df.columns.str.strip()

# Coerce numeric columns (strip % and commas)
for col in df.columns:
    if col in df.columns and df[col].dtype == object:
        try:
            s = df[col].astype(str).str.replace(",", "").str.replace("%", "")
            num = pd.to_numeric(s, errors="coerce")
            if num.notna().sum() > len(df) * 0.5:
                df[col] = num
        except Exception:
            pass

# Ensure AS and CV (L) columns exist
as_col = next((c for c in df.columns if "AS" in c and "L" in c), next((c for c in df.columns if "AS" in c), None))
cv_l_col = next((c for c in df.columns if "CV" in c and "L" in c), None)
if not as_col:
    as_col = None
if not cv_l_col and "CV (L)" in df.columns:
    cv_l_col = "CV (L)"
cv_col = cv_l_col

for col in [as_col, cv_col]:
    if col and col in df.columns:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", ""), errors="coerce")

st.sidebar.header("Filters")

# Columns to exclude from filters
FILTER_EXCLUDE = {"Sl.No", "EW", "BT", "BT Percentage", "GST", "Contingencies", "CV"}

# Build filters per column
filtered_df = df.copy()
for col in df.columns:
    if col in FILTER_EXCLUDE:
        continue
    if df[col].dtype == "object" or (df[col].dtype.name in ("string", "object")):
        uniq = sorted(df[col].dropna().astype(str).unique().tolist())
        if len(uniq) <= 100:
            sel = st.sidebar.multiselect(f"**{col}**", options=uniq, default=uniq)
            if sel:
                filtered_df = filtered_df[filtered_df[col].astype(str).isin(sel)]
        else:
            st.sidebar.caption(f"{col}: too many values to filter")
    elif pd.api.types.is_numeric_dtype(df[col]):
        mn, mx = float(df[col].min()), float(df[col].max())
        low, high = st.sidebar.slider(f"**{col}**", min_value=mn, max_value=mx, value=(mn, mx))
        filtered_df = filtered_df[(filtered_df[col] >= low) & (filtered_df[col] <= high)]

# Overall total AS and CV (L) — colored tiles
if as_col and cv_col:
    total_as = filtered_df[as_col].sum()
    total_cv = filtered_df[cv_col].sum()
    st.markdown("""
    <style>
    .tile-as { background: linear-gradient(135deg, #1e88e5 0%, #42a5f5 100%); color: white; padding: 1rem 1.25rem; border-radius: 10px; margin-bottom: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .tile-cv { background: linear-gradient(135deg, #43a047 0%, #66bb6a 100%); color: white; padding: 1rem 1.25rem; border-radius: 10px; margin-bottom: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .tile-label { font-size: 0.85rem; opacity: 0.95; }
    .tile-value { font-size: 1.5rem; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)
    st.subheader("Overall totals")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f'<div class="tile-as"><div class="tile-label">Overall Total AS (L)</div><div class="tile-value">{total_as:,.2f}</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="tile-cv"><div class="tile-label">Overall Total CV (L)</div><div class="tile-value">{total_cv:,.2f}</div></div>',
            unsafe_allow_html=True,
        )

# Tiles: total AS and CV (L) for each TN No (colored)
tn_no_col = "TN No"
if tn_no_col in filtered_df.columns and as_col and cv_col:
    st.subheader("Total AS and CV (L) by TN No")
    by_tn = (
        filtered_df.groupby(tn_no_col, as_index=False)
        .agg({as_col: "sum", cv_col: "sum"})
    )
    n_per_row = 6
    for start in range(0, len(by_tn), n_per_row):
        chunk = by_tn.iloc[start : start + n_per_row]
        cols = st.columns(len(chunk))
        for j, (_, row) in enumerate(chunk.iterrows()):
            with cols[j]:
                tn = row[tn_no_col]
                as_val = f"{row[as_col]:,.2f}"
                cv_val = f"{row[cv_col]:,.2f}"
                st.markdown(
                    f'<div class="tile-as"><div class="tile-label">{tn} — Total AS (L)</div><div class="tile-value">{as_val}</div></div>'
                    f'<div class="tile-cv"><div class="tile-label">{tn} — Total CV (L)</div><div class="tile-value">{cv_val}</div></div>',
                    unsafe_allow_html=True,
                )

# Summary: sum of AS and CV for each contractor
contractor_col = "Contractor"
if contractor_col not in filtered_df.columns:
    contractor_col = next((c for c in filtered_df.columns if "contractor" in c.lower()), None)

if contractor_col and as_col and cv_col and contractor_col in filtered_df.columns:
    st.subheader("Sum of AS and CV by contractor")
    summary = (
        filtered_df.groupby(contractor_col, as_index=False)
        .agg({as_col: "sum", cv_col: "sum"})
        .rename(columns={as_col: f"Sum {as_col}", cv_col: f"Sum {cv_col}"})
    )
    summary = summary.sort_values(f"Sum {as_col}", ascending=False)
    st.dataframe(summary, use_container_width=True)

st.subheader("Filtered data")
st.dataframe(filtered_df, use_container_width=True)
