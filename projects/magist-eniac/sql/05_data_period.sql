-- F2.1: First and last order date and the number of months in between.
-- Author: Julia

SELECT MIN(order_purchase_timestamp) AS min_date,
        MAX(order_purchase_timestamp) AS max_date,
        TIMESTAMPDIFF (MONTH, MIN(order_purchase_timestamp), MAX(order_purchase_timestamp)) AS datebase_in_month
FROM orders;
