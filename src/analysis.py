# all the analysis functions are in this file
# i tried to keep each function focused on one thing

import pandas as pd
import numpy as np
from data_loader import query_db


def monthly_revenue(df):
    monthly = df.groupby(["Month", "Month Name"]).agg(
        Total_Revenue    = ("Total", "sum"),
        Num_Transactions = ("Invoice ID", "count"),
        Avg_Order_Value  = ("Total", "mean")
    ).reset_index()

    monthly = monthly.sort_values("Month")
    monthly["Total_Revenue"] = monthly["Total_Revenue"].round(2)
    monthly["Avg_Order_Value"] = monthly["Avg_Order_Value"].round(2)
    return monthly


def quarterly_revenue(df):
    result = df.groupby("Quarter").agg(
        Total_Revenue = ("Total", "sum"),
        Transactions  = ("Invoice ID", "count")
    ).reset_index()

    result["Total_Revenue"] = result["Total_Revenue"].round(2)
    return result


def revenue_by_city(df):
    result = df.groupby("City").agg(
        Total_Revenue   = ("Total", "sum"),
        Avg_Order_Value = ("Total", "mean"),
        Transactions    = ("Invoice ID", "count")
    ).reset_index()

    result = result.sort_values("Total_Revenue", ascending=False)
    result["Total_Revenue"] = result["Total_Revenue"].round(2)
    result["Avg_Order_Value"] = result["Avg_Order_Value"].round(2)
    return result


def product_line_performance(df):
    result = df.groupby("Product line").agg(
        Total_Revenue  = ("Total", "sum"),
        Total_Quantity = ("Quantity", "sum"),
        Avg_Rating     = ("Rating", "mean"),
        Avg_Unit_Price = ("Unit price", "mean"),
        Transactions   = ("Invoice ID", "count")
    ).reset_index()

    result = result.sort_values("Total_Revenue", ascending=False)
    result["Total_Revenue"] = result["Total_Revenue"].round(2)
    result["Avg_Rating"] = result["Avg_Rating"].round(2)
    result["Avg_Unit_Price"] = result["Avg_Unit_Price"].round(2)
    return result


def top_product_lines_by_quantity(df, top_n=3):
    result = df.groupby("Product line")["Quantity"].sum()
    result = result.sort_values(ascending=False).head(top_n).reset_index()
    result.columns = ["Product line", "Total Units Sold"]
    return result


def customer_type_analysis(df):
    result = df.groupby("Customer type").agg(
        Total_Revenue = ("Total", "sum"),
        Avg_Spend     = ("Total", "mean"),
        Avg_Rating    = ("Rating", "mean"),
        Transactions  = ("Invoice ID", "count")
    ).reset_index()

    result["Total_Revenue"] = result["Total_Revenue"].round(2)
    result["Avg_Spend"] = result["Avg_Spend"].round(2)
    result["Avg_Rating"] = result["Avg_Rating"].round(2)
    return result


def gender_spending(df):
    result = df.groupby("Gender").agg(
        Total_Revenue = ("Total", "sum"),
        Avg_Spend     = ("Total", "mean"),
        Transactions  = ("Invoice ID", "count")
    ).reset_index()

    result["Total_Revenue"] = result["Total_Revenue"].round(2)
    result["Avg_Spend"] = result["Avg_Spend"].round(2)
    return result


def rfm_analysis(df):
    # RFM = Recency, Frequency, Monetary - i read about this and tried implementing it
    # doing it at city level since there are no individual customer IDs in the data

    snapshot_date = df["Date"].max() + pd.Timedelta(days=1)

    rfm = df.groupby("City").agg(
        Recency   = ("Date", lambda x: (snapshot_date - x.max()).days),
        Frequency = ("Invoice ID", "count"),
        Monetary  = ("Total", "sum")
    ).reset_index()

    # scoring 1-4, recency is flipped because lower days = more recent = better
    rfm["R_Score"] = pd.qcut(rfm["Recency"], q=4, labels=False, duplicates="drop") + 1
    rfm["R_Score"] = rfm["R_Score"].max() + 1 - rfm["R_Score"]
    rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), q=4, labels=False, duplicates="drop") + 1
    rfm["M_Score"] = pd.qcut(rfm["Monetary"].rank(method="first"),  q=4, labels=False, duplicates="drop") + 1

    rfm["RFM_Score"] = rfm["R_Score"] + rfm["F_Score"] + rfm["M_Score"]
    rfm["Monetary"]  = rfm["Monetary"].round(2)
    rfm = rfm.sort_values("RFM_Score", ascending=False)
    return rfm


def payment_method_breakdown(df):
    result = df.groupby("Payment").agg(
        Count           = ("Invoice ID", "count"),
        Total_Revenue   = ("Total", "sum"),
        Avg_Transaction = ("Total", "mean")
    ).reset_index()

    result = result.sort_values("Count", ascending=False)
    result["Total_Revenue"] = result["Total_Revenue"].round(2)
    result["Avg_Transaction"] = result["Avg_Transaction"].round(2)
    return result


def peak_hours(df):
    result = df.groupby("Hour").agg(
        Transactions = ("Invoice ID", "count"),
        Revenue      = ("Total", "sum")
    ).reset_index()

    result = result.sort_values("Transactions", ascending=False)
    result["Revenue"] = result["Revenue"].round(2)
    return result


def weekday_sales(df):
    result = df.groupby(["Weekday Num", "Weekday"]).agg(
        Transactions = ("Invoice ID", "count"),
        Revenue      = ("Total", "sum")
    ).reset_index()

    result = result.sort_values("Weekday Num")
    result["Revenue"] = result["Revenue"].round(2)
    return result


def sql_top_cities(db_path):
    sql = """
        SELECT City,
               ROUND(SUM(Total), 2) AS Total_Revenue,
               COUNT("Invoice ID")  AS Transactions,
               ROUND(AVG(Total), 2) AS Avg_Order_Value
        FROM sales
        GROUP BY City
        ORDER BY Total_Revenue DESC
    """
    return query_db(sql, db_path)


def sql_product_revenue_by_city(db_path):
    sql = """
        SELECT City,
               "Product line",
               ROUND(SUM(Total), 2) AS Revenue,
               COUNT("Invoice ID")  AS Transactions
        FROM sales
        GROUP BY City, "Product line"
        ORDER BY City, Revenue DESC
    """
    return query_db(sql, db_path)


def sql_monthly_gross_income(db_path):
    sql = """
        SELECT SUBSTR(Date, 1, 7)            AS Month,
               ROUND(SUM("gross income"), 2) AS Gross_Income,
               ROUND(SUM(Total), 2)          AS Revenue
        FROM sales
        GROUP BY Month
        ORDER BY Month
    """
    return query_db(sql, db_path)


def sql_avg_rating_by_product(db_path):
    sql = """
        SELECT "Product line",
               ROUND(AVG(Rating), 2) AS Avg_Rating,
               COUNT(*) AS Reviews
        FROM sales
        GROUP BY "Product line"
        ORDER BY Avg_Rating DESC
    """
    return query_db(sql, db_path)
