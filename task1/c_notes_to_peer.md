## Order metrics notes
-----------

- This query will get us the metrics we need.
- The grain of the table is by day. This is a fact table that we can join any kind of information **at a day level** to.
- Order revenue is calculated like: `order_payments.payment_value` * `order_payments.payment_installments`
  - This might not be correct and if it isn't, we need to adjust the `order_payments` cte.
- Take note of the lateral join. This is a postgres (yes - mode's sql explorer is postgres btw) function that will create filtering/scoping _and_ aggregation in parallel at the time of joining during compiling.
