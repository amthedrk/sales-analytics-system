import requests
import time

def fetch_product_details(product_name):
    """
    Searches for a product on DummyJSON API.
    Returns: Category (str) or "Unknown".
    """
    url = f"https://dummyjson.com/products/search?q={product_name}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['products']:
                # Return the category of the first matching product
                return data['products'][0]['category']
    except Exception:
        pass
    return "Unknown"

def enrich_sales_data(transactions):
    """
    Enriches transaction data with product categories from API.
    Uses caching to avoid repeated API calls for the same product.
    """
    print("[6/10] Fetching product data from API...")
    
    enriched_data = []
    # Cache results to prevent hitting API for "Mouse" 50 times
    product_cache = {} 
    success_count = 0
    
    unique_products = set(t['ProductName'] for t in transactions)
    print(f"✓ Found {len(unique_products)} unique products to look up")

    for t in transactions:
        p_name = t['ProductName']
        
        # Check cache first
        if p_name in product_cache:
            category = product_cache[p_name]
        else:
            category = fetch_product_details(p_name)
            product_cache[p_name] = category
            # Tiny sleep to be polite to the API
            time.sleep(0.1)
        
        # Create new record with Category
        new_record = t.copy()
        new_record['Category'] = category
        enriched_data.append(new_record)
        
        if category != "Unknown":
            success_count += 1

    success_rate = (success_count / len(transactions)) * 100
    print(f"[7/10] Enriching sales data...\n✓ Enriched {success_count}/{len(transactions)} transactions ({success_rate:.1f}%)")
    
    return enriched_data