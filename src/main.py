# run this to execute the full pipeline
# generates data if needed, cleans it, runs analysis, saves charts and excel report

import os
import sys
import subprocess

sys.path.insert(0, os.path.dirname(__file__))

from data_loader import load_raw_csv, save_to_sqlite
from clean_data  import clean, summary_stats
from analysis    import (
    monthly_revenue, quarterly_revenue, revenue_by_city,
    product_line_performance, customer_type_analysis,
    gender_spending, rfm_analysis, payment_method_breakdown,
    peak_hours, weekday_sales,
    sql_top_cities, sql_product_revenue_by_city,
    sql_monthly_gross_income, sql_avg_rating_by_product,
)
from visualize import (
    plot_monthly_revenue, plot_revenue_by_city,
    plot_product_line_revenue, plot_payment_methods,
    plot_customer_type, plot_city_product_heatmap,
    plot_peak_hours, plot_rating_distribution,
    plot_gender_product, plot_correlation_matrix,
)
from export_report import export_to_excel


def main():
    print("Supermarket Sales Analysis")
    print("starting...\n")

    raw_csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "supermarket_sales.csv")
    if not os.path.exists(os.path.abspath(raw_csv_path)):
        print("CSV not found, generating dataset...")
        gen_script = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "generate_data.py")
        subprocess.run(
            [sys.executable, os.path.basename(gen_script)],
            cwd=os.path.dirname(os.path.abspath(gen_script)),
            check=True
        )
    else:
        print("CSV found, skipping generation")

    print("\nloading and cleaning data...")
    df_raw  = load_raw_csv()
    df      = clean(df_raw)
    db_path = save_to_sqlite(df)

    print("\nsummary stats:")
    stats = summary_stats(df)
    print(stats.to_string(index=False))

    print("\nrunning analysis...")

    monthly   = monthly_revenue(df)
    quarterly = quarterly_revenue(df)
    by_city   = revenue_by_city(df)
    products  = product_line_performance(df)
    customers = customer_type_analysis(df)
    gender    = gender_spending(df)
    rfm       = rfm_analysis(df)
    payments  = payment_method_breakdown(df)
    hours     = peak_hours(df)
    weekdays  = weekday_sales(df)

    # running the same things in SQL to cross check
    print("\nSQL results:")
    print("\ntop cities:")
    print(sql_top_cities(db_path).to_string(index=False))

    print("\navg rating by product:")
    print(sql_avg_rating_by_product(db_path).to_string(index=False))

    print("\nmonthly gross income:")
    print(sql_monthly_gross_income(db_path).to_string(index=False))

    total_revenue = df["Total"].sum()
    total_orders  = len(df)
    avg_order     = df["Total"].mean()
    best_month    = monthly.loc[monthly["Total_Revenue"].idxmax(), "Month Name"]
    top_city      = by_city.iloc[0]["City"]
    top_product   = products.iloc[0]["Product line"]

    print("\nkey numbers:")
    print(f"  total revenue  : Rs.{total_revenue:,.2f}")
    print(f"  total orders   : {total_orders}")
    print(f"  avg order value: Rs.{avg_order:.2f}")
    print(f"  best month     : {best_month}")
    print(f"  top city       : {top_city}")
    print(f"  top product    : {top_product}")

    print("\ngenerating charts...")
    plot_monthly_revenue(monthly)
    plot_revenue_by_city(by_city)
    plot_product_line_revenue(products)
    plot_payment_methods(payments)
    plot_customer_type(customers)
    plot_city_product_heatmap(df)
    plot_peak_hours(hours)
    plot_rating_distribution(df)
    plot_gender_product(df)
    plot_correlation_matrix(df)

    print("\nexporting to excel...")
    report_path = export_to_excel(
        summary_stats   = stats,
        monthly_revenue = monthly,
        city_revenue    = by_city,
        product_perf    = products,
        customer_analysis = customers,
        payment_breakdown = payments,
        rfm             = rfm,
        peak_hours      = hours,
    )

    print("\ndone!")
    print(f"charts saved in outputs/charts/")
    print(f"report saved at: {report_path}")


if __name__ == "__main__":
    main()
