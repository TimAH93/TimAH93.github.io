-- F3.1: Average days from purchase to delivery, overall and for tech items.
-- Author: Julia

SELECT ROUND(AVG(DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp)), 0) AS AVG_zeit_lieferung,
        ROUND(AVG(
        CASE
            WHEN pn.product_category_name_english IN ('Computers_accessories',
                                                    'telephony',
                                                    'electronics',
                                                    'audio',
                                                    'computers',
                                                    'tablets_printing_image')
            THEN DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp)
            END), 0) AS AVG_tech_zeit_liefer
FROM orders AS o
LEFT JOIN order_items AS oi
        ON o.order_id = oi.order_id
LEFT JOIN products AS p
        ON oi.product_id = p.product_id
LEFT JOIN product_category_name_translation AS pn
        ON p.product_category_name = pn.product_category_name;
