# all the cleaning steps are here
# i kept this separate from main.py so the code doesnt get too long

import pandas as pd
import numpy as np


def clean(df):
    df = df.copy()

    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df["Time"] = pd.to_datetime(df["Time"], format="%H:%M").dt.time

    df["Month"] = df["Date"].dt.month
    df["Month Name"] = df["Date"].dt.strftime("%b")
    df["Weekday"] = df["Date"].dt.day_name()
    df["Weekday Num"] = df["Date"].dt.dayofweek
    df["Hour"] = pd.to_datetime(df["Time"].astype(str), format="%H:%M:%S").dt.hour
    df["Quarter"] = df["Date"].dt.quarter

    # strip whitespace from string columns - had issues with extra spaces earlier
    for col in df.select_dtypes(include="object").columns:
        try:
            df[col] = df[col].str.strip()
        except AttributeError:
            pass

    missing = df.isnull().sum().sum()
    if missing > 0:
        print(f"found {missing} missing values, dropping them")
        df.dropna(inplace=True)
    else:
        print("no missing values")

    dupes = df.duplicated().sum()
    if dupes > 0:
        print(f"dropping {dupes} duplicate rows")
        df.drop_duplicates(inplace=True)

    df["Revenue Bucket"] = pd.cut(
        df["Total"],
        bins=[0, 100, 300, 600, 1000, float("inf")],
        labels=["<100", "100-300", "300-600", "600-1000", "1000+"]
    )

    def get_time_of_day(hour):
        if 8 <= hour < 12:
            return "Morning"
        elif 12 <= hour < 17:
            return "Afternoon"
        elif 17 <= hour < 21:
            return "Evening"
        else:
            return "Night"

    df["Time of Day"] = df["Hour"].apply(get_time_of_day)

    df["Rating Category"] = pd.cut(
        df["Rating"],
        bins=[0, 4, 6, 8, 10],
        labels=["Poor", "Average", "Good", "Excellent"]
    )

    print(f"cleaned shape: {df.shape}")
    return df


def summary_stats(df):
    # calculating stats manually using numpy instead of just df.describe()
    cols = ["Unit price", "Quantity", "Tax 5%", "Total", "gross income", "Rating"]
    stats = []

    for col in cols:
        values = df[col].dropna().values
        stats.append({
            "Column":  col,
            "Count":   len(values),
            "Mean":    round(np.mean(values), 2),
            "Median":  round(np.median(values), 2),
            "Std Dev": round(np.std(values), 2),
            "Min":     round(np.min(values), 2),
            "Max":     round(np.max(values), 2),
        })

    return pd.DataFrame(stats)
