-- =============================================================================
-- AgriShield Analytics – SQL Queries
-- Database: AgriShield_DB
-- Author: AgriShield Analytics Team
-- Date: 2024
-- Description: All SQL queries supporting Days 1-9 deliverables
-- =============================================================================

-- ── TABLE CREATION ────────────────────────────────────────────────────────────

CREATE TABLE DimCrop (
    crop_id   VARCHAR(20) PRIMARY KEY,
    crop_name VARCHAR(100) NOT NULL
);

CREATE TABLE DimFarmer (
    farmer_id   VARCHAR(20) PRIMARY KEY,
    farmer_name VARCHAR(150) NOT NULL
);

CREATE TABLE DimLocation (
    location_id   VARCHAR(20) PRIMARY KEY,
    location_name VARCHAR(150) NOT NULL,
    soil_type     VARCHAR(100)
);

CREATE TABLE DimWeather (
    weather_id    VARCHAR(20) PRIMARY KEY,
    weather_type  VARCHAR(100),
    temperature_c DECIMAL(5,2),
    humidity_pct  DECIMAL(5,2),
    rainfall_mm   DECIMAL(8,2)
);

CREATE TABLE DimPest (
    pest_id        VARCHAR(20) PRIMARY KEY,
    pest_name      VARCHAR(150),
    pest_severity  VARCHAR(20),
    pest_risk_score INT
);

CREATE TABLE DimDisease (
    disease_id        VARCHAR(20) PRIMARY KEY,
    disease_name      VARCHAR(150),
    disease_severity  VARCHAR(20),
    disease_risk_score INT
);

CREATE TABLE DimDate (
    date_id          VARCHAR(10) PRIMARY KEY,
    monitoring_date  DATE NOT NULL,
    year             INT,
    month            INT,
    quarter          INT,
    month_name       VARCHAR(20),
    day_of_week      VARCHAR(20),
    week_number      INT
);

CREATE TABLE FactCropHealth (
    record_id          VARCHAR(20) PRIMARY KEY,
    crop_id            VARCHAR(20) REFERENCES DimCrop(crop_id),
    farmer_id          VARCHAR(20) REFERENCES DimFarmer(farmer_id),
    location_id        VARCHAR(20) REFERENCES DimLocation(location_id),
    weather_id         VARCHAR(20) REFERENCES DimWeather(weather_id),
    pest_id            VARCHAR(20) REFERENCES DimPest(pest_id),
    disease_id         VARCHAR(20) REFERENCES DimDisease(disease_id),
    date_id            VARCHAR(10) REFERENCES DimDate(date_id),
    crop_yield_tons_ha DECIMAL(8,4),
    farm_area_ha       DECIMAL(8,2),
    ndvi_index         DECIMAL(6,4),
    health_score       DECIMAL(5,2),
    fertilizer_kg_ha   DECIMAL(8,2),
    pesticide_l_ha     DECIMAL(8,2),
    water_usage_l      DECIMAL(12,2),
    total_revenue      DECIMAL(15,2),
    combined_risk      INT,
    water_efficiency   DECIMAL(10,4),
    yield_category     VARCHAR(20),
    health_category    VARCHAR(20),
    growth_stage       VARCHAR(50),
    irrigation_method  VARCHAR(50)
);

-- =============================================================================
-- DAY 1 – Data Quality Queries
-- =============================================================================

-- 1.1: Check for duplicate records
SELECT farmer_id, crop_id, monitoring_date, COUNT(*) AS duplicate_count
FROM FactCropHealth f
JOIN DimDate d ON f.date_id = d.date_id
GROUP BY farmer_id, crop_id, monitoring_date
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;

-- 1.2: Missing value count per numeric column
SELECT
    COUNT(*) - COUNT(crop_yield_tons_ha) AS missing_yield,
    COUNT(*) - COUNT(health_score)        AS missing_health,
    COUNT(*) - COUNT(ndvi_index)          AS missing_ndvi,
    COUNT(*) - COUNT(pesticide_l_ha)      AS missing_pesticide,
    COUNT(*) - COUNT(water_usage_l)       AS missing_water,
    COUNT(*) AS total_rows
FROM FactCropHealth;

