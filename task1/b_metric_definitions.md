| Metric  | Definition  |
|---|---|
|order_purchase_date   | the date of when an order was captured within the olist_orders_dataset table  |
|total_orders   | count of orders placed (note, I checked that order_ids are unique so no need for distinct)  |
|total_customers_making_orders   | count distinct of each customer_id placing an order by day  |
|total_revenue   | payment_value * payment_installments by order by day  |
|avg_rev_per_order   | (sum(revenue)/count(orders))/day  |
|top_three_products   | first three products by their daily revenue in descending order  |
|total_revenue_pct   | daily total revenue / top three's revenue summed revenue  |


