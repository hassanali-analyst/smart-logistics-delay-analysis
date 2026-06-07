-- =====================================================================
-- Smart Logistics Supply Chain - Delay Analysis (SQL)
-- Author: Hassan Ali
-- Table assumed name: smart_logistics
-- Note: load the CSV into a table called smart_logistics first.
-- =====================================================================

-- ---------------------------------------------------------------------
-- 0. DATA QUALITY CHECKS
-- ---------------------------------------------------------------------

-- How many records in total?
SELECT COUNT(*) AS total_rows
FROM smart_logistics;

-- Are there duplicate rows? (count distinct vs total)
SELECT COUNT(*) AS total_rows,
       COUNT(DISTINCT CONCAT(Timestamp, Asset_ID, Latitude, Longitude)) AS unique_rows
FROM smart_logistics;


-- ---------------------------------------------------------------------
-- ANALYSIS 1: Overall delay rate
-- ---------------------------------------------------------------------
SELECT
    COUNT(*)                                          AS total_shipments,
    SUM(Logistics_Delay)                              AS delayed_shipments,
    ROUND(SUM(Logistics_Delay) * 100.0 / COUNT(*), 1) AS delay_rate_pct
FROM smart_logistics;
-- Result: 1000 total, 566 delayed, 56.6%


-- ---------------------------------------------------------------------
-- ANALYSIS 2: Delay reasons among DELAYED shipments
-- (Caveat: the reason column is inconsistent - "None" also appears
--  on delayed shipments, so treat these counts with care.)
-- ---------------------------------------------------------------------
SELECT
    Logistics_Delay_Reason,
    COUNT(*) AS num_shipments
FROM smart_logistics
WHERE Logistics_Delay = 1
GROUP BY Logistics_Delay_Reason
ORDER BY num_shipments DESC;


-- ---------------------------------------------------------------------
-- ANALYSIS 3: Delay rate by traffic condition  (KEY INSIGHT)
-- ---------------------------------------------------------------------
SELECT
    Traffic_Status,
    COUNT(*)                                          AS shipments,
    SUM(Logistics_Delay)                              AS delayed,
    ROUND(SUM(Logistics_Delay) * 100.0 / COUNT(*), 1) AS delay_rate_pct
FROM smart_logistics
GROUP BY Traffic_Status
ORDER BY delay_rate_pct DESC;
-- Result: Heavy = 100%, Detour = 35.9%, Clear = 35.1%


-- ---------------------------------------------------------------------
-- ANALYSIS 4: Average waiting time - on time vs delayed
-- ---------------------------------------------------------------------
SELECT
    Logistics_Delay,                       -- 0 = on time, 1 = delayed
    ROUND(AVG(Waiting_Time), 1) AS avg_waiting_minutes
FROM smart_logistics
GROUP BY Logistics_Delay;
-- Result: on time = 36.1 min, delayed = 34.3 min (almost the same)


-- ---------------------------------------------------------------------
-- ANALYSIS 5: Delay rate by truck (asset)
-- ---------------------------------------------------------------------
SELECT
    Asset_ID,
    COUNT(*)                                          AS shipments,
    SUM(Logistics_Delay)                              AS delayed,
    ROUND(SUM(Logistics_Delay) * 100.0 / COUNT(*), 1) AS delay_rate_pct
FROM smart_logistics
GROUP BY Asset_ID
ORDER BY delay_rate_pct DESC;
-- Result: Truck_10 worst (64.8%), Truck_5 best (49.5%)
