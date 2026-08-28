# ============================================================
# PROJECT 4 - DATA VISUALIZATION
# E-COMMERCE SALES ANALYTICS DASHBOARD
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        font-size: 17px;
        color: #666;
        margin-bottom: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

DATA_PATH = "Dataset/Dataset for Data Analytics.csv"


@st.cache_data
def load_data():

    df = pd.read_csv(DATA_PATH)

    # Convert date
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )

    # Convert numeric columns
    numeric_columns = [
        "Quantity",
        "UnitPrice",
        "ItemsInCart",
        "TotalPrice"
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Create time columns
    if "Date" in df.columns:

        df["Year"] = df["Date"].dt.year

        df["Month"] = df["Date"].dt.month

        df["YearMonth"] = (
            df["Date"]
            .dt.to_period("M")
            .astype(str)
        )

    return df


# ============================================================
# LOAD DATASET
# ============================================================

try:

    df = load_data()

except FileNotFoundError:

    st.error(
        "Dataset not found. Check that the CSV file is inside "
        "the Dataset folder."
    )

    st.stop()

except Exception as e:

    st.error(f"Error loading dataset: {e}")

    st.stop()


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "OrderID",
    "CustomerID",
    "Date",
    "Product",
    "Quantity",
    "UnitPrice",
    "ItemsInCart",
    "TotalPrice",
    "PaymentMethod",
    "OrderStatus",
    "ReferralSource"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    st.error(
        "The following required columns are missing from the dataset:"
    )

    st.write(missing_columns)

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">'
    '📊 E-Commerce Sales Analytics Dashboard'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'Interactive analysis of sales, products, orders, payments '
    'and referral sources'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Filters")


# YEAR FILTER

years = sorted(
    df["Year"].dropna().unique()
)

selected_years = st.sidebar.multiselect(
    "Select Year",
    options=years,
    default=years
)


# PRODUCT FILTER

products = sorted(
    df["Product"].dropna().unique()
)

selected_products = st.sidebar.multiselect(
    "Select Product",
    options=products,
    default=products
)


# ORDER STATUS FILTER

statuses = sorted(
    df["OrderStatus"].dropna().unique()
)

selected_statuses = st.sidebar.multiselect(
    "Select Order Status",
    options=statuses,
    default=statuses
)


# PAYMENT METHOD FILTER

payment_methods = sorted(
    df["PaymentMethod"].dropna().unique()
)

selected_payment_methods = st.sidebar.multiselect(
    "Select Payment Method",
    options=payment_methods,
    default=payment_methods
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df[
    (df["Year"].isin(selected_years))
    &
    (df["Product"].isin(selected_products))
    &
    (df["OrderStatus"].isin(selected_statuses))
    &
    (df["PaymentMethod"].isin(selected_payment_methods))
].copy()


# ============================================================
# CHECK FILTERED DATA
# ============================================================

if filtered_df.empty:

    st.warning(
        "No data available for the selected filters."
    )

    st.stop()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_orders = filtered_df["OrderID"].nunique()

total_revenue = filtered_df["TotalPrice"].sum()

total_quantity = filtered_df["Quantity"].sum()

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)

total_customers = filtered_df["CustomerID"].nunique()

cancelled_orders = (
    filtered_df["OrderStatus"]
    .astype(str)
    .str.lower()
    .eq("cancelled")
    .sum()
)

returned_orders = (
    filtered_df["OrderStatus"]
    .astype(str)
    .str.lower()
    .eq("returned")
    .sum()
)

total_records = len(filtered_df)

cancellation_rate = (
    cancelled_orders / total_records * 100
    if total_records > 0
    else 0
)

return_rate = (
    returned_orders / total_records * 100
    if total_records > 0
    else 0
)


# ============================================================
# KPI SECTION
# ============================================================

st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4, col5, col6 = st.columns(6)


with col1:

    st.metric(
        "Total Orders",
        f"{total_orders:,}"
    )


with col2:

    st.metric(
        "Total Revenue",
        f"₹{total_revenue:,.0f}"
    )


with col3:

    st.metric(
        "Quantity Sold",
        f"{total_quantity:,}"
    )


with col4:

    st.metric(
        "Average Order Value",
        f"₹{average_order_value:,.0f}"
    )


with col5:

    st.metric(
        "Customers",
        f"{total_customers:,}"
    )


with col6:

    st.metric(
        "Cancellation Rate",
        f"{cancellation_rate:.2f}%"
    )


st.divider()


# ============================================================
# MONTHLY REVENUE TREND
# ============================================================

st.subheader("📈 Monthly Revenue Trend")

monthly_revenue = (
    filtered_df
    .groupby("YearMonth")["TotalPrice"]
    .sum()
    .reset_index()
    .sort_values("YearMonth")
)


fig, ax = plt.subplots(figsize=(14, 5))

ax.plot(
    monthly_revenue["YearMonth"],
    monthly_revenue["TotalPrice"],
    marker="o",
    linewidth=2
)

ax.set_title(
    "Monthly Revenue Trend",
    fontsize=16,
    fontweight="bold"
)

ax.set_xlabel("Month")

ax.set_ylabel("Revenue")

ax.tick_params(
    axis="x",
    rotation=45
)

ax.grid(
    True,
    alpha=0.3
)

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)


