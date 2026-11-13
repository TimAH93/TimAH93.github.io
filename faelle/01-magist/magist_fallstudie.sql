-- ============================================================
-- Fallstudie 01 · Magist
-- Alle Abfragen für den Report, MySQL (Datenbank: magist)
-- Tim Aßmann · Oktober 2026
--
-- Annahmen
--   Tech-Kategorien: computers_accessories, telephony, electronics,
--                    audio, computers, tablets_printing_image
--   Umsatz: Summe von price, ohne Fracht, ohne stornierte und nicht
--           verfügbare Bestellungen
--   Lieferdauer: Kauf bis Zustellung (Sicht der Kundin, nicht ab Freigabe)
--   Pünktlich: zugestellt am oder vor dem geschätzten Liefertermin
--   Eniac Ø Artikelpreis 540 € ≈ 2.052 BRL (1 € ≈ 3,8 BRL)
-- ============================================================

USE magist;

-- Hilfstabelle: Artikel mit Kategorie und Tech-Kennzeichen
DROP TEMPORARY TABLE IF EXISTS items_cat;
CREATE TEMPORARY TABLE items_cat AS
SELECT oi.order_id, oi.product_id, oi.price,
       pc.product_category_name_english AS cat,
       pc.product_category_name_english IN ('computers_accessories','telephony','electronics',
                                            'audio','computers','tablets_printing_image') AS is_tech
FROM order_items oi
JOIN orders o              ON o.order_id = oi.order_id
LEFT JOIN products p       ON p.product_id = oi.product_id
LEFT JOIN product_category_name_translation pc
                           ON pc.product_category_name = p.product_category_name
WHERE o.order_status NOT IN ('canceled', 'unavailable');

-- Hilfstabelle: zugestellte Bestellungen mit Bundesstaat, Dauer und Pünktlichkeit
DROP TEMPORARY TABLE IF EXISTS deliv;
CREATE TEMPORARY TABLE deliv AS
SELECT o.order_id,
       g.state,
       TIMESTAMPDIFF(HOUR, o.order_purchase_timestamp, o.order_delivered_customer_date) / 24 AS days,
       DATE(o.order_delivered_customer_date) <= DATE(o.order_estimated_delivery_date)       AS on_time
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
LEFT JOIN (SELECT zip_code_prefix, MIN(state) AS state FROM geo GROUP BY zip_code_prefix) g
       ON g.zip_code_prefix = c.customer_zip_code_prefix
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL;


-- ---------- 1 · Wie groß ist Tech auf Magist? ----------
-- Ergebnis: 15.712 Tech-Artikel, 1,66 Mio. BRL = 12,3 % des Umsatzes, Ø 106 BRL
SELECT is_tech,
       COUNT(DISTINCT order_id) AS orders,
       COUNT(*)                 AS items,
       ROUND(SUM(price))        AS revenue_brl,
       ROUND(AVG(price), 1)     AS avg_price_brl
FROM items_cat
GROUP BY is_tech;


-- ---------- 2 · Wie viele Tech-Artikel kosten so viel wie bei Eniac? ----------
-- Ergebnis: 23 von 15.712 Tech-Artikeln kosten 2.052 BRL (540 €) oder mehr
SELECT CASE WHEN price <  100 THEN '1 · unter 100'
            WHEN price <  500 THEN '2 · 100–499'
            WHEN price < 1000 THEN '3 · 500–999'
            WHEN price < 2052 THEN '4 · 1.000–2.051'
            ELSE                   '5 · ab 2.052 (540 €)' END AS price_band,
       COUNT(*)          AS items,
       ROUND(SUM(price)) AS revenue_brl
FROM items_cat
WHERE is_tech = 1
GROUP BY price_band
ORDER BY price_band;


-- ---------- 3 · Wächst Tech schneller als der Rest? ----------
-- Ergebnis: Anteil meist 12–14 %, einmalige Spitze 19 % in Q1 2018
SELECT CONCAT(YEAR(o.order_purchase_timestamp), '-Q', QUARTER(o.order_purchase_timestamp)) AS quarter,
       SUM(i.is_tech)                              AS tech_items,
       COUNT(*)                                    AS all_items,
       ROUND(100 * SUM(i.is_tech) / COUNT(*), 1)   AS tech_share_pct