-- 1.3: Star Schema record counts
SELECT 'FactCropHealth'  AS table_name, COUNT(*) AS row_count FROM FactCropHealth UNION ALL
SELECT 'DimCrop',          COUNT(*) FROM DimCrop            UNION ALL
SELECT 'DimFarmer',        COUNT(*) FROM DimFarmer          UNION ALL
SELECT 'DimLocation',      COUNT(*) FROM DimLocation        UNION ALL
SELECT 'DimWeather',       COUNT(*) FROM DimWeather         UNION ALL
SELECT 'DimPest',          COUNT(*) FROM DimPest            UNION ALL
SELECT 'DimDisease',       COUNT(*) FROM DimDisease         UNION ALL
SELECT 'DimDate',          COUNT(*) FROM DimDate;

-- =============================================================================
-- DAY 2 – EDA Queries
-- =============================================================================

-- 2.1: Descriptive Statistics
SELECT
    ROUND(AVG(crop_yield_tons_ha), 4)        AS avg_yield,
    ROUND(STDDEV(crop_yield_tons_ha), 4)     AS std_yield,
    ROUND(MIN(crop_yield_tons_ha), 4)        AS min_yield,
    ROUND(MAX(crop_yield_tons_ha), 4)        AS max_yield,
    ROUND(AVG(health_score), 4)              AS avg_health,
    ROUND(STDDEV(health_score), 4)           AS std_health,
    ROUND(AVG(ndvi_index), 4)               AS avg_ndvi,
    ROUND(AVG(pesticide_l_ha), 4)           AS avg_pesticide,
    ROUND(AVG(water_usage_l), 4)            AS avg_water,
    COUNT(*)                                 AS total_records
FROM FactCropHealth;

-- 2.2: Percentile distribution (PostgreSQL syntax)
SELECT
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY crop_yield_tons_ha) AS q1_yield,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY crop_yield_tons_ha) AS median_yield,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY crop_yield_tons_ha) AS q3_yield,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY crop_yield_tons_ha) AS p95_yield
FROM FactCropHealth;

-- 2.3: Correlation-like metric (yield vs health)
SELECT
    crop_name,
    ROUND(AVG(crop_yield_tons_ha), 3) AS avg_yield,
    ROUND(AVG(health_score), 3)       AS avg_health,
    ROUND(AVG(ndvi_index), 3)         AS avg_ndvi,
    COUNT(*)                           AS records
FROM FactCropHealth f
JOIN DimCrop c ON f.crop_id = c.crop_id
GROUP BY crop_name
ORDER BY avg_yield DESC;

-- =============================================================================
-- DAY 3 – RFM Analysis Queries
-- =============================================================================

-- 3.1: Compute RFM Metrics
WITH snapshot AS (
    SELECT MAX(d.monitoring_date) + INTERVAL '1 day' AS snap_date
    FROM DimDate d
),
rfm_raw AS (
    SELECT
        f.farmer_id,
        fn.farmer_name,
        DATEDIFF(s.snap_date, MAX(d.monitoring_date)) AS recency_days,
        COUNT(f.record_id)                             AS frequency,
        ROUND(SUM(f.crop_yield_tons_ha), 2)            AS monetary
    FROM FactCropHealth f
    JOIN DimDate d   ON f.date_id    = d.date_id
    JOIN DimFarmer fn ON f.farmer_id  = fn.farmer_id
    CROSS JOIN snapshot s
    GROUP BY f.farmer_id, fn.farmer_name, s.snap_date
)
SELECT
    farmer_id,
    farmer_name,
    recency_days,
    frequency,
    monetary,
    NTILE(5) OVER (ORDER BY recency_days DESC)  AS r_score,
    NTILE(5) OVER (ORDER BY frequency)           AS f_score,
    NTILE(5) OVER (ORDER BY monetary)            AS m_score
FROM rfm_raw
ORDER BY monetary DESC;

-- 3.2: Segment Distribution
WITH rfm_scores AS (
    SELECT
        f.farmer_id,
        COUNT(f.record_id)               AS frequency,
        ROUND(SUM(f.crop_yield_tons_ha),2) AS monetary,
        NTILE(5) OVER (ORDER BY COUNT(f.record_id))               AS f_score,
        NTILE(5) OVER (ORDER BY SUM(f.crop_yield_tons_ha))        AS m_score
    FROM FactCropHealth f
    GROUP BY f.farmer_id
),
segmented AS (
    SELECT *,
        CASE
            WHEN f_score >= 4 AND m_score >= 4 THEN 'Champions'
            WHEN f_score >= 3 AND m_score >= 3 THEN 'Loyal Farmers'
            WHEN f_score >= 3 THEN 'Potential Farmers'
            WHEN f_score < 3 AND m_score >= 3 THEN 'At Risk'
            ELSE 'Lost Farmers'
        END AS segment
    FROM rfm_scores
)
SELECT segment, COUNT(*) AS count,
       ROUND(AVG(frequency), 2)  AS avg_frequency,
       ROUND(AVG(monetary), 2)   AS avg_monetary,
       ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pct
