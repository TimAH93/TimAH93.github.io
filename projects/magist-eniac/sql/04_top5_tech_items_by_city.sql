-- F1.5b: Takes the 5 % most expensive items in the relevant categories and shows per state and city: orders, price cutoff, average delivery days, on-time share and average review.
-- Author: Matías
-- Note: 'computer_accessories' below does not match the category name
-- 'computers_accessories', so the largest tech category is not included.
-- Kept as in the original analysis; see Challenges in the README.

WITH relevant_items AS (
    SELECT
        oi.order_id,
        oi.product_id,
        oi.price
    FROM order_items oi
    JOIN products p
        ON oi.product_id = p.product_id
    LEFT JOIN product_category_name_translation t
        ON p.product_category_name = t.product_category_name
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
),

ranked_items AS (
    SELECT
        order_id,
        product_id,
        price,
        ROW_NUMBER() OVER (ORDER BY price DESC) AS price_rank,
        COUNT(*) OVER () AS total_items
    FROM relevant_items
),

top_5_items AS (
    SELECT
        order_id,
        product_id,
        price
    FROM ranked_items
    WHERE price_rank <= total_items * 0.05
),

price_cutoff AS (
    SELECT
        MIN(price) AS top_5_price_cutoff
    FROM top_5_items
),

qualifying_orders AS (
    SELECT DISTINCT order_id
    FROM top_5_items
),

reviews AS (
    SELECT
        order_id,
        AVG(review_score) AS review_score
    FROM order_reviews
    GROUP BY order_id
)

SELECT
    g.state,
    g.city,
    COUNT(*) AS orders,

    ROUND(pc.top_5_price_cutoff, 2) AS top_5_price_cutoff,

    ROUND(AVG(
        TIMESTAMPDIFF(
            DAY,
            o.order_purchase_timestamp,
            o.order_delivered_customer_date
        )
    ), 2) AS avg_delivery_days,

    ROUND(AVG(
        CASE
            WHEN o.order_delivered_customer_date
                 <= o.order_estimated_delivery_date
            THEN 1
            ELSE 0
        END
    ) * 100, 2) AS on_time_percentage,

    ROUND(AVG(r.review_score), 2) AS avg_review_score

FROM qualifying_orders qo

JOIN orders o
    ON qo.order_id = o.order_id

JOIN customers c
    ON o.customer_id = c.customer_id

LEFT JOIN geo g
    ON c.customer_zip_code_prefix = g.zip_code_prefix

LEFT JOIN reviews r
    ON o.order_id = r.order_id

CROSS JOIN price_cutoff pc

WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_estimated_delivery_date IS NOT NULL

GROUP BY
    g.state,
    g.city,
    pc.top_5_price_cutoff

HAVING COUNT(*) >= 5

ORDER BY avg_delivery_days;
