-- F1.1: Products per category, to identify the tech categories.
-- Author: Tim

USE magist;

SELECT
    p.product_category_name         AS category_pt,
    t.product_category_name_english AS category_en,
    COUNT(DISTINCT p.product_id)    AS products
FROM magist.products AS p
LEFT JOIN magist.product_category_name_translation AS t
    ON p.product_category_name = t.product_category_name
GROUP BY
    p.product_category_name,
    t.product_category_name_english
ORDER BY
    products DESC;
