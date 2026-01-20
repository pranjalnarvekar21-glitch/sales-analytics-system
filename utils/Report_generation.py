"""
Report Generation.

"""
from utils.data_process import calculate_total_revenue, region_wise_sales, top_selling_products, customer_analysis, daily_sales_trend, find_peak_sales_day, low_performing_products
from datetime import datetime
import os

def generate_sales_report(transactions, enriched, output_file='sales_report.txt'):

    
    # --- Pre-calculations ---
    total_rev = calculate_total_revenue(transactions)
    total_tx = len(transactions)
    aov = total_rev / total_tx if total_tx > 0 else 0
    
    # Date Range discovery
    all_dates = sorted([t['Date'] for t in transactions])
    date_range = f"{all_dates[0]} to {all_dates[-1]}" if all_dates else "N/A"

    # Directory
    dir_name = os.path.dirname(output_file)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    # Writing into the  Report
    with open(output_file, 'w', encoding='utf-8') as f:
        # 1. HEADER creation
        f.write("=" * 50 + "\n")
        f.write("           SALES ANALYTICS REPORT\n")
        f.write(f"         Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"         Records Processed: {total_tx}\n")
        f.write("=" * 50 + "\n\n")

        # 2. overall SUMMARY
        f.write("OVERALL SUMMARY\n")
        f.write("-" * 50 + "\n")
        f.write(f"Total Revenue:       ₹{total_rev:,.2f}\n")
        f.write(f"Total Transactions:  {total_tx}\n")
        f.write(f"Average Order Value: ₹{aov:,.2f}\n")
        f.write(f"Date Range:          {date_range}\n\n")

        # 3. REGION-WISE Performance
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Region':<15} {'Sales':<15} {'% Total':<10} {'Trans':<5}\n")
        
        RegSales=region_wise_sales(transactions)

        for region, metrics in RegSales.items():
            # Clean up empty region names
            display_name = region if region != '' else "Unknown"
    
            sales = metrics['total_sales']
            pct   = metrics['percentage']
            count = metrics['transaction_count']
            f.write(f"{display_name:<15} {sales:<15,.2f} {pct:<10} {count:<5}\n")

        f.write("\nTOP 5 PRODUCTS\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Rank':<6} {'Product Name':<20} {'Qty':<8} {'Revenue':<10}\n")

        Top5Products=top_selling_products(transactions,n=5)
        
        for rank, (name, qty, revenue) in enumerate(Top5Products, start=1):
         f.write(f"{rank:<6}  {name:<20}  {qty:>8}  ₹{revenue:>11,.2f}\n")

    
        f.write("\nTOP 5 CUSTOMERS\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Rank':<5} {'Customer ID':<15} {'Total Spent':>12}  {'Orders':>8}\n")

        Top5Customer = list(customer_analysis(transactions).items())[:5]
        for rank, (cid, data) in enumerate(Top5Customer, start=1):
          total = data['total_spent']
          count = data['purchase_count']
          f.write(f"{rank:<5} {str(cid):<15}  {total:>12,.2f}  {count:>8}\n")

        f.write("\n DAILY SALES TREND\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Date':<12}  {'Revenue':>15}  {'Transactions':>15}  {'Unique Customers':>18}\n")
        trend = daily_sales_trend(transactions)
        for date, metrics in trend.items():
            rev = metrics['revenue']
            tx_count = metrics['transaction_count']
            unique_c = metrics['unique_customers']
            f.write(f"{date:<12} {rev:>15,.2f} {tx_count:>15}  {unique_c:>18}\n")


        peak_date, peak_rev, peak_count = find_peak_sales_day(transactions)
        low_products = low_performing_products(transactions, threshold=10)

        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("="*50 + "\n")

        f.write(f"\nBEST SELLING DAY:\n")
        f.write(f"  Date: {peak_date}\n")
        f.write(f"  Total Revenue: ${peak_rev:,.2f}\n")
        f.write(f"  Transaction Count: {peak_count}\n")

        f.write(f"\nLOW PERFORMING PRODUCTS (Quantity < 10):\n")
        if not low_products:
            f.write("  No low performing products found.\n")
        else:
            f.write(f"  {'Product Name':<25}  {'Qty':<5}  {'Revenue':>12}\n")
            f.write("  " + "-"*48 + "\n")
            for name, qty, rev in low_products:
                f.write(f"  {name:<25}  {qty:<5}  {rev:>12,.2f}\n")

        f.write(f"\nAVERAGE TRANSACTION VALUE PER REGION:\n")
        
        region_data = {}
        for t in transactions:
            reg = t.get('Region', 'Unknown')
            rev = t['Quantity'] * t['UnitPrice']
            if reg not in region_data:
                region_data[reg] = {'rev': 0.0, 'count': 0}
            region_data[reg]['rev'] += rev
            region_data[reg]['count'] += 1
            
        for reg, stats in region_data.items():
            avg = stats['rev'] / stats['count']
            f.write(f"  {reg:<15}: ${avg:>10,.2f} per transaction\n")
        
        f.write("\nAPI ENRICHMENT SUMMARY\n")
        f.write("-" * 50 + "\n")    

        total_products = len(enriched)

        success_count = sum(1 for t in enriched if t.get('API_Match') is True)
    
        # Percentage
        success_rate = (success_count / total_products * 100) if total_products > 0 else 0
    
        f.write(f"Total Products Processed: {total_products}\n")
        f.write(f"Successful Enrichments:   {success_count}\n")
        f.write(f"Success Rate:             {success_rate:.2f}%\n")
        

        f.write("\n" + "-" * 50 + "\n")
        f.write("               *** END OF REPORT ***\n")