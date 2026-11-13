-- F1.2: Per tech category: products, items sold, share of sales, revenue and revenue share, average price vs. average price of all items.
-- Author: Julia

USE magist;
SELECT
    p.product_category_name AS kategorie_portugiesisch,
    t.product_category_name_english AS kategorie_englisch,
    COUNT(DISTINCT p.product_id) AS anzahl_produkte,
    COUNT(oi.product_id) AS verkauft_produkte,
    ROUND(COUNT(oi.product_id) / (SELECT COUNT(product_id) FROM order_items) * 100, 2) AS prozent_von_verkauf,
    ROUND(SUM(oi.price), 2) AS sum_verkauf,
    ROUND(SUM(oi.price) / (SELECT SUM(price) FROM order_items) * 100, 2) AS prozent_sum_verkauf,
    ROUND(AVG(oi.price), 2) AS avg_price,
    (SELECT ROUND(AVG(price), 2) FROM order_items) AS AVG
FROM magist.products AS p
LEFT JOIN magist.product_category_name_translation AS t
    ON p.product_category_name = t.product_category_name
lEFT JOIN order_items AS OI
    ON p.product_id = oi.product_id
WHERE t.product_category_name_english IN ('Computers_accessories',
                                                    'telephony',
                                                    'electronics',
                                                    'audio',
                                                    'computers',
                                                    'tablets_printing_image')
GROUP BY
    p.product_category_name,
    t.product_category_name_english
ORDER BY
    anzahl_produkte DESC;
