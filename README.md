# Sales Analytics System

Student Name: Ameya Kale

Student ID: bitsom_ba_25071568

Email: drameyakale.sm@gmail.com

Date: 19-01-2026

## Overview
A Python-based data analytics platform that processes messy sales transaction files, validates data, performs statistical analysis, and enriches records using the DummyJSON API.

## Project Structure
```text
sales-analytics-system/
├── data/
│   ├── sales_data.txt           # Raw input data
│   └── enriched_sales_data.txt  # Output: Data enriched with API info
├── output/
│   └── sales_report.txt         # Final generated report
├── utils/
│   ├── file_handler.py          # File I/O and Report Generation
│   ├── data_processor.py        # Cleaning, Validation, and Analytics logic
│   └── api_handler.py           # API integration (DummyJSON)
├── main.py                      # Main execution script
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation

```
##Features

    Data Cleaning: Handles encoding issues, removes invalid records, and parses mixed formats.

    Validation: Filters transactions based on strict business rules (e.g., valid IDs, non-negative prices).

    Analytics: Calculates revenue, top products, regional performance, and daily trends.

    API Enrichment: Fetches product categories in real-time using the DummyJSON API.

    Reporting: Generates a comprehensive text report.

### Setup & Execution
1. Prerequisites

    Python 3.x

    Internet connection (for API access)

2. Installation

Install the required libraries:
Bash

pip install -r requirements.txt

3. Usage

Run the main script:
Bash

python main.py

Follow the on-screen prompts to filter data (optional).
generated Output

    Report: output/sales_report.txt


    Data: data/enriched_sales_data.txt


