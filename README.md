# Highways Data Analysis

A Streamlit app for viewing and analysing highways restoration tender data—filter by columns, view totals by contractor and TN No, and explore data in tables.

## Features

- **Landing page** with links to each analysis page
- **Restoration Tender** (`pages/1_restoration_tender.py`):
  - Load default file (`restoration tender.csv` / `Restoration Tender.csv`) or upload CSV/Excel
  - **Filters** by TN No, Name of Road, Contractor, AS (L), CV (L)
  - **Overall totals**: coloured tiles for total AS (L) and CV (L)
  - **By TN No**: coloured tiles for total AS (L) and CV (L) per TN No
  - **By contractor**: sum of AS (L) and CV (L) per contractor
  - **Filtered data** table
- **KU Estimate Details** (`pages/2_ku_estimate_details.py`):
  - Reads `KU_Estimate Details.csv` (row 1 = title, row 2 = header)
  - **Filter** by `Items`
  - Coloured tiles for:
    - **Total Amt (filtered)**
    - **% of Total** (optionally excluding `Lumpsum` via a checkbox)
  - Filtered data table
- **CRIDP 2026-27 Proposal** (`pages/3_cridp_2026_27_proposal.py`):
  - Reads `CRIDP 2026-27 Proposal.xlsx` (first row as header)
  - **Filters** by `Category`, `Road`, `Work Type`
  - Coloured tiles for:
    - **Total Length in KM (filtered)**
    - **Total Cost in Lakhs (filtered)**
  - Grouped tiles: totals of Length and Cost by `Category` & `Work Type` (filtered)
  - Filtered data table
- **SH Junction Details** (`pages/4_sh_junction_details.py`):
  - Reads `SH Junction Details.xlsx` (first row as header)
  - **Filters** by `Main Road`, `Branch Road`, `Type of Junction`
  - Detects the junction count column (e.g. `No of Junctions`) automatically
  - Coloured tiles for:
    - **No of Junctions (filtered)**
    - **No of Junctions (all items)**
  - Filtered data table

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/SeetharamanM/Highways-Data-Analysis.git
   cd Highways-Data-Analysis
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv streamlit
   # Windows PowerShell:
   .\streamlit\Scripts\Activate.ps1
   # Windows CMD:
   .\streamlit\Scripts\activate.bat
   # macOS/Linux:
   source streamlit/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Run the app

```bash
streamlit run app.py
```

Or on Windows with the helper script (after activating the env):

```powershell
.\run_app.ps1
```

The app opens in your browser (typically <http://localhost:8501>).

## Project structure

```text
├── app.py                            # Landing page
├── pages/
│   ├── 1_restoration_tender.py       # Restoration Tender data page
│   ├── 2_ku_estimate_details.py      # KU Estimate Details page
│   ├── 3_cridp_2026_27_proposal.py   # CRIDP 2026-27 Proposal page
│   └── 4_sh_junction_details.py      # SH Junction Details page
├── requirements.txt
├── run_app.ps1                       # Run script (Windows)
├── restoration tender.csv            # Default data file (optional)
├── KU_Estimate Details.csv           # Default KU estimate data (optional)
├── CRIDP 2026-27 Proposal.xlsx       # Default CRIDP data (optional)
├── SH Junction Details.xlsx          # Default SH junction data (optional)
└── README.md
```

## Requirements

- Python 3.8+
- streamlit >= 1.28.0
- pandas >= 2.0.0
- openpyxl >= 3.1.0 (for Excel uploads)

## Deploy on Render

1. Push this repo to GitHub (e.g. [SeetharamanM/Highways-Data-Analysis](https://github.com/SeetharamanM/Highways-Data-Analysis)).
2. Go to [render.com](https://render.com) and sign in (or sign up).
3. Click **New +** → **Web Service**.
4. Connect your GitHub account and select the repo `Highways-Data-Analysis`.
5. Render will use the `render.yaml` in the repo. Confirm:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
6. Choose a **Free** instance and click **Create Web Service**.
7. After the build finishes, your app will be at `https://<your-service-name>.onrender.com`.
