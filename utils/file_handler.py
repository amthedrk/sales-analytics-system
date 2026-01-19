import os
from datetime import datetime
# Import analytics functions needed for the report
from .data_processor import (
    calculate_sales_stats, analyze_sales_by_region, 
    identify_top_products, identify_top_customers, daily_sales_trend
)

def read_sales_data(file_path):
    """
    Reads the sales data file with encoding handling.
    Returns a list of raw lines.
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return []

    encodings = ['utf-8', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                lines = f.readlines()
                print(f"[1/10] Reading sales data...\n✓ Successfully read {len(lines)} lines using {encoding}")
                return [line.strip() for line in lines if line.strip()]
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error reading file: {e}")
            return []
    
    print("Error: Could not read file with any supported encoding.")
    return []

def save_data_to_file(data, file_path):
    """
    Saves a list of dictionaries to a file (for the enriched data).
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for record in data:
                f.write(str(record) + "\n")
        print(f"[8/10] Saving enriched data...\n✓ Saved to: {file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report.
    """
    print("[9/10] Generating report...")
    
    try:
        # --- PRE-CALCULATE STATS ---
        stats = calculate_sales_stats(transactions)
        region_stats = analyze_sales_by_region(transactions)
        top_products = identify_top_products(transactions)
        top_customers = identify_top_customers(transactions)
        daily_stats = daily_sales_trend(transactions)
        
        # Calculate API stats
        enriched_count = sum(1 for t in enriched_transactions if t.get('Category') != "Unknown")
        enrichment_rate = (enriched_count / len(enriched_transactions)) * 100 if enriched_transactions else 0

        with open(output_file, 'w', encoding='utf-8') as f:
            
            # 1. HEADER
            f.write("============================================================\n")
            f.write("                   SALES ANALYTICS REPORT                   \n")
            f.write(f"           Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"           Records Processed: {len(transactions)}\n")
            f.write("============================================================\n\n")

            # 2. OVERALL SUMMARY
            f.write("OVERALL SUMMARY\n")
            f.write("------------------------------------------------------------\n")
            f.write(f"Total Revenue:      ₹{stats['total_revenue']:,.2f}\n")
            f.write(f"Total Transactions: {stats['total_transactions']}\n")
            f.write(f"Average Order Value: ₹{stats['avg_order_value']:,.2f}\n")
            f.write(f"Date Range:         {stats['date_range']}\n\n")

            # 3. REGION-WISE PERFORMANCE
            f.write("REGION-WISE PERFORMANCE\n")
            f.write("------------------------------------------------------------\n")
            f.write(f"{'Region':<15} {'Revenue':<15} {'% Total':<10} {'Count':<10}\n")
            f.write("-" * 55 + "\n")
            
            # Sort regions by revenue descending
            sorted_regions = sorted(region_stats.items(), key=lambda x: x[1]['revenue'], reverse=True)
            for region, data in sorted_regions:
                f.write(f"{region:<15} ₹{data['revenue']:<14,.0f} {data['percentage']:<9.1f}% {data['count']:<10}\n")
            f.write("\n")

            # 4. TOP 5 PRODUCTS
            f.write("TOP 5 PRODUCTS\n")
            f.write("------------------------------------------------------------\n")
            f.write(f"{'Rank':<6} {'Product Name':<25} {'Qty':<10} {'Revenue':<15}\n")
            f.write("-" * 60 + "\n")
            for i, (name, data) in enumerate(top_products, 1):
                f.write(f"{i:<6} {name[:24]:<25} {data['quantity']:<10} ₹{data['revenue']:<14,.0f}\n")
            f.write("\n")

            # 5. TOP 5 CUSTOMERS
            f.write("TOP 5 CUSTOMERS\n")
            f.write("------------------------------------------------------------\n")
            f.write(f"{'Rank':<6} {'Customer ID':<15} {'Total Spent':<15} {'Orders':<10}\n")
            f.write("-" * 50 + "\n")
            for i, (cid, data) in enumerate(top_customers, 1):
                f.write(f"{i:<6} {cid:<15} ₹{data['revenue']:<14,.0f} {data['count']:<10}\n")
            f.write("\n")
            
            # 6. DAILY SALES TREND (Show First 5 for brevity, or all sorted)
            f.write("DAILY SALES TREND (Recent 5 Days)\n")
            f.write("------------------------------------------------------------\n")
            f.write(f"{'Date':<15} {'Revenue':<15} {'Orders':<10} {'Unique Cust':<10}\n")
            f.write("-" * 55 + "\n")
            sorted_dates = sorted(daily_stats.items(), reverse=True)[:5]
            for date, data in sorted_dates:
                f.write(f"{date:<15} ₹{data['revenue']:<14,.0f} {data['transactions']:<10} {len(data['customers']):<10}\n")
            f.write("\n")

            # 7. PRODUCT PERFORMANCE ANALYSIS
            # Logic: Find best selling day
            best_day = max(daily_stats.items(), key=lambda x: x[1]['revenue'])
            f.write("PRODUCT PERFORMANCE ANALYSIS\n")
            f.write("------------------------------------------------------------\n")
            f.write(f"Best Selling Day:     {best_day[0]} (₹{best_day[1]['revenue']:,.0f})\n")
            f.write(f"Avg Txn Value (North): ₹{region_stats.get('North', {'revenue':0})['revenue'] / region_stats.get('North', {'count':1}):,.2f}\n")
            f.write("\n")

            # 8. API ENRICHMENT SUMMARY
            f.write("API ENRICHMENT SUMMARY\n")
            f.write("------------------------------------------------------------\n")
            f.write(f"Total Products Enriched: {enriched_count}\n")
            f.write(f"Success Rate:            {enrichment_rate:.1f}%\n")
            
        print(f"✓ Report saved to: {output_file}")
        
    except Exception as e:
        print(f"Error generating report: {e}")