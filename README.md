# Highways Data Analysis

A Streamlit app for viewing and analysing highways restoration tender data—filter by columns, view totals by contractor and TN No, and explore data in tables.

## Features

- **Landing page** with links to each data file
- **Restoration Tender** page:
  - Load default file (`restoration tender.csv`) or upload CSV/Excel
  - **Filters** by TN No, Name of Road, Contractor, AS (L), CV (L)
  - **Overall totals**: coloured tiles for total AS (L) and CV (L)
  - **By TN No**: coloured tiles for total AS and CV (L) per TN No
  - **By contractor**: sum of AS (L) and CV (L) per contractor
  - **Filtered data** table

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

The app opens in your browser (typically http://localhost:8501).

## Project structure

```
├── app.py                 # Landing page
├── pages/
│   └── 1_restoration_tender.py   # Restoration Tender data page
├── requirements.txt
├── run_app.ps1            # Run script (Windows)
├── restoration tender.csv # Default data file (optional)
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