FROM items_cat i
JOIN orders o ON o.order_id = i.order_id
GROUP BY quarter
ORDER BY quarter;


-- ---------- 4 · Wie schnell und pünktlich liefert Magist? ----------
-- Ergebnis gesamt: Ø 12,6 Tage, 93,1 % pünktlich, 59,3 % in höchstens 12 Tagen
SELECT COUNT(*)                          AS orders,
       ROUND(AVG(days), 1)               AS avg_days,
       ROUND(100 * AVG(on_time), 1)      AS on_time_pct,
       ROUND(100 * AVG(days <= 12), 1)   AS within_12_days_pct
FROM deliv;

-- 4b · nach Bundesstaat (mind. 100 Bestellungen)
-- Ergebnis: SP 8,8 Tage / 79,6 % in 12 Tagen · MG 12,0 / 60,8 % · PR 12,0 / 60,2 %
SELECT state,
       COUNT(*)                          AS orders,
       ROUND(AVG(days), 1)               AS avg_days,
       ROUND(100 * AVG(on_time), 1)      AS on_time_pct,
       ROUND(100 * AVG(days <= 12), 1)   AS within_12_days_pct
FROM deliv
GROUP BY state
HAVING orders >= 100
ORDER BY avg_days;


-- ---------- 5 · Was kostet eine Verspätung? ----------
-- Ergebnis: pünktlich Ø 4,28 Sterne · verspätet Ø 2,29 Sterne, 61,7 % geben 1–2 Sterne
SELECT d.on_time,
       COUNT(*)                                   AS orders,
       ROUND(AVG(r.review_score), 2)              AS avg_score,
       ROUND(100 * AVG(r.review_score <= 2), 1)   AS pct_1_or_2_stars
FROM deliv d
JOIN order_reviews r ON r.order_id = d.order_id
GROUP BY d.on_time;

-- 5b · Bewertung nach Lieferdauer
-- Ergebnis: bis 5 Tage 4,44 · 6–10 4,36 · 11–15 4,26 · 16–20 4,12 · über 20 3,21
SELECT CASE WHEN days <=  5 THEN '1 · bis 5 Tage'
            WHEN days <= 10 THEN '2 · 6–10 Tage'
            WHEN days <= 15 THEN '3 · 11–15 Tage'
            WHEN days <= 20 THEN '4 · 16–20 Tage'
            ELSE                 '5 · über 20 Tage' END AS duration,
       COUNT(*)                      AS orders,
       ROUND(AVG(r.review_score), 2) AS avg_score
FROM deliv d
JOIN order_reviews r ON r.order_id = d.order_id
GROUP BY duration
ORDER BY duration;


-- ---------- 6 · Wie viel Markt deckt ein Test in SP, PR, MG ab? ----------
-- Ergebnis: SP 42,0 % · MG 11,8 % · PR 5,1 % der Bestellungen (zusammen 58,8 %)
SELECT state,
       ROUND(100 * COUNT(*) / (SELECT COUNT(*) FROM deliv), 1) AS pct_orders
FROM deliv
WHERE state IN ('SP', 'PR', 'MG')
GROUP BY state;


-- ---------- 7 · Zahlen Kundinnen teure Bestellungen in Raten? ----------
-- Ergebnis: ab 1.000 BRL Ø 7,8 Raten, 75,6 % zahlen in 6 oder mehr Raten
SELECT CASE WHEN t.total <  100 THEN '1 · unter 100'
            WHEN t.total <  500 THEN '2 · 100–499'
            WHEN t.total < 1000 THEN '3 · 500–999'
            ELSE                     '4 · ab 1.000' END AS order_value,
       COUNT(*)                                        AS payments,
       ROUND(AVG(p.payment_installments), 1)           AS avg_installments,
       ROUND(100 * AVG(p.payment_installments >= 6), 1) AS pct_6_or_more
FROM (SELECT order_id, SUM(price) AS total FROM items_cat GROUP BY order_id) t
JOIN order_payments p ON p.order_id = t.order_id AND p.payment_type = 'credit_card'
GROUP BY order_value
ORDER BY order_value;
