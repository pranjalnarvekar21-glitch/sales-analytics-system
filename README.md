# Sales Analytics system
## Assignment 3
---

Student Name: Pranjal Pramod Shet Narvekar

Student ID: bitsom_ba_25071749

Email: pranjal.narvekar21@gmail.com

---
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
    ├── file_handler.py       # Functions for read/write
    ├── data_processor.py     # Functions for analysis (trends, peak days)
    ├── report_generation.py  # Report Generation code
    └── api_handler.py        # Functions for enrichment logic

```
## Code flow and requirement.
- Python version used to run the code is 3.13.9.
- in the Terminal run 'pip3 install requests', will be needed for the api_handler and main.py execution.
- Make sure all  files from utils are folder are run/executed successfully before running the main.py file.
- I have added the output Generated files into the output folder, you will get the files once the main.py is executed into your cwd.
