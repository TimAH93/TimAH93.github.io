-- F2.2: All sellers, tech sellers (at least one item in a tech category) and their share.
-- Author: Julia

SELECT COUNT(DISTINCT(oi.seller_id)) AS anzahl_verkäufer,
        COUNT(DISTINCT CASE
            WHEN pn.product_category_name_english IN ('Computers_accessories',
                                                    'telephony',
                                                    'electronics',
                                                    'audio',
                                                    'computers',
                                                    'tablets_printing_image')
            THEN oi.seller_id
            END) AS anzahl_tech_verkäufer,
            ROUND(COUNT(DISTINCT CASE
            WHEN pn.product_category_name_english IN ('Computers_accessories',
                                                    'telephony',
                                                    'electronics',
                                                    'audio',
                                                    'computers',
                                                    'tablets_printing_image')
            THEN oi.seller_id
            END) / COUNT(DISTINCT(oi.seller_id)) * 100, 2) AS prozent_tech_verkäufer
FROM order_items AS oi
LEFT JOIN products AS p ON oi.product_id = p.product_id
LEFT JOIN product_category_name_translation AS pn ON pn.product_category_name = p.product_category_name;
