"""
API handler file.
BASE API : https://dummyjson.com/products

"""
import requests,re, os

def fetch_all_products():
    #Fetches all products from DummyJSON API
    url = 'https://dummyjson.com/products?limit=100'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Check errors
        data = response.json()
        raw_products = data.get('products', [])
        # Specified schema mappin
        formatted_products = []
        for p in raw_products:
            formatted_products.append({
                'id': p.get('id'),
                'title': p.get('title'),
                'category': p.get('category'),
                'brand': p.get('brand'),
                'price': p.get('price'),
                'rating': p.get('rating')
            })
        print(f"Successfully fetched {len(formatted_products)} products")
        return formatted_products
    except Exception as e:
        print(f"API Error: {e}")
        return []
    
"""
Fucntion to create a Product mapping : creates an ID-to-Info mapping for fast retrieval
"""

def create_product_mapping(api_products):

    mapping = {}
    for product in api_products:
        p_id = product.get('id')
        # Use ID as key, select specific fields for value
        mapping[p_id] = {
            'title': product.get('title'),
            'category': product.get('category'),
            'brand': product.get('brand'),
            'rating': product.get('rating')
        }
    return mapping  

"""
Fucntion to Enrich
"""

def enrich_sales_data(transactions, product_mapping):
    enriched_list = []
    for t in transactions:
      try:
    # Extract Product ID
        match = re.search(r'\d+', t['ProductID'])
        p_id = int(match.group()) if match else None
    # Enrich Logic
        api_info = product_mapping.get(p_id)
        t['API_Category'] = api_info.get('category') if api_info else None
        t['API_Brand'] = api_info.get('brand') if api_info else None
        t['API_Rating'] = api_info.get('rating') if api_info else None
        t['API_Match'] = api_info is not None
      except Exception:
          t['API_Match'] = False
    
      enriched_list.append(t)
    # CHECK IF LIST IS EMPTY before writing to file
    if not enriched_list:
        print("No data found to write.")
        return []
    
    # File Persistence
    os.makedirs('data', exist_ok=True)
    headers = list(enriched_list[0].keys())
    with open('data/enriched_sales_data.txt', 'w') as f:
        f.write('|'.join(headers) + '\\n')

        for row in enriched_list:
            line = '|'.join([str(row.get(h, "")) for h in headers])
            f.write(line + '\n')

    return enriched_list

"""
Helper Function to save the Enriched data: Saves enriched data to a pipe-delimited file.
"""

def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):

    if not enriched_transactions:
        return False
    # Directory
    dir_name = os.path.dirname(filename)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    # Headers extraction
    headers = list(enriched_transactions[0].keys())
    # Data write 
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('|'.join(headers) + '\n')

            for row in enriched_transactions:
                     values = []
                     for h in headers:
                        val = row.get(h)
                        values.append("" if val is None else str(val))

                     f.write('|'.join(values) + '\n')
        return True
    except IOError as e:
        print(f"Failed to write file: {e}")
        return False