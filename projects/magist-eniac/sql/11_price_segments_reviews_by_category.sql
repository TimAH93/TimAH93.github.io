-- F4.1: Splits the 4 % most expensive items into price segments (top 1-4 %) and shows per category: average/minimum price, on-time share and average review.
-- Author: Matías
-- Note: 'computer_accessories' below does not match the category name
-- 'computers_accessories', so the largest tech category is not included.
-- Kept as in the original analysis; see Challenges in the README.

WITH ranked_items AS (
    SELECT
        oi.order_id,
        oi.product_id,
        oi.price,

        ROW_NUMBER() OVER (
            ORDER BY oi.price DESC
        ) AS price_rank,

        COUNT(*) OVER () AS total_items

    FROM order_items oi
),

price_segments AS (
    SELECT
        order_id,
        product_id,
        price,

        CASE
            WHEN price_rank <= total_items * 0.01 THEN 'Top 1%'
            WHEN price_rank <= total_items * 0.02 THEN 'Top 2%'
            WHEN price_rank <= total_items * 0.03 THEN 'Top 3%'
            WHEN price_rank <= total_items * 0.04 THEN 'Top 4%'
        END AS price_segment

    FROM ranked_items

    WHERE price_rank <= total_items * 0.04
),

delivery_reviews AS (
    SELECT
        o.order_id,

        CASE
            WHEN o.order_delivered_customer_date
                 <= o.order_estimated_delivery_date
            THEN 1
            ELSE 0
        END AS on_time,

        r.review_score

    FROM orders o

    LEFT JOIN order_reviews r
        ON o.order_id = r.order_id

    WHERE o.order_status = 'delivered'
      AND o.order_delivered_customer_date IS NOT NULL
      AND o.order_estimated_delivery_date IS NOT NULL
)

SELECT
    t.product_category_name_english AS category,

    /* PRICE */
    ROUND(
        AVG(
            CASE
                WHEN ps.price_segment = 'Top 1%'
                THEN ps.price
            END
        ), 2
    ) AS avg_top1,

    ROUND(
        MIN(
            CASE
                WHEN ps.price_segment = 'Top 1%'
                THEN ps.price
            END
        ), 2
    ) AS min_top1,

    ROUND(
        AVG(
            CASE
                WHEN ps.price_segment = 'Top 2%'
                THEN ps.price
            END
        ), 2
    ) AS avg_top2,

    ROUND(
        MIN(
            CASE
                WHEN ps.price_segment = 'Top 2%'
                THEN ps.price
            END
        ), 2
    ) AS min_top2,

    ROUND(
        AVG(
            CASE
                WHEN ps.price_segment = 'Top 3%'
                THEN ps.price
            END
        ), 2
    ) AS avg_top3,

    ROUND(
        MIN(
            CASE
                WHEN ps.price_segment = 'Top 3%'
                THEN ps.price
            END
        ), 2
    ) AS min_top3,

    ROUND(
        AVG(
            CASE
                WHEN ps.price_segment = 'Top 4%'
                THEN ps.price
            END
        ), 2
    ) AS avg_top4,

    ROUND(
        MIN(
            CASE
                WHEN ps.price_segment = 'Top 4%'
                THEN ps.price
            END
        ), 2
    ) AS min_top4,

    /* DELIVERY */
    ROUND(
        AVG(
            CASE
                WHEN ps.price_segment = 'Top 1%'
                THEN dr.on_time
            END
        ) * 100,
        2
    ) AS on_time_top1,

    ROUND(
        AVG(
            CASE
                WHEN ps.price_segment = 'Top 2%'
                THEN dr.on_time
            END
        ) * 100,
        2
    ) AS on_time_top2,

    ROUND(
        AVG(
            CASE
                WHEN ps.price_segment = 'Top 3%'
                THEN dr.on_time
            END
        ) * 100,
        2
    ) AS on_time_top3,

    ROUND(
        AVG(
            CASE
                WHEN ps.price_segment = 'Top 4%'
                THEN dr.on_time
            END
        ) * 100,
        2
    ) AS on_time_top4,

    /* REVIEWS */
    ROUND(
        AVG(
            CASE
                WHEN ps.price_segment = 'Top 1%'
                THEN dr.review_score
            END
        ), 2
    ) AS avg_review_top1,

    ROUND(
        AVG(
            CASE
                WHEN ps.price_segment = 'Top 2%'
                THEN dr.review_score
            END
        ), 2
    ) AS avg_review_top2,

    ROUND(
        AVG(
            CASE
                WHEN ps.price_segment = 'Top 3%'
                THEN dr.review_score
            END
        ), 2
    ) AS avg_review_top3,

    ROUND(
        AVG(
            CASE
                WHEN ps.price_segment = 'Top 4%'
                THEN dr.review_score
            END
        ), 2
    ) AS avg_review_top4

FROM price_segments ps

JOIN products p
    ON ps.product_id = p.product_id

LEFT JOIN product_category_name_translation t
    ON p.product_category_name = t.product_category_name

LEFT JOIN delivery_reviews dr
    ON ps.order_id = dr.order_id

WHERE t.product_category_name_english IN (
    'computer_accessories',
    'telephony',
    'electronics',
    'audio',
    'computers',
    'tablets_printing_image',
    'watches_gifts',
    'cool_stuff'
)

GROUP BY
    t.product_category_name_english

ORDER BY
    t.product_category_name_english;
