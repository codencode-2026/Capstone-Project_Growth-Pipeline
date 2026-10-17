Mamaearth Returns & Growth Intelligence Pipeline

An end-to-end connected data pipeline combining an SQLite relational layer, a Pandas data wrangling and EDA layer, and a Gemini GenAI narrative layer to analyze order returns, identify revenue leakage, and generate executive reports.

Repository Structure
.
├── README.md
├── sql/
│   ├── schema.sql
│   ├── seed_data.sql
│   └── reports.sql
├── data/
│   ├── customers.csv
│   ├── products.csv
│   └── orders.csv
├── analysis/
│   ├── clean_and_eda.py
│   └── visualize.py
├── visualizations/
│   ├── return_rate_by_payment.png
│   └── monthly_revenue_trend.png
└── narrator/
    ├── findings.json
    ├── generate_narrative.py
    └── sample_output.txt

    Pipeline Execution Order

    Step 1: SQL Relational Layer
    Run the database schema setup, load seed data into SQLite (mamaearth.db), and execute business reports:
    
    python run_sql_pipeline.py

    Input: data/customers.csv, data/products.csv, data/orders.csv

    Execution: Executes sql/schema.sql, populates database tables (sql/seed_data.sql), cleans empty string cells to NULL, and verifies table row counts (Customers: 45, Products: 16, Orders: 180).

    Queries: Runs all analytical reports defined in sql/reports.sql.

    Step 2: Python Data Wrangling & EDA Layer
    Clean the raw data, perform duplicate removal, impute missing values, reconcile revenue deltas, detect outliers, and generate visual reports:

    python analysis/clean_and_eda.py
    python analysis/visualize.py

    Data Cleaning & Reconciliation:
    Standardizes payment_method casing (CARD: 70, UPI: 55, COD: 55).
    Drops 5 exact duplicate rows (O0176–O0180), reducing order count from 180 to 175.
    Imputes missing discount_pct with 0 and missing rating with the median value (3.0).
    Reconciles raw revenue (INR 99,860.20) against cleaned revenue (INR 97,358.30), accounting for the exact INR 2,501.90 delta from the 5 duplicate rows.
    
    Key Findings:
    Identifies bulk order outliers (O0011 quantity 25, O0098 quantity 30).
    Confirms COD return rate hypothesis at 44.4% (vs 14.7% Card, 18.9% UPI).
    Identifies highest-risk segment: COD + Tier-2 cities at 54.5% return rate.
    Uncovers March 2026 as the true peak month (INR 20,318.90) after adjusting for January bulk outliers.

    Output Artifacts:
    Writes structured metrics to narrator/findings.json.
    Saves visualizations/return_rate_by_payment.png and visualizations/monthly_revenue_trend.png.

    Step 3: GenAI Executive Narrative Layer
    Generate the Situation-Complication-Resolution (SCR) executive report using the Gemini API or the built-in offline fallback:

    # Option A: Online Path (with Gemini API Key)
        set GEMINI_API_KEY=your_gemini_api_key_here
        python narrator/generate_narrative.py

    # Option B: Offline Fallback Path (No network or key required)
        python narrator/generate_narrative.py

    Integration: Reads verified numbers directly from narrator/findings.json.
    Execution Details:
    Uses parameter locking (temperature=0.0) for deterministic, factually locked output.
    System instruction enforces SCR formatting and strict adherence to provided figures without inventing metrics.
    Automatically falls back to deterministic template formatting if no API key is detected or if network requests fail.

    Verification: Checks generated narrative against all required key figures (97,358.30 revenue, 44.4% COD return rate, 54.5% Tier-2 COD rate, 2,501.90 delta, and March peak at 20,318.90) and saves the sample output to narrator/sample_output.