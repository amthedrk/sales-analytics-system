from datetime import datetime

# --- PART 1: CLEANING & VALIDATION ---

def parse_and_clean_data(raw_lines):
    """
    Parses raw strings into dictionaries and handles type conversion.
    """
    cleaned_data = []
    
    for line in raw_lines:
        # Skip empty lines
        if not line.strip():
            continue
            
        parts = line.split('|')
        
        # Basic structure check (we need at least 8 columns)
        if len(parts) < 8:
            continue
            
        # Parse fields
        record = {
            "TransactionID": parts[0].strip(),
            "Date": parts[1].strip(),
            "ProductID": parts[2].strip(),
            "ProductName": parts[3].strip(),
            "Quantity": parts[4].strip(),
            "UnitPrice": parts[5].strip(),
            "CustomerID": parts[6].strip(),
            "Region": parts[7].strip()
        }
        
        # Clean Numeric Fields (Remove commas)
        try:
            # Handle Quantity
            qty_str = record["Quantity"].replace(',', '')
            record["Quantity"] = int(qty_str)
            
            # Handle Price
            price_str = record["UnitPrice"].replace(',', '')
            record["UnitPrice"] = float(price_str)
            
        except ValueError:
            # If numbers are unparseable, keep them as is; validation will catch them later
            pass
            
        cleaned_data.append(record)
        
    print(f"[2/10] Parsing and cleaning data...\n✓ Parsed {len(cleaned_data)} records")
    return cleaned_data

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates data rules and applies optional filters.
    Returns: (valid_transactions, invalid_count, filter_summary)
    """
    valid_transactions = []
    invalid_count = 0
    filter_summary = {"total_input": len(transactions), "filtered_by_region": 0, "filtered_by_amount": 0}
    
    print("[4/10] Validating transactions...")
    
    for t in transactions:
        is_valid = True
        
        # --- VALIDATION RULES ---
        
        # 1. TransactionID must start with 'T'
        if not str(t["TransactionID"]).startswith('T'):
            is_valid = False
            
        # 2. Missing CustomerID or Region
        if not t["CustomerID"] or not t["Region"]:
            is_valid = False
            
        # 3. Quantity <= 0
        if not isinstance(t["Quantity"], int) or t["Quantity"] <= 0:
            is_valid = False
            
        # 4. UnitPrice <= 0
        if not isinstance(t["UnitPrice"], (int, float)) or t["UnitPrice"] <= 0:
            is_valid = False
            
        if not is_valid:
            invalid_count += 1
            continue

        # --- FILTERING LOGIC (Optional) ---
        
        # Filter by Region
        if region and t["Region"].lower() != region.lower():
            filter_summary["filtered_by_region"] += 1
            continue
            
        # Filter by Amount (Revenue = Price * Qty)
        revenue = t["Quantity"] * t["UnitPrice"]
        
        if min_amount is not None and revenue < min_amount:
            filter_summary["filtered_by_amount"] += 1
            continue
            
        if max_amount is not None and revenue > max_amount:
            filter_summary["filtered_by_amount"] += 1
            continue
            
        # If it passes validation and filters, add to list
        valid_transactions.append(t)

    print(f"✓ Valid: {len(valid_transactions)} | Invalid: {invalid_count}")
    return valid_transactions, invalid_count, filter_summary


# --- PART 2: ANALYTICS FUNCTIONS ---

def calculate_sales_stats(transactions):
    """
    Calculates overall sales statistics.
    Returns: dict with total revenue, average order value, etc.
    """
    if not transactions:
        return {"total_revenue": 0, "total_transactions": 0, "avg_order_value": 0, "date_range": "N/A"}

    total_revenue = sum(t['Quantity'] * t['UnitPrice'] for t in transactions)
    total_transactions = len(transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions > 0 else 0
    
    # Get Date Range
    try:
        dates = [datetime.strptime(t['Date'], "%Y-%m-%d") for t in transactions]
        date_range = f"{min(dates).strftime('%Y-%m-%d')} to {max(dates).strftime('%Y-%m-%d')}"
    except ValueError:
        date_range = "Invalid Dates Found"

    print("[5/10] Analyzing sales data...\n✓ Analysis complete")
    
    return {
        "total_revenue": total_revenue,
        "total_transactions": total_transactions,
        "avg_order_value": avg_order_value,
        "date_range": date_range
    }

def analyze_sales_by_region(transactions):
    """
    Groups sales by region.
    Returns: Dictionary of region stats.
    """
    region_stats = {}
    total_revenue = sum(t['Quantity'] * t['UnitPrice'] for t in transactions)
    if total_revenue == 0: total_revenue = 1 # Avoid division by zero
    
    for t in transactions:
        region = t['Region']
        revenue = t['Quantity'] * t['UnitPrice']
        
        if region not in region_stats:
            region_stats[region] = {'revenue': 0, 'count': 0}
        
        region_stats[region]['revenue'] += revenue
        region_stats[region]['count'] += 1
        
    # Calculate percentage
    for r in region_stats:
        region_stats[r]['percentage'] = (region_stats[r]['revenue'] / total_revenue) * 100
        
    return region_stats

def identify_top_products(transactions):
    """
    Identifies top selling products by revenue.
    Returns: List of sorted products.
    """
    product_stats = {}
    
    for t in transactions:
        pid = t['ProductName']
        revenue = t['Quantity'] * t['UnitPrice']
        qty = t['Quantity']
        
        if pid not in product_stats:
            product_stats[pid] = {'revenue': 0, 'quantity': 0}
            
        product_stats[pid]['revenue'] += revenue
        product_stats[pid]['quantity'] += qty
        
    # Convert to list and sort
    sorted_products = sorted(product_stats.items(), key=lambda x: x[1]['revenue'], reverse=True)
    return sorted_products[:5]

def identify_top_customers(transactions):
    """
    Identifies top spending customers.
    """
    cust_stats = {}
    for t in transactions:
        cid = t['CustomerID']
        revenue = t['Quantity'] * t['UnitPrice']
        
        if cid not in cust_stats:
            cust_stats[cid] = {'revenue': 0, 'count': 0}
        cust_stats[cid]['revenue'] += revenue
        cust_stats[cid]['count'] += 1
        
    sorted_cust = sorted(cust_stats.items(), key=lambda x: x[1]['revenue'], reverse=True)
    return sorted_cust[:5]

def daily_sales_trend(transactions):
    """
    Analyzes sales by date.
    """
    daily_stats = {}
    for t in transactions:
        date = t['Date']
        revenue = t['Quantity'] * t['UnitPrice']
        
        if date not in daily_stats:
            daily_stats[date] = {'revenue': 0, 'transactions': 0, 'customers': set()}
        
        daily_stats[date]['revenue'] += revenue
        daily_stats[date]['transactions'] += 1
        daily_stats[date]['customers'].add(t['CustomerID'])
        
    return daily_stats