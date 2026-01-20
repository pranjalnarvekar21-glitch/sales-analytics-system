"""
2.1.a.Function to calculate Total Revenues
"""

def calculate_total_revenue(transactions):
    #Calculates sum of (Quantity * UnitPrice)
    revenue = sum(
        t['Quantity'] * t['UnitPrice']
        for t in transactions
    )
    return float(revenue)

"""
2.1.b. Function to do Region wise sales Analysis.
"""

def region_wise_sales(transactions):
    stats = {}
    grand_total = 0.0

    for t in transactions:
        reg = t['Region']
        sale = t['Quantity'] * t['UnitPrice']
        grand_total += sale

        if reg not in stats:
            stats[reg] = {'total_sales': 0.0, 'transaction_count': 0}
        stats[reg]['total_sales'] += sale
        stats[reg]['transaction_count'] += 1
    # Calculate %
    for reg in stats:
        share = (stats[reg]['total_sales'] / grand_total) * 100
        stats[reg]['percentage'] = round(share, 2)
    # Sort- total_sales desc
    sorted_items = sorted(stats.items(), key=lambda x: x[1]['total_sales'], reverse=True)
    return dict(sorted_items)
"""
2.1.c. Function to get the Top Selling Products.
"""

def top_selling_products(transactions, n=5):
    product_stats = {}
    for t in transactions:
        name = t['ProductName']
        qty, price = t['Quantity'], t['UnitPrice']
        revenue = qty * price
        if name not in product_stats:
            product_stats[name] = {'qty': 0, 'rev': 0.0}
        product_stats[name]['qty'] += qty
        product_stats[name]['rev'] += revenue
    # Form- list of tuples
    product_list = [
        (name, data['qty'], data['rev'])
        for name, data in product_stats.items()
    ]
    # Sort- Quantity desc
    product_list.sort(key=lambda x: x[1], reverse=True)
    return product_list[:n]

"""
2.1.d. Function for getting the Customer Purcase Analysis
"""

def customer_analysis(transactions):
    stats = {}
    for t in transactions:
        cid = t['CustomerID']
        amount = t['Quantity'] * t['UnitPrice']
        prod = t['ProductName']
        if cid not in stats:
            stats[cid] = {'total_spent': 0.0, 'purchase_count': 0, 'products': set()}
        stats[cid]['total_spent'] += amount
        stats[cid]['purchase_count'] += 1
        stats[cid]['products'].add(prod)
    # Calc averages and format results
    for cid, data in stats.items():
        data['avg_order_value'] = round(data['total_spent'] / data['purchase_count'], 2)
        data['products_bought'] = sorted(list(data.pop('products')))
    # Sort by total_spent descending
    sorted_items = sorted(stats.items(), key=lambda x: x[1]['total_spent'], reverse=True)
    return dict(sorted_items)

"""
2.2.a Functino for getting Daily Sales trends.
"""

def daily_sales_trend(transactions):
    trend = {}
    for t in transactions:
        date = t['Date']
        rev = t['Quantity'] * t['UnitPrice']
        cust = t['CustomerID']
        if date not in trend:
            trend[date] = {'revenue': 0.0, 'transaction_count': 0, 'customers': set()}
        trend[date]['revenue'] += rev
        trend[date]['transaction_count'] += 1
        trend[date]['customers'].add(cust)
    # Final metrics
    for date, data in trend.items():
        data['unique_customers'] = len(data.pop('customers'))
        data['revenue'] = round(data['revenue'], 2)
    # Return sort- date
    return dict(sorted(trend.items()))

"""
2.2.b. Fucntion to get Peak Sales by Day.
"""

def find_peak_sales_day(transactions):
 # Two dicts- revenue and transaction counts
    daily_revenue = {}
    daily_count = {}
    for t in transactions:
        date = t['Date']
        revenue = t['Quantity'] * t['UnitPrice']
   
    if date in daily_revenue:
        daily_revenue[date] += revenue
        daily_count[date] += 1
    else:
        daily_revenue[date] = revenue
        daily_count[date] = 1
# Variables - highest values found
    peak_date = ""
    max_revenue = 0.0
    for date in daily_revenue:
     if daily_revenue[date] > max_revenue:
       max_revenue = daily_revenue[date]
       peak_date = date
    return (peak_date, max_revenue, daily_count[peak_date])

"""
2.3.a. Functino to get the Low performing Products.
"""
def low_performing_products(transactions, threshold=10):
    product_counts = {}
    product_revenue = {}
    for t in transactions:
        name = t['ProductName']
        qty = t['Quantity']
        rev = qty * t['UnitPrice']
        if name in product_counts:
            product_counts[name] += qty
            product_revenue[name] += rev
        else:
            product_counts[name] = qty
            product_revenue[name] = rev
    low_performers = []
    for name in product_counts:
        total_qty = product_counts[name]
        if total_qty < threshold:
            total_rev = product_revenue[name]
            low_performers.append((name, total_qty, total_rev))
    # Sort- quantity asc
    low_performers.sort(key=lambda x: x[1])
    return low_performers