from utils.file_handler import read_sales_data, save_data_to_file, generate_sales_report
from utils.data_processor import parse_and_clean_data, validate_and_filter, calculate_sales_stats
from utils.api_handler import enrich_sales_data
import os

def main():
    """
    Main execution function for the Sales Analytics System.
    """
    print("==================================================")
    print("              SALES ANALYTICS SYSTEM              ")
    print("==================================================\n")

    input_file = 'data/sales_data.txt'
    enriched_file = 'data/enriched_sales_data.txt'
    report_file = 'output/sales_report.txt'

    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)

    try:
        # [1/10] Reading Data
        raw_lines = read_sales_data(input_file)
        if not raw_lines:
            print("CRITICAL ERROR: No data found. Exiting.")
            return

        # [2/10] Parsing Data
        cleaned_data = parse_and_clean_data(raw_lines)

        # [3/10] Filter Options Display
        print("\n[3/10] Filter Options Available:")
        print("Regions: North, South, East, West")
        print("Amount Range: ₹500 - ₹90,000")
        
        # User Interaction
        apply_filter = input("\nDo you want to filter data? (y/n): ").strip().lower()
        
        region_filter = None
        min_amt = None
        max_amt = None

        if apply_filter == 'y':
            r_input = input("Enter Region (Leave blank for none): ").strip()
            if r_input: region_filter = r_input
            
            try:
                min_input = input("Enter Min Amount (Leave blank for none): ").strip()
                if min_input: min_amt = float(min_input)
                
                max_input = input("Enter Max Amount (Leave blank for none): ").strip()
                if max_input: max_amt = float(max_input)
            except ValueError:
                print("Invalid number entered. Skipping amount filter.")

        # [4/10] Validating & Filtering
        valid_transactions, invalid_count, filter_stats = validate_and_filter(
            cleaned_data, region=region_filter, min_amount=min_amt, max_amount=max_amt
        )

        if not valid_transactions:
            print("No valid transactions found after filtering. Exiting.")
            return

        # [5/10] Analyzing Data (Quick check)
        calculate_sales_stats(valid_transactions)

        # [6/10] & [7/10] API Enrichment
        # We pass valid_transactions to the API handler
        enriched_data = enrich_sales_data(valid_transactions)

        # [8/10] Save Enriched Data
        save_data_to_file(enriched_data, enriched_file)

        # [9/10] Generate Report
        generate_sales_report(valid_transactions, enriched_data, report_file)
        
        print("\nSuccess! System finished execution.")

    except Exception as e:
        print(f"\nAN UNEXPECTED ERROR OCCURRED: {e}")

if __name__ == "__main__":
    main()