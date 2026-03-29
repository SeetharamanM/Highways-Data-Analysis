"""
Final Award Table - Ward 10 page with filters and summary.
"""
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Final Award Table - VNBR", layout="wide")

st.title("Final Award Table")

# Get the directory of the current script
SCRIPT_DIR = Path(__file__).parent.parent


def format_indian_amount(amount):
    """Format amount with Indian style comma separators (e.g., 1,50,000)"""
    s = str(int(amount))
    if len(s) <= 3:
        return f"₹ {s}"
    else:
        # Last 3 digits
        last_three = s[-3:]
        # Remaining digits
        remaining = s[:-3]
        # Add commas every 2 digits for remaining
        if remaining:
            remaining = ','.join([remaining[max(0, i-2):i] for i in range(len(remaining), 0, -2)][::-1])
            return f"₹ {remaining},{last_three}"
        return f"₹ {last_three}"


# Load data
@st.cache_data
def load_data_v2():
    file_path = SCRIPT_DIR / "Final Award table.xlsx"
    
    # Read reference/title from first row
    df_header = pd.read_excel(file_path, header=None, nrows=1)
    reference_text = str(df_header.iloc[0, 0]) if not df_header.empty else ""
    
    # Read actual data from row 2 onwards
    df = pd.read_excel(file_path, header=1)
    
    # Clean column names - remove extra spaces
    df.columns = df.columns.str.strip()
    
    # Convert numeric columns
    numeric_cols = ['Acquired Land Area (Sqm)', 'Structures Value', 'Tree Value', 'Compensation Amount']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Clean text columns
    df['Village'] = df['Village'].astype(str).str.strip()
    df['Block'] = df['Block'].astype(str).str.strip()
    df['Land Owners'] = df['Land Owners'].fillna('').astype(str)
    
    return df, reference_text


df, reference_text = load_data_v2()

# Display reference/title from Excel top row
if reference_text and reference_text != 'nan':
    st.markdown(f"<h3 style='text-align: center; color: #1f77b4;'>{reference_text}</h3>", unsafe_allow_html=True)
    st.markdown("---")

# Grand Totals (without filters)
st.subheader("Grand Totals")

grand_land_area = df['Acquired Land Area (Sqm)'].sum()
grand_compensation = df['Compensation Amount'].sum()
grand_structure = df['Structures Value'].sum()
grand_tree = df['Tree Value'].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style="background-color: #e3f2fd; padding: 15px; border-radius: 10px; text-align: center; border-left: 5px solid #1976d2;">
        <p style="color: #1976d2; margin: 0; font-size: 12px; font-weight: bold;">Total Land Area</p>
        <p style="color: #333; margin: 5px 0 0 0; font-size: 18px; font-weight: bold;">{grand_land_area:,.2f} Sq.m</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background-color: #e8f5e9; padding: 15px; border-radius: 10px; text-align: center; border-left: 5px solid #388e3c;">
        <p style="color: #388e3c; margin: 0; font-size: 12px; font-weight: bold;">Total Compensation</p>
        <p style="color: #333; margin: 5px 0 0 0; font-size: 18px; font-weight: bold;">{format_indian_amount(grand_compensation)}</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background-color: #fff3e0; padding: 15px; border-radius: 10px; text-align: center; border-left: 5px solid #f57c00;">
        <p style="color: #f57c00; margin: 0; font-size: 12px; font-weight: bold;">Total Structures</p>
        <p style="color: #333; margin: 5px 0 0 0; font-size: 18px; font-weight: bold;">{format_indian_amount(grand_structure)}</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="background-color: #fce4ec; padding: 15px; border-radius: 10px; text-align: center; border-left: 5px solid #c2185b;">
        <p style="color: #c2185b; margin: 0; font-size: 12px; font-weight: bold;">Total Tree Value</p>
        <p style="color: #333; margin: 5px 0 0 0; font-size: 18px; font-weight: bold;">{format_indian_amount(grand_tree)}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Sidebar filters
