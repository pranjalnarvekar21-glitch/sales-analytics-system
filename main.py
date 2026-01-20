"""
The Main.py is the file which integrates all parts of the assignment. 
 Execution Sequence
    Workflow:
    1. Print welcome message
    2. Read sales data file (handle encoding)
    3. Parse and clean transactions
    4. Display filter options to user
       - Show available regions
       - Show transaction amount range
       - Ask if user wants to filter (y/n)
    5. If yes, ask for filter criteria and apply
    6. Validate transactions
    7. Display validation summary
    8. Perform all data analyses (call all functions from Part 2)
    9. Fetch products from API
    10. Enrich sales data with API info
    11. Save enriched data to file
    12. Generate comprehensive report
    13. Print success message with file locations

    Error Handling:
    - Wrap entire process in try-except
    - Display user-friendly error messages
    - Don't let program crash on errors
"""
from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
from utils.Report_generation import generate_sales_report
from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data, save_enriched_data
from pathlib import Path



def main():
    try:
        print("=" * 40)
        print("         SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # Loading and Parsing the file
        print("\n[1/10] Reading sales data...")
        
        # Get the directory of the current script
        script_dir = Path(__file__).parent 

        # Combine the directory with your filename
        data_file = script_dir / "data/sales_data.txt"
        raw_lines = read_sales_data(data_file)
        
        print("[2/10] Parsing and cleaning transactions...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records")

        # Interactive Filtering
        print("\n[3/10] Filter Options...")
        regions = sorted(list(set(t.get('Region', 'N/A') for t in transactions)))
        print(f"Available Regions: {', '.join(regions)}")
        
        want_filter = input("Do you want to filter data? (y/n): ").lower()
        
        if want_filter == 'y':
            reg_input = input("Enter specific Region: ")
            valid_tx, _, summary = validate_and_filter(transactions, region=reg_input)
        else:
            valid_tx, _, summary = validate_and_filter(transactions)

        # Validation Summary
        print(f"\n[4/10] Validating transactions...")
        print(f"✓ Valid: {len(valid_tx)} | Invalid: {summary['invalid']}")

        # The  Analytical Part 
        print("\n[5/10] Analyzing sales performance...")
        # Data can be viewed in the report. sales_report.txt
        print("✓ Analysis completed")

        # API Integration
        print("\n[6/10] Fetching product data from API...")
        api_data = fetch_all_products()
        product_map = create_product_mapping(api_data)
        
        print("[7/10] Enriching sales data...")
        enriched = enrich_sales_data(valid_tx, product_map)

        # 9: Disk Persistence
        print("\n[8/10] Saving enriched data...")
        save_enriched_data(enriched, 'data/enriched_sales_data.txt')

        # 10: Human-Readable Reporting
        print("[9/10] Generating report...")
        generate_sales_report(valid_tx, enriched, 'output/sales_report.txt')

        print("\n[10/10] Process Complete!")
        print("=" * 40)
        print(f"Success! Enriched Data: data/enriched_sales_data.txt")
        print(f"Analytics Report: output/sales_report.txt")
        print("=" * 40)

    except Exception as e:
        print(f"\n!!! CRITICAL SYSTEM ERROR !!!")
        print(f"Details: {e}")
        
if __name__ == "__main__":
    main()