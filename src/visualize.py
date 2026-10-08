# creates and saves all the charts
# using matplotlib and seaborn

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

sns.set_theme(style="whitegrid", palette="muted")

CHART_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs", "charts")


def save_chart(fig, filename):
    os.makedirs(CHART_DIR, exist_ok=True)
    path = os.path.join(CHART_DIR, filename)
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"saved: {path}")


def plot_monthly_revenue(monthly_df):
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        monthly_df["Month Name"], monthly_df["Total_Revenue"],
        marker="o", linewidth=2, color="#2E86AB", markersize=6
    )
    ax.fill_between(monthly_df["Month Name"], monthly_df["Total_Revenue"], alpha=0.1, color="#2E86AB")

    ax.set_title("Monthly Revenue Trend", fontsize=13, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue (Rs.)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"Rs.{x:,.0f}"))
    fig.tight_layout()
    save_chart(fig, "01_monthly_revenue.png")


def plot_revenue_by_city(city_df):
    fig, ax = plt.subplots(figsize=(9, 5))

    colors = sns.color_palette("Blues_d", len(city_df))
    bars = ax.barh(city_df["City"], city_df["Total_Revenue"], color=colors)

    for bar in bars:
        ax.text(
            bar.get_width() + 500,
            bar.get_y() + bar.get_height() / 2,
            f'Rs.{bar.get_width():,.0f}',
            va="center", fontsize=9
        )

    ax.set_title("Total Revenue by City", fontsize=13, fontweight="bold")
    ax.set_xlabel("Revenue (Rs.)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"Rs.{x:,.0f}"))
    ax.invert_yaxis()
    fig.tight_layout()
    save_chart(fig, "02_revenue_by_city.png")


def plot_product_line_revenue(product_df):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    sns.barplot(
        data=product_df, y="Product line", x="Total_Revenue",
        hue="Product line", palette="viridis", legend=False, ax=axes[0]
    )
    axes[0].set_title("Revenue by Product Line", fontweight="bold")
    axes[0].set_xlabel("Revenue (Rs.)")
    axes[0].set_ylabel("")

    rating_df = product_df.sort_values("Avg_Rating", ascending=False)
    sns.barplot(
        data=rating_df, y="Product line", x="Avg_Rating",
        hue="Product line", palette="rocket", legend=False, ax=axes[1]
    )
    axes[1].set_title("Avg Rating by Product Line", fontweight="bold")
    axes[1].set_xlabel("Average Rating (out of 10)")
    axes[1].set_ylabel("")
    axes[1].set_xlim(0, 10)

    fig.suptitle("Product Line Performance", fontsize=13, fontweight="bold")
    fig.tight_layout()
    save_chart(fig, "03_product_line_performance.png")


def plot_payment_methods(payment_df):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].pie(
        payment_df["Count"],
        labels=payment_df["Payment"],
        autopct="%1.1f%%",
        startangle=140,
        colors=sns.color_palette("Set2", len(payment_df)),
        wedgeprops={"edgecolor": "white"}
    )
    axes[0].set_title("Payment Method Share", fontweight="bold")

    sns.barplot(
        data=payment_df, x="Payment", y="Avg_Transaction",
        hue="Payment", palette="Set2", legend=False, ax=axes[1]
    )
    axes[1].set_title("Avg Transaction by Payment Method", fontweight="bold")
    axes[1].set_xlabel("Payment Method")
    axes[1].set_ylabel("Avg Transaction (Rs.)")

    fig.suptitle("Payment Method Analysis", fontsize=13, fontweight="bold")
    fig.tight_layout()
    save_chart(fig, "04_payment_methods.png")


def plot_customer_type(customer_df):
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))

    metrics = [
        ("Total_Revenue", "Total Revenue (Rs.)", "coral"),
        ("Avg_Spend", "Avg Spend per Visit (Rs.)", "steelblue"),
        ("Avg_Rating", "Avg Rating", "mediumseagreen"),
    ]

    for ax, (col, label, color) in zip(axes, metrics):
        bars = ax.bar(customer_df["Customer type"], customer_df[col], color=color, width=0.5)
        for bar in bars:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() * 1.01,
                f"{bar.get_height():,.1f}",
                ha="center", fontsize=10
            )
        ax.set_title(label, fontweight="bold")

    fig.suptitle("Member vs Normal Customers", fontsize=13, fontweight="bold")
    fig.tight_layout()
    save_chart(fig, "05_customer_type_comparison.png")