st.sidebar.header("Filters")

# Get unique values
villages = sorted(df['Village'].unique())
blocks = sorted(df['Block'].unique())

# Get unique land owners (handle multiple owners per cell)
all_owners = []
for owners in df['Land Owners']:
    if owners:
        owners_list = [o.strip() for o in str(owners).split(',') if o.strip()]
        all_owners.extend(owners_list)
unique_owners = sorted(list(set(all_owners)))

# Create filters with Select All option
st.sidebar.markdown("**Village**")
select_all_villages = st.sidebar.checkbox("Select All Villages", value=True)
if select_all_villages:
    selected_villages = villages
else:
    selected_villages = st.sidebar.multiselect("Select Village", options=villages, default=[], label_visibility="collapsed")

st.sidebar.markdown("**Block**")
select_all_blocks = st.sidebar.checkbox("Select All Blocks", value=True)
if select_all_blocks:
    selected_blocks = blocks
else:
    selected_blocks = st.sidebar.multiselect("Select Block", options=blocks, default=[], label_visibility="collapsed")

st.sidebar.markdown("**Land Owners**")
select_all_owners = st.sidebar.checkbox("Select All Land Owners", value=True)
if select_all_owners:
    selected_land_owners = unique_owners
else:
    selected_land_owners = st.sidebar.multiselect("Select Land Owners", options=unique_owners, default=[], label_visibility="collapsed")

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
    (df['Village'].isin(selected_villages)) &
    (df['Block'].isin(selected_blocks)) &
    land_owner_mask
]

# Filtered Summary Cards
st.subheader("Filtered Summary")

total_land_area = filtered_df['Acquired Land Area (Sqm)'].sum()
total_compensation = filtered_df['Compensation Amount'].sum()
total_structure = filtered_df['Structures Value'].sum()
total_tree = filtered_df['Tree Value'].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style="background-color: #e3f2fd; padding: 15px; border-radius: 10px; text-align: center; border-left: 5px solid #1976d2;">
        <p style="color: #1976d2; margin: 0; font-size: 12px; font-weight: bold;">Filtered Land Area</p>
        <p style="color: #333; margin: 5px 0 0 0; font-size: 18px; font-weight: bold;">{total_land_area:,.2f} Sq.m</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background-color: #e8f5e9; padding: 15px; border-radius: 10px; text-align: center; border-left: 5px solid #388e3c;">
        <p style="color: #388e3c; margin: 0; font-size: 12px; font-weight: bold;">Filtered Compensation</p>
        <p style="color: #333; margin: 5px 0 0 0; font-size: 18px; font-weight: bold;">{format_indian_amount(total_compensation)}</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background-color: #fff3e0; padding: 15px; border-radius: 10px; text-align: center; border-left: 5px solid #f57c00;">
        <p style="color: #f57c00; margin: 0; font-size: 12px; font-weight: bold;">Filtered Structures</p>
        <p style="color: #333; margin: 5px 0 0 0; font-size: 18px; font-weight: bold;">{format_indian_amount(total_structure)}</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="background-color: #fce4ec; padding: 15px; border-radius: 10px; text-align: center; border-left: 5px solid #c2185b;">
        <p style="color: #c2185b; margin: 0; font-size: 12px; font-weight: bold;">Filtered Tree Value</p>
        <p style="color: #333; margin: 5px 0 0 0; font-size: 18px; font-weight: bold;">{format_indian_amount(total_tree)}</p>
    </div>
    """, unsafe_allow_html=True)

# Detailed Data Table
st.subheader("Detailed Data")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)

# Filter Summary
st.sidebar.markdown("---")
st.sidebar.subheader("Filter Summary")
st.sidebar.write(f"**Records shown:** {len(filtered_df)} of {len(df)}")
st.sidebar.write(f"**Selected villages:** {len(selected_villages)}")
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
