# generates the supermarket sales dataset and saves it as a csv
# i didnt use a real dataset so i wrote this script to create one
# seed is set so the data comes out the same every time you run it

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

NUM_RECORDS = 1500
START_DATE = datetime(2023, 1, 1)
END_DATE   = datetime(2023, 12, 31)

CITIES = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Pune", "Kolkata"]
BRANCHES = {
    "Mumbai":    "A",
    "Delhi":     "B",
    "Bangalore": "C",
    "Chennai":   "D",
    "Hyderabad": "E",
    "Pune":      "F",
    "Kolkata":   "G",
}

CUSTOMER_TYPES   = ["Member", "Normal"]
GENDERS          = ["Male", "Female"]
PAYMENT_METHODS  = ["Cash", "Credit card", "Ewallet"]

# price range per product line in INR
PRODUCT_LINES = {
    "Food and Beverages":      (10,  120),
    "Electronic accessories":  (50,  800),
    "Fashion accessories":     (30,  500),
    "Health and beauty":       (20,  300),
    "Home and lifestyle":      (40,  600),
    "Sports and travel":       (25,  700),
}


def random_date(start, end):
    delta          = end - start
    random_days    = random.randint(0, delta.days)
    random_seconds = random.randint(28800, 79200)   # shop open 8am–10pm
    return start + timedelta(days=random_days, seconds=random_seconds)


def generate_invoice_id(i):
    return f"INV-{str(i).zfill(4)}-{random.randint(100, 999)}"


rows = []
for i in range(1, NUM_RECORDS + 1):
    city         = random.choice(CITIES)
    branch       = BRANCHES[city]
    cust_type    = random.choice(CUSTOMER_TYPES)
    gender       = random.choice(GENDERS)
    product_line = random.choice(list(PRODUCT_LINES.keys()))

    unit_price = round(random.uniform(*PRODUCT_LINES[product_line]), 2)
    quantity   = random.randint(1, 10)

    tax_rate         = 0.05
    total_before_tax = round(unit_price * quantity, 2)
    tax              = round(total_before_tax * tax_rate, 4)
    total            = round(total_before_tax + tax, 2)

    dt       = random_date(START_DATE, END_DATE)
    date_str = dt.strftime("%Y-%m-%d")
    time_str = dt.strftime("%H:%M")

    payment = random.choice(PAYMENT_METHODS)

    # rating influenced by customer type
    base_rating = random.gauss(6.5, 1.5)
    if cust_type == "Member":
        base_rating += 0.3
    rating = round(min(10.0, max(1.0, base_rating)), 1)

    gross_income = tax
    gross_margin = round((gross_income / total) * 100, 9) if total > 0 else 0

    rows.append({
        "Invoice ID":               generate_invoice_id(i),
        "Branch":                   branch,
        "City":                     city,
        "Customer type":            cust_type,
        "Gender":                   gender,
        "Product line":             product_line,
        "Unit price":               unit_price,
        "Quantity":                 quantity,
        "Tax 5%":                   tax,
        "Total":                    total,
        "Date":                     date_str,
        "Time":                     time_str,
        "Payment":                  payment,
        "cogs":                     total_before_tax,
        "gross margin percentage":  gross_margin,
        "gross income":             gross_income,
        "Rating":                   rating,
    })

df = pd.DataFrame(rows)
df.to_csv("supermarket_sales.csv", index=False)
print(f"generated {len(df)} records -> supermarket_sales.csv")
print(df.head(3).to_string())