def plot_city_product_heatmap(df):
    pivot = df.pivot_table(
        values="Total", index="City", columns="Product line", aggfunc="sum"
    ).fillna(0).round(0)

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.heatmap(
        pivot,
        annot=True, fmt=".0f",
        cmap="YlOrRd", linewidths=0.5,
        ax=ax
    )
    ax.set_title("Revenue Heatmap - City vs Product Line", fontsize=13, fontweight="bold")
    ax.set_xlabel("Product Line")
    ax.set_ylabel("City")
    fig.tight_layout()
    save_chart(fig, "06_city_product_heatmap.png")


def plot_peak_hours(hours_df):
    fig, ax = plt.subplots(figsize=(12, 5))

    hours_df = hours_df.sort_values("Hour")
    max_trans = hours_df["Transactions"].max()
    colors = ["#E63946" if t == max_trans else "#457B9D" for t in hours_df["Transactions"]]

    ax.bar(hours_df["Hour"], hours_df["Transactions"], color=colors, edgecolor="white")
    ax.set_title("Transactions by Hour of Day", fontsize=13, fontweight="bold")
    ax.set_xlabel("Hour (24h)")
    ax.set_ylabel("Number of Transactions")
    ax.set_xticks(hours_df["Hour"])

    fig.tight_layout()
    save_chart(fig, "07_peak_hours.png")


# TODO: maybe add boxplot by branch later
def plot_rating_distribution(df):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    axes[0].hist(df["Rating"], bins=18, color="#2E86AB", edgecolor="white")
    axes[0].axvline(df["Rating"].mean(), color="#E63946", linestyle="--", linewidth=1.5, label=f'Mean = {df["Rating"].mean():.2f}')
    axes[0].axvline(df["Rating"].median(), color="#2EC4B6", linestyle=":", linewidth=1.5, label=f'Median = {df["Rating"].median():.2f}')
    axes[0].set_title("Rating Distribution", fontweight="bold")
    axes[0].set_xlabel("Rating")
    axes[0].set_ylabel("Count")
    axes[0].legend()

    order = df.groupby("Product line")["Rating"].median().sort_values(ascending=False).index
    sns.boxplot(
        data=df, x="Rating", y="Product line",
        order=order, hue="Product line", palette="coolwarm", legend=False, ax=axes[1]
    )
    axes[1].set_title("Rating by Product Line", fontweight="bold")
    axes[1].set_xlabel("Rating")
    axes[1].set_ylabel("")

    fig.suptitle("Customer Rating Analysis", fontsize=13, fontweight="bold")
    fig.tight_layout()
    save_chart(fig, "08_rating_distribution.png")


def plot_gender_product(df):
    pivot = df.groupby(["Product line", "Gender"])["Total"].sum().unstack().fillna(0)

    fig, ax = plt.subplots(figsize=(11, 5))
    pivot.plot(kind="bar", ax=ax, color=["#F4A261", "#2A9D8F"], edgecolor="white", width=0.65)

    ax.set_title("Revenue by Product Line and Gender", fontsize=13, fontweight="bold")
    ax.set_xlabel("Product Line")
    ax.set_ylabel("Revenue (Rs.)")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=25, ha="right")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"Rs.{x:,.0f}"))
    ax.legend(title="Gender")

    fig.tight_layout()
    save_chart(fig, "09_gender_product_revenue.png")


def plot_correlation_matrix(df):
    cols = ["Unit price", "Quantity", "Tax 5%", "Total", "gross income", "Rating"]
    corr = df[cols].corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        corr,
        annot=True, fmt=".2f",
        cmap="coolwarm", center=0,
        square=True, linewidths=0.5,
        ax=ax
    )
    ax.set_title("Correlation Matrix", fontsize=13, fontweight="bold")
    fig.tight_layout()
    save_chart(fig, "10_correlation_matrix.png")
