"""
VNBR 15-1 Data Analysis page with summary tabs and filters.
"""
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="VNBR 15-1 Data", layout="wide")

st.title("VNBR 15-1 Land Acquisition Data")

# Load and clean data
@st.cache_data
def load_data():
    df = pd.read_excel("vnbr 15-1.xlsx")
    
    # Clean the data - handle missing values and convert to numeric
    df['Extent to be acquired (in Sqm)'] = pd.to_numeric(df['Extent to be acquired (in Sqm)'], errors='coerce')
    df['Extent to be acquired (in Sqm)'].fillna(0, inplace=True)
    
    # Clean Land Owners column - split multiple owners and create unique owner list
    df['Land Owners'] = df['Land Owners'].fillna('')
    
    # Create a list of all unique land owners across all records
    all_owners = []
    for owners in df['Land Owners']:
        if owners:
            owners_list = [owner.strip() for owner in str(owners).split(',') if owner.strip()]
            all_owners.extend(owners_list)
    
    unique_owners = list(set(all_owners))
    
    # Count owners per record (for individual record analysis)
    df['Owner Count'] = df['Land Owners'].apply(lambda x: len([owner.strip() for owner in str(x).split(',') if owner.strip()]) if x else 0)
    
    return df, unique_owners

df, unique_owners = load_data()

# Sidebar filters
st.sidebar.header("Filters")

# Get unique values for filters
villages = sorted(df['Villages'].unique())
subdivisions = sorted(df['New Sub division No.'].dropna().unique())
land_owners = sorted(unique_owners)

# Create filters
selected_villages = st.sidebar.multiselect(
    "Select Villages",
    options=villages,
    default=villages
)

selected_subdivisions = st.sidebar.multiselect(
    "Select New Sub division No.",
    options=subdivisions,
    default=subdivisions
)

selected_land_owners = st.sidebar.multiselect(
    "Select Land Owners",
    options=land_owners,
    default=land_owners  # Show all by default
)

# Filter data based on selections - fix land owner filtering
if selected_land_owners:
    # Create mask for land owners - check if any selected owner is in the record
    def has_selected_owner(owners_str):
        if not owners_str:
            return False
        return any(owner in str(owners_str) for owner in selected_land_owners)
    
    land_owner_mask = df['Land Owners'].apply(has_selected_owner)
else:
    land_owner_mask = pd.Series([True] * len(df))

filtered_df = df[
    (df['Villages'].isin(selected_villages)) &
    (df['New Sub division No.'].isin(selected_subdivisions)) &
    land_owner_mask
]

# Create tabs
tab1, tab2 = st.tabs(["Summary Statistics", "Detailed Data"])

with tab1:
    st.header("Summary Statistics")
    
    # Calculate summary statistics with unique land owners per village
    village_summary = filtered_df.groupby('Villages').agg({
        'Extent to be acquired (in Sqm)': 'sum',
        'New Sub division No.': 'nunique',
        'Owner Count': 'sum'
    }).reset_index()
    
    # Calculate unique land owners per village
    village_unique_owners = {}
    for village in filtered_df['Villages'].unique():
        village_data = filtered_df[filtered_df['Villages'] == village]
        village_owners = []
        for owners in village_data['Land Owners']:
            if owners:
                owners_list = [owner.strip() for owner in str(owners).split(',') if owner.strip()]
                village_owners.extend(owners_list)
        village_unique_owners[village] = len(set(village_owners))
    
    village_summary['Total Land Owners'] = village_summary['Villages'].map(village_unique_owners)
    
    village_summary.columns = ['Village', 'Total Extent to be Acquired (Sqm)', 'Total New Sub Division No.', 'Total Owner Count', 'Total Land Owners']
    
    # Display summary table
    st.subheader("Village-wise Summary")
    st.dataframe(village_summary, use_container_width=True)
    
    # Overall Summary Cards
    st.subheader("Overall Summary")
    
    # Calculate totals
    total_extent = filtered_df['Extent to be acquired (in Sqm)'].sum()
    total_subdivisions = filtered_df['New Sub division No.'].nunique()
    
    # Calculate unique land owners across all filtered data
    all_filtered_owners = []
    for owners in filtered_df['Land Owners']:
        if owners:
            owners_list = [owner.strip() for owner in str(owners).split(',') if owner.strip()]
            all_filtered_owners.extend(owners_list)
    unique_filtered_owners = len(set(all_filtered_owners))
    
    # Display cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="**Total Acquired Land**",
            value=f"{total_extent:,.2f} Sq.m"
        )
    
    with col2:
        st.metric(
            label="**Total Subdivisions**",
            value=f"{total_subdivisions}"
        )
    
    with col3:
        st.metric(
            label="**Unique Land Owners**",
            value=f"{unique_filtered_owners}"
        )
    
    # Charts
    st.subheader("Visualizations")
    
    # Extent by village chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.bar_chart(village_summary.set_index('Village')['Total Extent to be Acquired (Sqm)'])
    
    with col2:
        st.bar_chart(village_summary.set_index('Village')['Total Land Owners'])
    
    # Structures and Trees Table
    st.subheader("Items with Structures and Trees")
    structures_trees_df = filtered_df[
        (filtered_df['Structures'].notna() & (filtered_df['Structures'] != '') & (filtered_df['Structures'] != '---')) |
        (filtered_df['Trees'].notna() & (filtered_df['Trees'] != '') & (filtered_df['Trees'] != '---'))
    ][['Villages', 'New Sub division No.', 'Structures', 'Trees', 'Land Owners', 'Extent to be acquired (in Sqm)']]
    
    if not structures_trees_df.empty:
        st.dataframe(structures_trees_df, use_container_width=True)
        st.write(f"**Total records with Structures/Trees:** {len(structures_trees_df)}")
    else:
        st.info("No records with Structures or Trees data found in current filter.")

with tab2:
    st.header("Detailed Data")
    
    # Display filtered data
    st.dataframe(filtered_df, use_container_width=True)
    
    # Download button for filtered data
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name="vnbr_15_1_filtered_data.csv",
        mime="text/csv"
    )

# Show filter summary
st.sidebar.markdown("---")
st.sidebar.subheader("Filter Summary")
st.sidebar.write(f"**Records shown:** {len(filtered_df)} of {len(df)}")
st.sidebar.write(f"**Selected villages:** {len(selected_villages)}")
st.sidebar.write(f"**Selected subdivisions:** {len(selected_subdivisions)}")
st.sidebar.write(f"**Selected land owners:** {len(selected_land_owners)}")
