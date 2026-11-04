# Sales-Analytics-Without-Pandas
# Tech Hub Kenya – Sales Analytics

## Project Overview

This project analyzes September 2026 sales data from a fictional Kenyan electronics retailer, Tech Hub Kenya. The goal is to clean sales records, calculate revenue, identify top-performing products and stores, and generate basic transaction statistics.

The analysis was completed primarily using Python's standard library, with Pandas used independently to verify the results.

## Objectives

- Read and explore sales data from a CSV file.
- Clean and validate numeric values, including prices and quantities.
- Identify invalid records and separate them from valid transactions.
- Calculate total revenue.
- Analyze revenue by product, store, and payment method.
- Identify the top five products by revenue.
- Identify high-value transactions of KES 50,000 and above.
- Calculate mean, median, minimum, and maximum transaction revenue.
- Verify the results using Pandas.

## Tools and Technologies

- Python
- CSV module
- Dictionaries, lists, sets, and functions
- Pandas

## Data Cleaning

The original dataset contained 50 sales records.

During cleaning:
- Missing and invalid values were identified.
- KES prefixes and comma separators were handled.
- Word-based numeric values were converted into numbers.
- Records with invalid prices or quantities were excluded from the analysis.

Cleaning results:

| Description | Records |
|---|---:|
| Original records | 50 |
| Valid records | 47 |
| Skipped records | 3 |

## Key Findings

- Total revenue: KES 1,317,210.00
- Valid transactions: 47
- Skipped transactions: 3
- Top-performing product: HP 15 Laptop
- Top product revenue: KES 389,994.00
- High-value transactions: 5

### Top 3 Products by Revenue

| Product | Revenue (KES) |
|---|---:|
| HP 15 Laptop | 389,994.00 |
| Hisense 43in Smart TV | 272,993.00 |
| Lenovo Tab M10 | 199,992.00 |

### Transaction Revenue Statistics

| Statistic | Amount (KES) |
|---|---:|
| Mean | 28,025.74 |
| Median | 10,998.00 |
| Minimum | 1,499.00 |
| Maximum | 259,996.00 |

## Approach

The project was completed in the following stages:

1. Data ingestion: Read the CSV file using Python's `csv` module.
2. Data exploration: Inspected the dataset structure, columns, and records.
3. Data cleaning: Created functions to validate and convert numeric values.
4. Revenue analysis: Used loops and dictionaries to aggregate revenue by product, store, and payment method.
5. Transaction analysis: Identified high-value sales and calculated descriptive statistics.
6. Verification: Used Pandas to independently check the calculated results.

## Pandas Verification

Pandas was used as a separate verification step to compare the cleaned data and calculated statistics against the results from the standard-library implementation.

The total revenue, mean, median, minimum, and maximum transaction revenue matched the Pandas results.

## What I Learned

Through this project, I practised:

- Working with CSV files using Python.
- Handling missing, invalid, and inconsistent data.
- Using dictionaries and sets for grouping and counting.
- Writing reusable functions for data analysis.
- Applying loops and list comprehensions.
- Calculating descriptive statistics without relying on Pandas.
- Using Pandas to verify results.

## Conclusion

This project strengthened my understanding of data cleaning, Python data structures, functions, and basic sales analysis. It also demonstrated how Python's standard library can be used to perform data analysis before introducing specialised libraries such as Pandas.
