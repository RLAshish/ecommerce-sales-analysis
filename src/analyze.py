from pathlib import Path

import pandas as pd
from ucimlrepo import fetch_ucirepo

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
DATA.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)


def main():
    dataset = fetch_ucirepo(id=352)
    df = dataset.data.original.copy()
    df.to_csv(DATA / "online_retail_raw.csv", index=False)
    df.columns = [str(column).strip().replace(" ", "") for column in df.columns]

    required = {
        "InvoiceNo", "StockCode", "Description", "Quantity",
        "InvoiceDate", "UnitPrice", "CustomerID", "Country",
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Unexpected dataset schema; missing columns: {sorted(missing)}")

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
    df["CustomerID"] = df["CustomerID"].astype("string")
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]

    sales = df.loc[
        df["InvoiceDate"].notna()
        & df["Quantity"].gt(0)
        & df["UnitPrice"].gt(0)
        & ~df["InvoiceNo"].astype(str).str.startswith("C")
    ].copy()

    if sales.empty:
        raise ValueError("No sales rows remain after applying the documented filters.")

    sales["OrderMonth"] = sales["InvoiceDate"].dt.to_period("M").astype(str)
    latest_date = sales["InvoiceDate"].max()

    kpis = pd.DataFrame([{
        "transactions": sales["InvoiceNo"].nunique(),
        "units_sold": int(sales["Quantity"].sum()),
        "revenue_gbp": round(sales["Revenue"].sum(), 2),
        "customers_with_id": sales["CustomerID"].nunique(),
        "average_order_value_gbp": round(
            sales.groupby("InvoiceNo")["Revenue"].sum().mean(), 2
        ),
        "first_transaction": sales["InvoiceDate"].min(),
        "last_transaction": latest_date,
    }])

    monthly = sales.groupby("OrderMonth", as_index=False).agg(
        revenue_gbp=("Revenue", "sum"),
        orders=("InvoiceNo", "nunique"),
        units=("Quantity", "sum"),
    )
    country = sales.groupby("Country", as_index=False).agg(
        revenue_gbp=("Revenue", "sum"),
        orders=("InvoiceNo", "nunique"),
    ).sort_values("revenue_gbp", ascending=False)
    products = sales.groupby(["StockCode", "Description"], as_index=False).agg(
        revenue_gbp=("Revenue", "sum"),
        units=("Quantity", "sum"),
    ).sort_values("revenue_gbp", ascending=False)

    customer_sales = sales.dropna(subset=["CustomerID"])
    customer = customer_sales.groupby("CustomerID").agg(
        recency_days=("InvoiceDate", lambda values: (latest_date - values.max()).days),
        frequency=("InvoiceNo", "nunique"),
        monetary=("Revenue", "sum"),
    ).reset_index()

    if len(customer) >= 4:
        customer["R_score"] = pd.qcut(
            customer["recency_days"].rank(method="first"),
            4, labels=[4, 3, 2, 1],
        ).astype(int)
        customer["F_score"] = pd.qcut(
            customer["frequency"].rank(method="first"),
            4, labels=[1, 2, 3, 4],
        ).astype(int)
        customer["M_score"] = pd.qcut(
            customer["monetary"].rank(method="first"),
            4, labels=[1, 2, 3, 4],
        ).astype(int)
        customer["RFM_score"] = customer[
            ["R_score", "F_score", "M_score"]
        ].astype(str).agg("".join, axis=1)

    sales.to_csv(OUT / "clean_sales.csv", index=False)
    with pd.ExcelWriter(OUT / "ecommerce_analysis.xlsx", engine="openpyxl") as writer:
        kpis.to_excel(writer, sheet_name="KPIs", index=False)
        monthly.to_excel(writer, sheet_name="Monthly Trends", index=False)
        country.to_excel(writer, sheet_name="Country", index=False)
        products.head(100).to_excel(writer, sheet_name="Top Products", index=False)
        customer.to_excel(writer, sheet_name="RFM Customers", index=False)

    print(f"Rows analysed: {len(sales):,}")
    print(kpis.to_string(index=False))
    print(f"Outputs saved to: {OUT}")


if __name__ == "__main__":
    main()
