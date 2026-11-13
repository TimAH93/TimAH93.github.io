-- F2.3: Total revenue, tech revenue and its share, average price overall and for tech items.
-- Author: Julia

SELECT ROUND(SUM(oi.price), 2) AS verdienstsumme,
        ROUND(SUM(CASE
            WHEN pn.product_category_name_english IN ('Computers_accessories',
                                                    'telephony',
                                                    'electronics',
                                                    'audio',
                                                    'computers',
                                                    'tablets_printing_image')
            THEN oi.price
            END), 2) AS tech_verdienstsumme,
            ROUND(SUM(CASE
            WHEN pn.product_category_name_english IN ('Computers_accessories',
                                                    'telephony',
                                                    'electronics',
                                                    'audio',
                                                    'computers',
                                                    'tablets_printing_image')
            THEN oi.price
            END) / SUM(oi.price) * 100, 2) AS prozent_tech_verdienstsumme,
            ROUND(AVG(oi.price), 2) AS AVG_verdint,
            ROUND(AVG(CASE
            WHEN pn.product_category_name_english IN ('Computers_accessories',
                                                    'telephony',
                                                    'electronics',
                                                    'audio',
                                                    'computers',
                                                    'tablets_printing_image')
            THEN oi.price
            END), 2) AS AVG_tech_verdient
FROM order_items AS oi
LEFT JOIN products AS p ON oi.product_id = p.product_id
LEFT JOIN product_category_name_translation AS pn ON pn.product_category_name = p.product_category_name;
