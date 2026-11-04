
import csv
import pandas as pd
from pprint import pprint


# 1. READ SALES DATA
def read_sales(path):
    sales = []
    with open(path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            sales.append(row)

    return sales


# 2. PARSE NUMERIC VALUES
def parse_number(value):
    if value is None:
        return None

    cleaned = str(value).strip().lower()

    if isinstance(value, (int, float)):
        return value

    if not cleaned:
        return None

    if cleaned.upper() in {'NA', 'N/A', 'NULL', 'NONE', '-'}:
        return None

    # Catch word numbers
    word_to_num = {
        'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
        'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
    }

    if cleaned in word_to_num:
        return float(word_to_num[cleaned])

    # Catch unsupported commas
    cleaned = cleaned.upper().replace("KES", "").strip()

    if "." in cleaned:
        main_part, decimal_part = cleaned.split(".", 1)
    else:
        main_part, decimal_part = cleaned, ""

    # Check commas only on the main integer part
    if "," in main_part:
        parts = main_part.split(",")

        if not (1 <= len(parts[0]) <= 3 and parts[0].isdigit()):
            return None

        if not all(len(part) == 3 and part.isdigit() for part in parts[1:]):
            return None

        main_part = "".join(parts)

    # Recombine them safely for float conversion
    cleaned = f"{main_part}.{decimal_part}" if decimal_part else main_part

    try:
        return float(cleaned)

    except ValueError:
        return None


# 3. CONVERT AND CLEAN ROWS
def convert_rows(rows):
    valid_rows = []
    skipped_rows = []

    for row in rows:
        cleaned_row = row.copy()

        parsed_price = parse_number(cleaned_row.get("unit_price_kes"))
        parsed_quantity = parse_number(cleaned_row.get("quantity"))

        reasons = []

        if parsed_price is None:
            reasons.append("Invalid Price")

        if parsed_quantity is None:
            reasons.append("Invalid Quantity")

        if reasons:
            skipped_rows.append({
                "row": cleaned_row,
                "reason": reasons
            })
        else:
            cleaned_row["unit_price_kes"] = parsed_price
            cleaned_row["quantity"] = parsed_quantity
            valid_rows.append(cleaned_row)

    return valid_rows, skipped_rows


# 4. CALCULATE TOTAL REVENUE
def total_revenue(sales):
    revenue_generated = 0

    for sale in sales:
        revenue = sale["unit_price_kes"] * sale["quantity"]
        revenue_generated += revenue

    return revenue_generated


# 5. GROUP REVENUE BY FIELD
def revenue_by(rows, field):
    revenue_totals = {}

    for sale in rows:
        category = sale[field]
        amount = sale["unit_price_kes"] * sale["quantity"]

        if category in revenue_totals:
            revenue_totals[category] += amount
        else:
            revenue_totals[category] = amount

    return revenue_totals


# 6. SORT REVENUE
def sort_revenue(sorting_revenue):
    sorted_revenue = sorted(
        sorting_revenue.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return sorted_revenue


# 7. GET TOP N CATEGORIES
def top_n(category_revenue, n):
    sorted_category_revenue = sorted(
        category_revenue.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return sorted_category_revenue[:n]


# 8. FILTER HIGH-VALUE SALES
def high_value(rows, threshold):
    return [
        sale for sale in rows
        if sale["unit_price_kes"] * sale["quantity"] >= threshold
    ]


# 9. CALCULATE MEAN
def mean(rows):
    if not rows:
        raise ValueError("Cannot calculate mean of an empty list")

    total = 0

    for sale in rows:
        transaction = sale["unit_price_kes"] * sale["quantity"]
        total += transaction

    return total / len(rows)


# 10. CALCULATE MINIMUM AND MAXIMUM
def minimum_maximum(rows):
    if not rows:
        raise ValueError("Cannot calculate minimum and maximum of an empty list")

    minimum = rows[0]["unit_price_kes"] * rows[0]["quantity"]
    maximum = rows[0]["unit_price_kes"] * rows[0]["quantity"]

    for sale in rows:
        transaction = sale["unit_price_kes"] * sale["quantity"]

        if transaction < minimum:
            minimum = transaction

        if transaction > maximum:
            maximum = transaction

    return minimum, maximum


# 11. CALCULATE MEDIAN
def median(rows):
    if not rows:
        raise ValueError("Cannot calculate median of an empty list")

    values = sorted([
        sale["unit_price_kes"] * sale["quantity"]
        for sale in rows
    ])

    count = len(values)
    middle = count // 2

    if count % 2 == 1:
        return values[middle]
    else:
        return (values[middle - 1] + values[middle]) / 2


# 12. PANDAS VERIFICATION
def verify_results(file_path):
    df = pd.read_csv(file_path)

    word_to_num = {
        "zero": 0, "one": 1, "two": 2, "three": 3,
        "four": 4, "five": 5, "six": 6, "seven": 7,
        "eight": 8, "nine": 9, "ten": 10
    }

    df["unit_price_kes"] = pd.to_numeric(
        df["unit_price_kes"].astype(str)
        .str.replace("KES", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip(),
        errors="coerce"
    )

    quantity_clean = df["quantity"].astype(str).str.strip().str.lower()

    df["quantity"] = pd.to_numeric(
        quantity_clean.replace(word_to_num),
        errors="coerce"
    )

    valid_df = df.dropna(
        subset=["unit_price_kes", "quantity"]
    ).copy()

    skipped_df = df[
        df[["unit_price_kes", "quantity"]].isna().any(axis=1)
    ]

    valid_df["revenue"] = (
        valid_df["unit_price_kes"] * valid_df["quantity"]
    )

    print("\nPANDAS VERIFICATION")
    print("Original records:", len(df))
    print("Valid records:", len(valid_df))
    print("Skipped records:", len(skipped_df))
    print("Total Revenue:", valid_df["revenue"].sum())
    print("Mean Revenue:", valid_df["revenue"].mean())
    print("Median Revenue:", valid_df["revenue"].median())
    print("Minimum Revenue:", valid_df["revenue"].min())
    print("Maximum Revenue:", valid_df["revenue"].max())

    return valid_df, skipped_df


# 13. MAIN FUNCTION
def main():

    file_path = r"C:\Users\Administrator\Downloads\electronics_sales.csv"

    # Read data
    sales = read_sales(file_path)

    print("DATA EXPLORATION")
    print("----------------")
    print("Data type:", type(sales).__name__)
    print("Column names:", sales[0].keys())

    # Clean data
    valid_rows, skipped_rows = convert_rows(sales)

    print("\nDATA CLEANING")
    print("-------------")
    print("Original records:", len(sales))
    print("Valid records:", len(valid_rows))
    print("Skipped records:", len(skipped_rows))

    # Total revenue
    print("\nTOTAL REVENUE")
    print("-------------")
    print("Total revenue:", total_revenue(valid_rows))

    # Revenue grouping
    product_revenue = revenue_by(valid_rows, "product")
    store_revenue = revenue_by(valid_rows, "store")
    payment_revenue = revenue_by(valid_rows, "payment_method")

    sorted_store_revenue = sort_revenue(store_revenue)
    sorted_payment_revenue = sort_revenue(payment_revenue)
    sorted_product_revenue = sort_revenue(product_revenue)

    print("\nREVENUE BY PRODUCT")
    print(sorted_product_revenue)

    print("\nREVENUE BY STORE")
    print(sorted_store_revenue)

    print("\nREVENUE BY PAYMENT METHOD")
    print(sorted_payment_revenue)

    # Top 5 products
    top_3_product = top_n(product_revenue, 3)

    print("\nTOP 5 PRODUCTS")
    print(top_5_product)

    # High-value sales
    high_value_sales = high_value(valid_rows, 50000)

    stores = [sale["store"] for sale in high_value_sales]
    unique_stores = set(stores)

    store_count = {
        store: stores.count(store)
        for store in unique_stores
    }

    print("\nHIGH-VALUE SALES")
    print("----------------")
    print("High-value sales:", len(high_value_sales))
    print("High-value sales per store:", store_count)

    # Statistical calculations
    average_revenue = mean(valid_rows)
    minimum, maximum = minimum_maximum(valid_rows)
    median_revenue = median(valid_rows)

    print("\nTRANSACTION STATISTICS")
    print("---------------------")
    print(f"Mean: KES {average_revenue:,.2f}")
    print(f"Median: KES {median_revenue:,.2f}")
    print(f"Minimum: KES {minimum:,.2f}")
    print(f"Maximum: KES {maximum:,.2f}")

    # Pandas verification
    verified_valid, verified_skipped = verify_results(file_path)


# RUN MAIN FUNCTION
if __name__ == "__main__":
    main()
