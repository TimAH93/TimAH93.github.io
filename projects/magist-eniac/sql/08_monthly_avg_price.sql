-- F2.4: Average item price per month, overall and for tech items.
-- Author: Julia

SELECT YEAR(o.order_purchase_timestamp) AS Year,
        MONTH(o.order_purchase_timestamp) AS Month,
        ROUND(AVG(oi.price), 2) AS AVG_verdint,
        ROUND(AVG(CASE
            WHEN pn.product_category_name_english IN ('Computers_accessories',
                                                    'telephony',
                                                    'electronics',
                                                    'audio',
                                                    'computers',
                                                    'tablets_printing_image')
            THEN oi.price
            END), 2) AS AVG_tech_verdienstsumme
FROM orders AS o
LEFT JOIN order_items AS oi
        ON o.order_id = oi.order_id
LEFT JOIN products AS p
        ON oi.product_id = p.product_id
LEFT JOIN product_category_name_translation AS pn
        ON p.product_category_name = pn.product_category_name
GROUP BY YEAR(order_purchase_timestamp),
        MONTH(order_purchase_timestamp)
ORDER BY Year,
        Month;
