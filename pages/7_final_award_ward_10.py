"""
Final Award Table - Ward 10 page with filters and summary.
"""
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Final Award Table - Ward 10", layout="wide")

st.title("Final Award Table - Ward 10")

# Get the directory of the current script
SCRIPT_DIR = Path(__file__).parent.parent

# Load data
@st.cache_data
def load_data():
    file_path = SCRIPT_DIR / "Final Award table-WARD-10.xlsx"
    df = pd.read_excel(file_path, header=1)
    
    # Clean column names - remove extra spaces
    df.columns = df.columns.str.strip()
    
    # Convert numeric columns
    numeric_cols = ['Acquired Land Area (Sqm)', 'Structures Value', 'Tree Value', 'Compensation Amount']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Clean text columns
    df['Ward'] = df['Ward'].astype(str).str.strip()
    df['Block'] = df['Block'].astype(str).str.strip()
    df['Land Owners'] = df['Land Owners'].fillna('').astype(str)
    
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

# Get unique values
wards = sorted(df['Ward'].unique())
blocks = sorted(df['Block'].unique())

# Get unique land owners (handle multiple owners per cell)
all_owners = []
for owners in df['Land Owners']:
    if owners:
        owners_list = [o.strip() for o in str(owners).split(',') if o.strip()]
        all_owners.extend(owners_list)
unique_owners = sorted(list(set(all_owners)))

# Create filters
selected_wards = st.sidebar.multiselect("Select Ward", options=wards, default=wards)
selected_blocks = st.sidebar.multiselect("Select Block", options=blocks, default=blocks)
selected_land_owners = st.sidebar.multiselect("Select Land Owners", options=unique_owners, default=unique_owners[:20] if len(unique_owners) > 20 else unique_owners)

# Filter data
if selected_land_owners:
    def has_selected_owner(owners_str):
        if not owners_str:
            return False
        return any(owner in str(owners_str) for owner in selected_land_owners)
    land_owner_mask = df['Land Owners'].apply(has_selected_owner)
else:
    land_owner_mask = pd.Series([True] * len(df))

filtered_df = df[
    (df['Ward'].isin(selected_wards)) &
    (df['Block'].isin(selected_blocks)) &
    land_owner_mask
]

# Summary Cards
st.subheader("Summary")

total_land_area = filtered_df['Acquired Land Area (Sqm)'].sum()
total_compensation = filtered_df['Compensation Amount'].sum()
total_structure = filtered_df['Structures Value'].sum()
total_tree = filtered_df['Tree Value'].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="**Total Acquired Land Area**",
        value=f"{total_land_area:,.2f} Sq.m"
    )

with col2:
    st.metric(
        label="**Total Compensation Amount**",
        value=f"₹ {total_compensation:,.2f}"
    )

with col3:
    st.metric(
        label="**Total Structure Amount**",
        value=f"₹ {total_structure:,.2f}"
    )

with col4:
    st.metric(
        label="**Total Tree Valuation**",
        value=f"₹ {total_tree:,.2f}"
    )

# Detailed Data Table
st.subheader("Detailed Data")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)

# Filter Summary
st.sidebar.markdown("---")
st.sidebar.subheader("Filter Summary")
st.sidebar.write(f"**Records shown:** {len(filtered_df)} of {len(df)}")
st.sidebar.write(f"**Selected wards:** {len(selected_wards)}")
st.sidebar.write(f"**Selected blocks:** {len(selected_blocks)}")
st.sidebar.write(f"**Selected land owners:** {len(selected_land_owners)}")

# Download button
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name="final_award_ward_10_filtered.csv",
    mime="text/csv"
)
