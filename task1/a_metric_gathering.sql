/* 

NOTE: This should be run in app.mode.com's database sql editor

-- Task 1.1 - Build the thing

-- Attempting to match https://github.com/brooklyn-data/co/blob/main/sql_style_guide.md
*/

with daily_product_stats as (
    select
      orders.order_purchase_timestamp::date as order_purchase_date,
      products.product_category_name as product,
      sum(price)::numeric(8,2) as revenue,
      rank() over (
        partition by
          orders.order_purchase_timestamp::date
        order by
          sum(price) desc -- Postgres can handle aggregation as an order by in a window function :O
      ) as position_rank
    from brooklyndata.olist_order_items_dataset as order_items
    inner join brooklyndata.olist_products_dataset as products on order_items.product_id = products.product_id
    inner join brooklyndata.olist_orders_dataset as orders on order_items.order_id = orders.order_id
    group by 1,2
),

daily_top_three_products as (
  select
    order_purchase_date,
    string_agg(product, ', ') as top_three_products,
    sum(revenue) as product_revenue
  from daily_product_stats
  where position_rank <= 3
  group by 1
),

order_payments as (
  select
    order_id,
    (payment_value * payment_installments)::numeric(9,2) as assumed_revenue -- I am unclear as to what revenue so this is my assumption.
  from brooklyndata.olist_order_payments_dataset
),

order_aggregates as (
  select
    order_purchase_timestamp::date as order_purchase_date,
    count(orders.order_id) as total_orders,
    count(distinct orders.customer_id) as total_customers_making_orders, -- this is what I think we actually want
    sum(order_payments.assumed_revenue) as total_revenue,
    round(avg(order_payments.assumed_revenue),2) as avg_rev_per_order
  from brooklyndata.olist_orders_dataset as orders
  inner join order_payments on orders.order_id = order_payments.order_id
  inner join daily_top_three_products on daily_top_three_products.order_purchase_date = orders.order_purchase_timestamp::date
  group by 1
),

all_stats as (
    select
        to_char(aggregates.order_purchase_date, 'YYYY-MM-DD') as day,
        aggregates.total_orders,
        aggregates.total_customers_making_orders,
        aggregates.total_revenue,
        aggregates.avg_rev_per_order,
        top_products.top_three_products,
        round((aggregates.total_revenue / product_revenue),2) as total_revenue_pct
    from order_aggregates as aggregates
    inner join lateral ( -- this is ugly but about 80% faster than another cte
        select
            order_purchase_date,
            string_agg(
                coalesce(
                    -- pref english if the translation exists else primary language
                    translations.product_category_name_english,
                    stats.product
                    ),
                ', '
            ) as top_three_products,
            sum(revenue) as product_revenue
        from daily_product_stats as stats
        left join brooklyndata.product_category_name_translation as translations on stats.product = translations.product_category_name
        where
            position_rank <= 3 and
            aggregates.order_purchase_date = stats.order_purchase_date
        group by 1
    ) as top_products on true
    order by aggregates.order_purchase_date desc
)

select * from all_stats
order by day desc