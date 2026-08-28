# =============================================================================
# PROJECT 4 - DATA VISUALIZATION
# E-COMMERCE SALES DATA ANALYTICS
# =============================================================================
#
# Goal:
# Convert raw e-commerce data into clear business insights using
# appropriate and decision-oriented visualizations.
#
# =============================================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# =============================================================================
# 1. CONFIGURATION
# =============================================================================

DATA_PATH = "Dataset/Dataset for Data Analytics.csv"

OUTPUT_DIR = "output"
CHART_DIR = os.path.join(OUTPUT_DIR, "charts")
INSIGHT_DIR = os.path.join(OUTPUT_DIR, "insights")

os.makedirs(CHART_DIR, exist_ok=True)
os.makedirs(INSIGHT_DIR, exist_ok=True)

sns.set_theme(style="whitegrid")


# =============================================================================
# 2. LOAD DATA
# =============================================================================

print("\n" + "=" * 80)
print("PROJECT 4 - DATA VISUALIZATION")
print("=" * 80)

print("\n[1] Loading dataset...")

df = pd.read_csv(DATA_PATH)

print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

print("\nColumns:")
print(df.columns.tolist())


# =============================================================================
# 3. DATA CLEANING
# =============================================================================

print("\n[2] Data Cleaning...")

# Convert date column
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Convert numerical columns
numeric_columns = [
    "Quantity",
    "UnitPrice",
    "ItemsInCart",
    "TotalPrice"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Remove duplicate records
duplicate_count = df.duplicated().sum()
df = df.drop_duplicates()

# Remove rows with critical missing values
critical_columns = [
    "Date",
    "Product",
    "Quantity",
    "UnitPrice",
    "OrderStatus",
    "TotalPrice"
]

missing_before = df[critical_columns].isnull().sum()

df = df.dropna(subset=critical_columns)

print(f"Duplicates removed : {duplicate_count}")
print(f"Rows after cleaning: {len(df)}")

print("\nMissing values:")
print(df.isnull().sum())


# =============================================================================
# 4. CREATE DERIVED VARIABLES
# =============================================================================

print("\n[3] Creating analytical variables...")

df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["MonthName"] = df["Date"].dt.strftime("%b")
df["YearMonth"] = df["Date"].dt.to_period("M").astype(str)

# Revenue
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# Average order value
average_order_value = df["TotalPrice"].mean()

print("Derived variables created successfully.")


# =============================================================================
# 5. KPI CALCULATIONS
# =============================================================================

print("\n" + "=" * 80)
print("KEY PERFORMANCE INDICATORS")
print("=" * 80)

total_orders = df["OrderID"].nunique()
total_revenue = df["TotalPrice"].sum()
total_quantity = df["Quantity"].sum()
average_order_value = df["TotalPrice"].mean()
average_unit_price = df["UnitPrice"].mean()

cancelled_orders = (df["OrderStatus"] == "Cancelled").sum()
returned_orders = (df["OrderStatus"] == "Returned").sum()

cancelled_rate = (cancelled_orders / total_orders) * 100
returned_rate = (returned_orders / total_orders) * 100

print(f"\nTotal Orders          : {total_orders:,}")
print(f"Total Revenue         : ₹{total_revenue:,.2f}")
print(f"Total Quantity Sold   : {total_quantity:,}")
print(f"Average Order Value   : ₹{average_order_value:,.2f}")
print(f"Average Unit Price    : ₹{average_unit_price:,.2f}")
print(f"Cancelled Orders      : {cancelled_orders:,}")
print(f"Cancelled Rate        : {cancelled_rate:.2f}%")
print(f"Returned Orders       : {returned_orders:,}")
print(f"Returned Rate         : {returned_rate:.2f}%")


# =============================================================================
# 6. PRODUCT PERFORMANCE
# =============================================================================

product_summary = (
    df.groupby("Product")
      .agg(
          Orders=("OrderID", "nunique"),
          Quantity=("Quantity", "sum"),
          Revenue=("TotalPrice", "sum"),
          AveragePrice=("UnitPrice", "mean")
      )
      .sort_values("Revenue", ascending=False)
)

print("\n" + "=" * 80)
print("PRODUCT PERFORMANCE")
print("=" * 80)

print(product_summary)


# =============================================================================
# CHART 1 - REVENUE BY PRODUCT
# =============================================================================

plt.figure(figsize=(11, 6))

plot_data = product_summary.sort_values("Revenue", ascending=True)

bars = plt.barh(
    plot_data.index,
    plot_data["Revenue"]
)

plt.title("Revenue Performance by Product", fontsize=16, fontweight="bold")
plt.xlabel("Revenue")
plt.ylabel("Product")

for bar in bars:
    value = bar.get_width()
    plt.text(
        value,
        bar.get_y() + bar.get_height() / 2,
        f" ₹{value:,.0f}",
        va="center",
        fontsize=9
    )

plt.tight_layout()

plt.savefig(
    os.path.join(CHART_DIR, "01_revenue_by_product.png"),
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# =============================================================================
# CHART 2 - QUANTITY SOLD BY PRODUCT
# =============================================================================

quantity_summary = (
    df.groupby("Product")["Quantity"]
      .sum()
      .sort_values(ascending=True)
)

plt.figure(figsize=(11, 6))

bars = plt.barh(
    quantity_summary.index,
    quantity_summary.values
)

plt.title(
    "Quantity Sold by Product",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Quantity Sold")
plt.ylabel("Product")

for bar in bars:
    value = bar.get_width()
    plt.text(
        value,
        bar.get_y() + bar.get_height() / 2,
        f" {value:,.0f}",
        va="center"
    )

plt.tight_layout()

plt.savefig(
    os.path.join(CHART_DIR, "02_quantity_by_product.png"),
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# =============================================================================
# 7. MONTHLY REVENUE TREND
# =============================================================================

monthly_revenue = (
    df.groupby("YearMonth")["TotalPrice"]
      .sum()
      .reset_index()
)

plt.figure(figsize=(13, 6))

plt.plot(
    monthly_revenue["YearMonth"],
    monthly_revenue["TotalPrice"],
    marker="o",
    linewidth=2
)

plt.title(
    "Monthly Revenue Trend",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Month")
plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    os.path.join(CHART_DIR, "03_monthly_revenue_trend.png"),
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# =============================================================================
# 8. YEARLY REVENUE
# =============================================================================

yearly_revenue = (
    df.groupby("Year")["TotalPrice"]
      .sum()
      .reset_index()
)

print("\nYearly Revenue:")
print(yearly_revenue)


plt.figure(figsize=(9, 5))

bars = plt.bar(
    yearly_revenue["Year"].astype(str),
    yearly_revenue["TotalPrice"]
)

plt.title(
    "Yearly Revenue Performance",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Year")
plt.ylabel("Revenue")

for bar in bars:
    value = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value,
        f"₹{value:,.0f}",
        ha="center",
        va="bottom",
        fontsize=9
    )

plt.tight_layout()

plt.savefig(
    os.path.join(CHART_DIR, "04_yearly_revenue.png"),
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# =============================================================================
# 9. ORDER STATUS ANALYSIS
# =============================================================================

status_summary = (
    df["OrderStatus"]
    .value_counts()
)

print("\nOrder Status:")
print(status_summary)


plt.figure(figsize=(9, 6))

bars = plt.bar(
    status_summary.index,
    status_summary.values
)

plt.title(
    "Order Status Distribution",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Order Status")
plt.ylabel("Number of Orders")

for bar in bars:
    value = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value,
        f"{value:,}",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

plt.savefig(
    os.path.join(CHART_DIR, "05_order_status.png"),
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# =============================================================================
# 10. PAYMENT METHOD ANALYSIS
# =============================================================================

payment_summary = (
    df.groupby("PaymentMethod")
      .agg(
          Orders=("OrderID", "nunique"),
          Revenue=("TotalPrice", "sum")
      )
      .sort_values("Revenue", ascending=False)
)

print("\nPayment Method Performance:")
print(payment_summary)


plt.figure(figsize=(10, 6))

bars = plt.bar(
    payment_summary.index,
    payment_summary["Revenue"]
)

plt.title(
    "Revenue by Payment Method",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Payment Method")
plt.ylabel("Revenue")

plt.xticks(rotation=20)

for bar in bars:
    value = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value,
        f"₹{value:,.0f}",
        ha="center",
        va="bottom",
        fontsize=9
    )

plt.tight_layout()

plt.savefig(
    os.path.join(CHART_DIR, "06_payment_method_revenue.png"),
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# =============================================================================
# 11. REFERRAL SOURCE ANALYSIS
# =============================================================================

referral_summary = (
    df.groupby("ReferralSource")
      .agg(
          Orders=("OrderID", "nunique"),
          Revenue=("TotalPrice", "sum")
      )
      .sort_values("Revenue", ascending=False)
)

print("\nReferral Source Performance:")
print(referral_summary)


plt.figure(figsize=(10, 6))

plot_data = referral_summary.sort_values("Revenue", ascending=True)

bars = plt.barh(
    plot_data.index,
    plot_data["Revenue"]
)

plt.title(
    "Revenue by Referral Source",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Revenue")
plt.ylabel("Referral Source")

for bar in bars:
    value = bar.get_width()

    plt.text(
        value,
        bar.get_y() + bar.get_height() / 2,
        f" ₹{value:,.0f}",
        va="center",
        fontsize=9
    )

plt.tight_layout()

plt.savefig(
    os.path.join(CHART_DIR, "07_referral_source_revenue.png"),
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# =============================================================================
# 12. PRODUCT VS UNIT PRICE RELATIONSHIP
# =============================================================================

product_relationship = (
    df.groupby("Product")
      .agg(
          AveragePrice=("UnitPrice", "mean"),
          Revenue=("TotalPrice", "sum"),
          Quantity=("Quantity", "sum")
      )
      .reset_index()
)

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=product_relationship,
    x="AveragePrice",
    y="Revenue",
    size="Quantity",
    sizes=(100, 800)
)

plt.title(
    "Average Product Price vs Revenue",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Average Unit Price")
plt.ylabel("Revenue")

plt.tight_layout()

plt.savefig(
    os.path.join(CHART_DIR, "08_price_vs_revenue.png"),
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# =============================================================================
# 13. MONTHLY ORDER VOLUME
# =============================================================================

monthly_orders = (
    df.groupby("YearMonth")["OrderID"]
      .nunique()
      .reset_index()
)

plt.figure(figsize=(13, 6))

plt.plot(
    monthly_orders["YearMonth"],
    monthly_orders["OrderID"],
    marker="o",
    linewidth=2
)

plt.title(
    "Monthly Order Volume Trend",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Month")
plt.ylabel("Number of Orders")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    os.path.join(CHART_DIR, "09_monthly_order_volume.png"),
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# =============================================================================
# 14. ORDER STATUS BY PRODUCT
# =============================================================================

status_product = pd.crosstab(
    df["Product"],
    df["OrderStatus"]
)

print("\nOrder Status by Product:")
print(status_product)


plt.figure(figsize=(12, 7))

status_product.plot(
    kind="bar",
    stacked=True,
    figsize=(12, 7)
)

plt.title(
    "Order Status Composition by Product",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Product")
plt.ylabel("Number of Orders")

plt.xticks(rotation=30)

plt.legend(
    title="Order Status",
    bbox_to_anchor=(1.02, 1),
    loc="upper left"
)

plt.tight_layout()

plt.savefig(
    os.path.join(CHART_DIR, "10_product_order_status.png"),
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# =============================================================================
# 15. TOP PRODUCT
# =============================================================================

top_product = product_summary["Revenue"].idxmax()
top_product_revenue = product_summary.loc[top_product, "Revenue"]

top_quantity_product = product_summary["Quantity"].idxmax()
top_quantity = product_summary.loc[top_quantity_product, "Quantity"]


# =============================================================================
# 16. TOP REFERRAL SOURCE
# =============================================================================

top_referral = referral_summary["Revenue"].idxmax()
top_referral_revenue = referral_summary.loc[top_referral, "Revenue"]


# =============================================================================
# 17. INSIGHT GENERATION
# =============================================================================

insights = []

insights.append(
    f"1. Total revenue generated is ₹{total_revenue:,.2f} "
    f"from {total_orders:,} orders."
)

insights.append(
    f"2. {top_product} is the highest-revenue product with "
    f"₹{top_product_revenue:,.2f} revenue."
)

insights.append(
    f"3. {top_quantity_product} has the highest quantity sold "
    f"with {top_quantity:,} units."
)

insights.append(
    f"4. The leading referral source by revenue is "
    f"{top_referral}, generating ₹{top_referral_revenue:,.2f}."
)

insights.append(
    f"5. Cancelled orders represent {cancelled_rate:.2f}% "
    f"of total orders."
)

insights.append(
    f"6. Returned orders represent {returned_rate:.2f}% "
    f"of total orders."
)


# =============================================================================
# 18. SAVE INSIGHTS
# =============================================================================

insight_file = os.path.join(
    INSIGHT_DIR,
    "business_insights.txt"
)

with open(insight_file, "w", encoding="utf-8") as file:

    file.write("=" * 80 + "\n")
    file.write("PROJECT 4 - BUSINESS INSIGHTS\n")
    file.write("=" * 80 + "\n\n")

    for insight in insights:
        file.write(insight + "\n")


# =============================================================================
# 19. SAVE SUMMARY TABLES
# =============================================================================

product_summary.to_csv(
    os.path.join(OUTPUT_DIR, "product_summary.csv")
)

payment_summary.to_csv(
    os.path.join(OUTPUT_DIR, "payment_summary.csv")
)

referral_summary.to_csv(
    os.path.join(OUTPUT_DIR, "referral_summary.csv")
)

yearly_revenue.to_csv(
    os.path.join(OUTPUT_DIR, "yearly_revenue.csv"),
    index=False
)


# =============================================================================
# 20. FINAL OUTPUT
# =============================================================================

print("\n" + "=" * 80)
print("KEY BUSINESS INSIGHTS")
print("=" * 80)

for insight in insights:
    print(insight)

print("\n" + "=" * 80)
print("PROJECT COMPLETED")
print("=" * 80)

print(f"\nCharts saved in : {CHART_DIR}")
print(f"Insights saved in: {INSIGHT_DIR}")
print(f"Summary tables saved in: {OUTPUT_DIR}")