# ============================================================
# PRODUCT ANALYSIS
# ============================================================

st.subheader("🏆 Product Performance")

product_revenue = (
    filtered_df
    .groupby("Product")["TotalPrice"]
    .sum()
    .sort_values(ascending=True)
)

product_quantity = (
    filtered_df
    .groupby("Product")["Quantity"]
    .sum()
    .sort_values(ascending=True)
)


col1, col2 = st.columns(2)


# ============================================================
# REVENUE BY PRODUCT
# ============================================================

with col1:

    st.markdown("### Revenue by Product")

    fig, ax = plt.subplots(figsize=(8, 6))

    bars = ax.barh(
        product_revenue.index,
        product_revenue.values
    )

    ax.set_xlabel("Revenue")

    ax.set_ylabel("Product")

    ax.set_title(
        "Revenue Contribution by Product"
    )

    for bar in bars:

        value = bar.get_width()

        ax.text(
            value,
            bar.get_y() + bar.get_height() / 2,
            f" ₹{value:,.0f}",
            va="center",
            fontsize=8
        )

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


# ============================================================
# QUANTITY BY PRODUCT
# ============================================================

with col2:

    st.markdown("### Quantity Sold by Product")

    fig, ax = plt.subplots(figsize=(8, 6))

    bars = ax.barh(
        product_quantity.index,
        product_quantity.values
    )

    ax.set_xlabel("Quantity")

    ax.set_ylabel("Product")

    ax.set_title(
        "Quantity Sold by Product"
    )

    for bar in bars:

        value = bar.get_width()

        ax.text(
            value,
            bar.get_y() + bar.get_height() / 2,
            f" {value:,.0f}",
            va="center",
            fontsize=8
        )

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


# ============================================================
# PAYMENT & REFERRAL
# ============================================================

st.subheader("💳 Payment & Referral Analysis")

col1, col2 = st.columns(2)


# ============================================================
# PAYMENT METHOD REVENUE
# ============================================================

