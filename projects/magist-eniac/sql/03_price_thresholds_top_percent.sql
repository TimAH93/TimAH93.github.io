-- F1.5a: Minimum price an item needs to be among the 1-5 % most expensive items sold.
-- Author: Matías

WITH ranked_items AS (
    SELECT
        price,
        ROW_NUMBER() OVER (ORDER BY price DESC) AS price_rank,
        COUNT(*) OVER () AS total_items
    FROM order_items
)

SELECT
    'Top 1%' AS segment,
    ROUND(
        MIN(CASE
            WHEN price_rank <= total_items * 0.01
            THEN price
        END), 2
    ) AS minimum_price
FROM ranked_items

UNION ALL

SELECT
    'Top 2%',
    ROUND(
        MIN(CASE
            WHEN price_rank <= total_items * 0.02
            THEN price
        END), 2
    )
FROM ranked_items

UNION ALL

SELECT
    'Top 3%',
    ROUND(
        MIN(CASE
            WHEN price_rank <= total_items * 0.03
            THEN price
        END), 2
    )
FROM ranked_items

UNION ALL

SELECT
    'Top 4%',
    ROUND(
        MIN(CASE
            WHEN price_rank <= total_items * 0.04
            THEN price
        END), 2
    )
FROM ranked_items

UNION ALL

SELECT
    'Top 5%',
    ROUND(
        MIN(CASE
            WHEN price_rank <= total_items * 0.05
            THEN price
        END), 2
    )
FROM ranked_items;