FROM segmented
GROUP BY segment
ORDER BY count DESC;

-- =============================================================================
-- DAY 4 – Performance Analysis Queries
-- =============================================================================

-- 4.1: Crop Performance Summary
SELECT
    c.crop_name,
    ROUND(AVG(f.crop_yield_tons_ha), 3) AS avg_yield,
    ROUND(AVG(f.health_score), 2)       AS avg_health,
    ROUND(AVG(f.ndvi_index), 3)         AS avg_ndvi,
    ROUND(AVG(f.pesticide_l_ha), 2)     AS avg_pesticide,
    ROUND(AVG(f.water_usage_l), 0)      AS avg_water,
    ROUND(SUM(f.total_revenue)/1e6, 2)  AS total_revenue_m,
    COUNT(f.record_id)                   AS total_records
FROM FactCropHealth f
JOIN DimCrop c ON f.crop_id = c.crop_id
GROUP BY c.crop_name
ORDER BY avg_yield DESC;

-- 4.2: Top 5 and Bottom 5 Crops
(SELECT crop_name, ROUND(AVG(crop_yield_tons_ha),3) AS avg_yield, 'Top 5' AS category
 FROM FactCropHealth f JOIN DimCrop c ON f.crop_id = c.crop_id
 GROUP BY crop_name ORDER BY avg_yield DESC LIMIT 5)
UNION ALL
(SELECT crop_name, ROUND(AVG(crop_yield_tons_ha),3) AS avg_yield, 'Bottom 5' AS category
 FROM FactCropHealth f JOIN DimCrop c ON f.crop_id = c.crop_id
 GROUP BY crop_name ORDER BY avg_yield ASC LIMIT 5);

-- 4.3: Regional Performance
SELECT
    l.location_name,
    l.soil_type,
    ROUND(AVG(f.crop_yield_tons_ha), 3) AS avg_yield,
    ROUND(AVG(f.health_score), 2)       AS avg_health,
    ROUND(AVG(f.water_usage_l), 0)      AS avg_water,
    COUNT(DISTINCT f.farmer_id)          AS farmer_count,
    ROUND(SUM(f.total_revenue)/1e6, 2)  AS revenue_m
FROM FactCropHealth f
JOIN DimLocation l ON f.location_id = l.location_id
GROUP BY l.location_name, l.soil_type
ORDER BY avg_yield DESC;

-- 4.4: Disease Frequency by Crop
SELECT
    c.crop_name,
    di.disease_name,
    di.disease_severity,
    COUNT(*) AS frequency,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY c.crop_name), 2) AS pct_in_crop
FROM FactCropHealth f
JOIN DimCrop c    ON f.crop_id    = c.crop_id
JOIN DimDisease di ON f.disease_id = di.disease_id
GROUP BY c.crop_name, di.disease_name, di.disease_severity
ORDER BY frequency DESC;

-- =============================================================================
-- DAY 5 – Anomaly Detection Queries
-- =============================================================================

-- 5.1: Z-Score anomalies (using standard deviation)
WITH stats AS (
    SELECT
        AVG(pesticide_l_ha)    AS mean_pest,
        STDDEV(pesticide_l_ha) AS std_pest,
        AVG(water_usage_l)     AS mean_water,
        STDDEV(water_usage_l)  AS std_water,
        AVG(crop_yield_tons_ha) AS mean_yield,
        STDDEV(crop_yield_tons_ha) AS std_yield
    FROM FactCropHealth
)
SELECT
    f.record_id,
    f.farmer_id,
    f.pesticide_l_ha,
    f.water_usage_l,
    f.crop_yield_tons_ha,
    ROUND(ABS((f.pesticide_l_ha - s.mean_pest) / NULLIF(s.std_pest, 0)), 3)     AS z_pesticide,
    ROUND(ABS((f.water_usage_l - s.mean_water) / NULLIF(s.std_water, 0)), 3)    AS z_water,
    ROUND(ABS((f.crop_yield_tons_ha - s.mean_yield) / NULLIF(s.std_yield, 0)), 3) AS z_yield
FROM FactCropHealth f, stats s
WHERE
    ABS((f.pesticide_l_ha - s.mean_pest) / NULLIF(s.std_pest, 0)) > 3
    OR ABS((f.water_usage_l - s.mean_water) / NULLIF(s.std_water, 0)) > 3
    OR ABS((f.crop_yield_tons_ha - s.mean_yield) / NULLIF(s.std_yield, 0)) > 3
