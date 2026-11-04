# E-commerce Sales Analysis

End-to-end descriptive analysis of the UCI Online Retail transaction dataset using Python, SQL, Excel and Power BI.

## Business questions
- How do revenue and order volume change over time?
- Which countries and products contribute most to revenue?
- What is average order value (AOV)?
- How concentrated is revenue among identified customers?
- How can customers be segmented using recency, frequency and monetary value (RFM)?

## Dataset and attribution
UCI Machine Learning Repository, [Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail). The dataset contains 541,909 transaction records from a UK-based online retailer between 2010 and 2011. Dataset citation: Chen (2015), DOI: https://doi.org/10.24432/C5BW33. The dataset is licensed under CC BY 4.0. The pipeline downloads the dataset at runtime; the raw file is not committed to this repository.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/analyze.py
```
The script writes cleaned data and an Excel workbook to `outputs/`.

## Repository structure
- `src/analyze.py` — data acquisition, cleaning, KPI analysis, RFM segmentation and Excel export.
- `sql/analysis.sql` — reusable SQL business questions.
- `powerbi/README.md` — data model, DAX measures and report-page instructions.
- `outputs/` — generated locally; excluded from version control.

## Metric definitions
Revenue is Quantity × UnitPrice. The primary sales analysis includes rows with valid dates, positive quantities and positive unit prices, and excludes cancellation invoice numbers beginning with `C`. AOV is total revenue divided by distinct invoice count. RFM recency is measured against the latest transaction date in the dataset.

## Limitations
This is descriptive analysis of historical data, not a causal or predictive study. Customer IDs are missing for some transactions. Product descriptions and transaction records may contain inconsistencies; the script retains a transparent filtered subset rather than silently modifying source records.
