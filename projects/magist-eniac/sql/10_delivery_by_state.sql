-- F3.3: Average delivery days and on-time share per state, only states with at least 100 orders.
-- Author: Matías

SELECT
    g.state,
    COUNT(*) AS orders,
    ROUND(AVG(
        TIMESTAMPDIFF(
            DAY,
            o.order_purchase_timestamp,
            o.order_delivered_customer_date
        )
    ), 2) AS avg_delivery_days,

    ROUND(AVG(
        CASE
            WHEN o.order_delivered_customer_date <= o.order_estimated_delivery_date
            THEN 1
            ELSE 0
        END
    ) * 100, 2) AS on_time_percentage

FROM orders o

JOIN customers c
    ON o.customer_id = c.customer_id

LEFT JOIN geo g
    ON c.customer_zip_code_prefix = g.zip_code_prefix

WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_estimated_delivery_date IS NOT NULL

GROUP BY g.state

HAVING COUNT(*) >= 100

ORDER BY on_time_percentage DESC;