ORDER BY z_pesticide DESC;

-- 5.2: IQR-based outliers
WITH iqr_calc AS (
    SELECT
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY pesticide_l_ha) AS q1_pest,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY pesticide_l_ha) AS q3_pest,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY water_usage_l)  AS q1_water,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY water_usage_l)  AS q3_water
    FROM FactCropHealth
)
SELECT f.record_id, f.farmer_id, f.pesticide_l_ha, f.water_usage_l,
       'IQR_Outlier' AS flag_type
FROM FactCropHealth f, iqr_calc i
WHERE
    f.pesticide_l_ha < (i.q1_pest - 1.5 * (i.q3_pest - i.q1_pest))
    OR f.pesticide_l_ha > (i.q3_pest + 1.5 * (i.q3_pest - i.q1_pest))
    OR f.water_usage_l  > (i.q3_water + 1.5 * (i.q3_water - i.q1_water))
ORDER BY f.pesticide_l_ha DESC;

-- 5.3: Duplicate detection
SELECT farmer_id, crop_id, monitoring_date,
       COUNT(*) AS dup_count,
       'DuplicateRecord' AS flag_type
FROM FactCropHealth f
JOIN DimDate d ON f.date_id = d.date_id
GROUP BY farmer_id, crop_id, monitoring_date
HAVING COUNT(*) > 1;

-- =============================================================================
-- DAY 6 – KPI Dashboard Queries
-- =============================================================================