with col1:

    payment_revenue = (
        filtered_df
        .groupby("PaymentMethod")["TotalPrice"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    bars = ax.bar(
        payment_revenue.index,
        payment_revenue.values
    )

    ax.set_title(
        "Revenue by Payment Method"
    )

    ax.set_xlabel("Payment Method")

    ax.set_ylabel("Revenue")

    ax.tick_params(
        axis="x",
        rotation=20
    )

    for bar in bars:

        value = bar.get_height()

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value,
            f"₹{value:,.0f}",
            ha="center",
            va="bottom",
            fontsize=8
        )

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


# ============================================================
# REFERRAL SOURCE REVENUE
# ============================================================

with col2:

    referral_revenue = (
        filtered_df
        .groupby("ReferralSource")["TotalPrice"]
        .sum()
        .sort_values(ascending=True)
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    bars = ax.barh(
        referral_revenue.index,
        referral_revenue.values
    )

    ax.set_title(
        "Revenue by Referral Source"
    )

    ax.set_xlabel("Revenue")

    ax.set_ylabel("Referral Source")

    for bar in bars:

        value = bar.get_width()

        ax.text(
            value,
            bar.get_y() + bar.get_height() / 2,
            f" ₹{value:,.0f}",
            va="center",
            fontsize=8
        )

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


# ============================================================
# ORDER ANALYSIS
# ============================================================

st.subheader("📦 Order Analysis")

col1, col2 = st.columns(2)


# ============================================================
# ORDER STATUS
# ============================================================

with col1:

    status_counts = (
        filtered_df["OrderStatus"]
        .value_counts()
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    bars = ax.bar(
        status_counts.index,
        status_counts.values
    )

    ax.set_title(
        "Order Status Distribution"
    )

    ax.set_xlabel("Order Status")

    ax.set_ylabel("Number of Orders")

    for bar in bars:

        value = bar.get_height()

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value,
            f"{value:,}",
            ha="center",
            va="bottom"
        )

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


# ============================================================
# ORDER STATUS BY PRODUCT
# ============================================================

with col2:

    status_product = pd.crosstab(
        filtered_df["Product"],
        filtered_df["OrderStatus"]
    )

    fig, ax = plt.subplots(figsize=(9, 5))

    status_product.plot(
        kind="bar",
        stacked=True,
        ax=ax
    )

    ax.set_title(
        "Order Status by Product"
    )

    ax.set_xlabel("Product")

    ax.set_ylabel("Number of Orders")

    ax.tick_params(
        axis="x",
        rotation=30
    )

    ax.legend(
        title="Order Status",
        bbox_to_anchor=(1.02, 1),
        loc="upper left"
    )

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.divider()

st.subheader("💡 Key Business Insights")


# TOP REVENUE PRODUCT

top_product = product_revenue.idxmax()

top_product_revenue = product_revenue.max()


# TOP QUANTITY PRODUCT

top_quantity_product = product_quantity.idxmax()

top_quantity = product_quantity.max()


# TOP PAYMENT METHOD

top_payment = (
    filtered_df
    .groupby("PaymentMethod")["TotalPrice"]
    .sum()
    .idxmax()
)


# TOP REFERRAL SOURCE

top_referral = (
    filtered_df
    .groupby("ReferralSource")["TotalPrice"]
    .sum()
    .idxmax()
)


# TOP REVENUE MONTH

top_month = (
    monthly_revenue
    .loc[
        monthly_revenue["TotalPrice"].idxmax(),
        "YearMonth"
    ]
)

top_month_revenue = (
    monthly_revenue["TotalPrice"].max()
)


st.info(
    f"🏆 **Top Revenue Product:** {top_product} "
    f"generated ₹{top_product_revenue:,.0f}."
)

st.info(
    f"📦 **Top Selling Product:** {top_quantity_product} "
    f"with {top_quantity:,.0f} units sold."
)

st.info(
    f"💳 **Top Payment Method:** {top_payment} "
    f"generated the highest revenue."
)

st.info(
    f"📢 **Top Referral Source:** {top_referral} "
    f"generated the highest revenue."
)

st.info(
    f"📅 **Peak Revenue Month:** {top_month} "
    f"with ₹{top_month_revenue:,.0f} revenue."
)

st.info(
    f"↩️ **Return Rate:** {return_rate:.2f}% "
    f"| **Cancellation Rate:** {cancellation_rate:.2f}%."
)


# ============================================================
# PRODUCT SUMMARY
# ============================================================

st.divider()

st.subheader("📋 Product Performance Summary")

product_summary = (
    filtered_df
    .groupby("Product")
    .agg(
        Revenue=("TotalPrice", "sum"),
        Quantity=("Quantity", "sum"),
        Orders=("OrderID", "nunique")
    )
    .sort_values(
        "Revenue",
        ascending=False
    )
)

st.dataframe(
    product_summary,
    use_container_width=True
)


# ============================================================
# FILTERED DATASET
# ============================================================

with st.expander("📄 View Filtered Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Project 4 – Data Visualization | "
    "E-Commerce Sales Analytics"
)