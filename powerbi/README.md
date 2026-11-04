# Power BI report build guide

Run the Python pipeline first, then import `outputs/clean_sales.csv` into Power BI Desktop.

## Data model
Create a date table and relate its date column to the date-only portion of `sales[InvoiceDate]`.

```DAX
Calendar =
CALENDAR (
    MIN ( sales[InvoiceDate] ),
    MAX ( sales[InvoiceDate] )
)
```

## Measures
```DAX
Revenue GBP = SUM ( sales[Revenue] )
Orders = DISTINCTCOUNT ( sales[InvoiceNo] )
Units Sold = SUM ( sales[Quantity] )
Customers = DISTINCTCOUNT ( sales[CustomerID] )
Average Order Value = DIVIDE ( [Revenue GBP], [Orders] )
Revenue per Customer = DIVIDE ( [Revenue GBP], [Customers] )
```

## Suggested report pages
1. **Executive overview:** Revenue, orders and AOV cards; monthly revenue line chart; revenue by country bar chart.
2. **Product performance:** Top products by revenue and units; product and country slicers.
3. **Customer analysis:** Customer revenue distribution and RFM segment counts.

Add date, country and customer slicers. Reconcile Power BI totals against the generated Excel workbook before publishing. Save the resulting `.pbix` file in this folder from Power BI Desktop.