-- 6.1: Executive KPI Summary
SELECT
    COUNT(DISTINCT f.farmer_id)                                          AS total_farms,
    COUNT(f.record_id)                                                   AS total_records,
    SUM(CASE WHEN f.health_score >= 70 THEN 1 ELSE 0 END)              AS healthy_crops,
    SUM(CASE WHEN di.disease_severity IN ('High','Critical') THEN 1 ELSE 0 END) AS diseased_crops,
    SUM(CASE WHEN p.pest_severity    IN ('High','Critical') THEN 1 ELSE 0 END)  AS pest_cases,
    ROUND(AVG(f.crop_yield_tons_ha), 3)                                 AS avg_yield,
    ROUND(AVG(f.pesticide_l_ha), 3)                                     AS avg_pesticide,
    ROUND(AVG(f.water_usage_l), 0)                                      AS avg_irrigation,
    ROUND(SUM(CASE WHEN di.disease_severity IN ('High','Critical') THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS disease_rate_pct,
    ROUND(SUM(CASE WHEN f.health_score >= 70 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS healthy_pct,
    ROUND(SUM(f.total_revenue) / 1e6, 2)                               AS total_revenue_m
FROM FactCropHealth f
JOIN DimDisease di ON f.disease_id = di.disease_id
JOIN DimPest     p  ON f.pest_id    = p.pest_id;

-- 6.2: Monthly Trend for KPI Dashboard
SELECT
    d.year, d.month, d.month_name,
    ROUND(AVG(f.crop_yield_tons_ha), 3)                                    AS avg_yield,
    ROUND(AVG(f.health_score), 2)                                          AS avg_health,
    ROUND(SUM(CASE WHEN di.disease_severity IN ('High','Critical') THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS disease_rate,
    ROUND(AVG(f.pesticide_l_ha), 3)                                        AS avg_pesticide,
    COUNT(f.record_id)                                                     AS record_count
FROM FactCropHealth f
JOIN DimDate    d  ON f.date_id    = d.date_id
JOIN DimDisease di ON f.disease_id = di.disease_id
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;

-- =============================================================================
-- DAY 8 – Forecasting Support Queries
-- =============================================================================

-- 8.1: Daily time series for forecasting
SELECT
    d.monitoring_date                          AS ds,
    ROUND(AVG(f.crop_yield_tons_ha), 4)        AS avg_yield,
    COUNT(f.record_id)                          AS record_count,
    ROUND(AVG(f.health_score), 2)              AS avg_health,
    ROUND(AVG(f.ndvi_index), 4)                AS avg_ndvi
FROM FactCropHealth f
JOIN DimDate d ON f.date_id = d.date_id
GROUP BY d.monitoring_date
ORDER BY d.monitoring_date;

-- 8.2: Seasonal analysis (by month)
SELECT
    d.month, d.month_name,
    ROUND(AVG(f.crop_yield_tons_ha), 3) AS avg_yield,
    ROUND(STDDEV(f.crop_yield_tons_ha), 3) AS std_yield,
    ROUND(AVG(f.health_score), 2)       AS avg_health,
    COUNT(*)                             AS record_count
FROM FactCropHealth f
JOIN DimDate d ON f.date_id = d.date_id
GROUP BY d.month, d.month_name
ORDER BY d.month;

-- =============================================================================
-- DAY 9 – Cohort Analysis Queries
-- =============================================================================

-- 9.1: Farmer first monitoring date (cohort assignment)
SELECT farmer_id, MIN(d.monitoring_date) AS first_monitoring_date,
       DATE_TRUNC('month', MIN(d.monitoring_date)) AS cohort_month
FROM FactCropHealth f
JOIN DimDate d ON f.date_id = d.date_id
GROUP BY farmer_id;

-- 9.2: Cohort retention matrix
WITH first_month AS (
    SELECT farmer_id, DATE_TRUNC('month', MIN(d.monitoring_date)) AS cohort_month
    FROM FactCropHealth f JOIN DimDate d ON f.date_id = d.date_id
    GROUP BY farmer_id
),
activity AS (
    SELECT f.farmer_id, DATE_TRUNC('month', d.monitoring_date) AS active_month
    FROM FactCropHealth f JOIN DimDate d ON f.date_id = d.date_id
),
cohort_activity AS (
    SELECT
        fm.cohort_month,
        EXTRACT(MONTH FROM AGE(a.active_month, fm.cohort_month)) AS month_offset,
        COUNT(DISTINCT a.farmer_id) AS active_farmers
    FROM first_month fm
    JOIN activity a ON fm.farmer_id = a.farmer_id
    GROUP BY fm.cohort_month, month_offset
),
cohort_size AS (
    SELECT cohort_month, COUNT(DISTINCT farmer_id) AS total_farmers
    FROM first_month GROUP BY cohort_month
)
SELECT
    ca.cohort_month,
    ca.month_offset,
    ca.active_farmers,
    cs.total_farmers,
    ROUND(ca.active_farmers * 100.0 / cs.total_farmers, 2) AS retention_pct
FROM cohort_activity ca
JOIN cohort_size cs ON ca.cohort_month = cs.cohort_month
ORDER BY ca.cohort_month, ca.month_offset;

-- 9.3: Regional cohort analysis
SELECT
    l.location_name,
    d.year AS cohort_year,
    COUNT(DISTINCT f.farmer_id)          AS unique_farmers,
    COUNT(f.record_id)                   AS records,
    ROUND(AVG(f.crop_yield_tons_ha), 3) AS avg_yield,
    ROUND(AVG(f.health_score), 2)       AS avg_health,
    ROUND(SUM(CASE WHEN di.disease_severity IN ('High','Critical') THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS disease_rate
FROM FactCropHealth f
JOIN DimDate     d  ON f.date_id     = d.date_id
JOIN DimLocation l  ON f.location_id = l.location_id
JOIN DimDisease  di ON f.disease_id  = di.disease_id
GROUP BY l.location_name, d.year
ORDER BY l.location_name, d.year;

-- 9.4: Disease retention (persistence across months)
SELECT
    di.disease_name,
    COUNT(DISTINCT DATE_TRUNC('month', d.monitoring_date)) AS months_active,
    COUNT(*)                                               AS total_occurrences,
    ROUND(AVG(f.crop_yield_tons_ha), 3)                   AS avg_yield_when_diseased,
    ROUND(AVG(f.health_score), 2)                         AS avg_health_when_diseased
FROM FactCropHealth f
JOIN DimDisease di ON f.disease_id = di.disease_id
JOIN DimDate    d  ON f.date_id    = d.date_id
GROUP BY di.disease_name
ORDER BY months_active DESC, total_occurrences DESC;

-- =============================================================================
-- UTILITY – Data Quality Report
-- =============================================================================

-- Overall data quality score
SELECT
    COUNT(*) AS total_records,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM FactCropHealth), 2) AS completeness_pct,
    COUNT(DISTINCT farmer_id)   AS unique_farmers,
    COUNT(DISTINCT crop_id)     AS unique_crops,
    COUNT(DISTINCT location_id) AS unique_locations,
    MIN(d.monitoring_date) AS earliest_date,
    MAX(d.monitoring_date) AS latest_date,
    DATEDIFF(MAX(d.monitoring_date), MIN(d.monitoring_date)) AS date_span_days
FROM FactCropHealth f
JOIN DimDate d ON f.date_id = d.date_id;
