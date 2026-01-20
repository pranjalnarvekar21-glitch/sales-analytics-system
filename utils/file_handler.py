
"""
Function for Reading the sales data,
def read_sales_data(filename):

Requirements:
    - Use 'with' statement
    - Handle different encodings (try 'utf-8', 'latin-1', 'cp1252')
    - Handle FileNotFoundError with appropriate error message
    - Skip the header row
    - Remove empty lines
"""

def read_sales_data(filename):
#Defined Encoding types
    encod = ['utf-8', 'latin-1', 'cp1252']
    
    for enc in encod:
        try:
            with open(filename, 'r', encoding=enc) as file:
                lines = file.readlines()
                return [line.strip() for line in lines if line.strip()][1:]
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"Error: {filename} not found.")
            return []
    
    return []
"""
Function for parsing the raw data and handling the data quality issues,
Requirements:
    - Split by pipe delimiter '|'
    - Handle commas within ProductName (remove or replace)
    - Remove commas from numeric fields and convert to proper types
    - Convert Quantity to int
    - Convert UnitPrice to float
    - Skip rows with incorrect number of fields

"""
def parse_transactions(raw_lines):
    transactions = []
    for l in raw_lines:
        parts = l.split('|')
        if len(parts) != 8:
            continue
        try:
            data = {
                'TransactionID': parts[0],
                'Date': parts[1],
                'ProductID': parts[2],
                'ProductName': parts[3].replace(',', ''),
                'Quantity': int(parts[4].replace(',', '')),
                'UnitPrice': float(parts[5].replace(',', '')),
                'CustomerID': parts[6],
                'Region': parts[7]
            }
            transactions.append(data)
        except ValueError:
            continue
    return transactions

"""
A Function to validate and filter the data
    Parameters:
    - transactions: list of transaction dictionaries
    - region: filter by specific region (optional)
    - min_amount: minimum transaction amount (Quantity * UnitPrice) (optional)
    - max_amount: maximum transaction amount (optional)

    Returns: tuple (valid_transactions, invalid_count, filter_summary)

    Validation Rules:
    - Quantity must be > 0
    - UnitPrice must be > 0
    - All required fields must be present
    - TransactionID must start with 'T'
    - ProductID must start with 'P'
    - CustomerID must start with 'C'

    Filter Display:
    - Print available regions to user before filtering
    - Print transaction amount range (min/max) to user
    - Show count of records after each filter applied
"""

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid_data, inv_count = [], 0
    reg_filt, amt_filt = 0, 0
    for t in transactions:
        # Validation Part
        is_valid = (t.get('Quantity', 0) > 0 and t.get('UnitPrice', 0) > 0 and
                    t['TransactionID'].startswith('T') and
                    t['ProductID'].startswith('P') and
                    t['CustomerID'].startswith('C'))

        if not is_valid: inv_count += 1; continue

        # Filtering part
        total = t['Quantity'] * t['UnitPrice']
        if region and t['Region'] != region: reg_filt += 1; continue
        if (min_amount and total < min_amount) or (max_amount and total > max_amount):
            amt_filt += 1; continue
        valid_data.append(t)

    summary = {'total_input': len(transactions), 'invalid': inv_count,
               'filtered_by_region': reg_filt, 'filtered_by_amount': amt_filt,
               'final_count': len(valid_data)}


    return valid_data, inv_count, summary