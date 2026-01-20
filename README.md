## Repository Structure

```text
sales-analytics-system/
├── README.md
├── requirements.txt
├── main.py                   # The "Entry Point" of your app
├── data/
│   └── sales_data.txt        # Raw input data
├── output/
│   ├── sales_summary.txt     # Results/Reports
│   └── enriched_sales_data.txt
└── utils/
    ├── __init__.py           # Makes utils a package
    ├── file_handler.py       # Functions for read/write
    ├── data_processor.py     # Functions for analysis (trends, peak days)
    ├── report_generation.py  # Report Generation code
    └── api_handler.py        # Functions for enrichment logic