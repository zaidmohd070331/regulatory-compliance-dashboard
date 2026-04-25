-- sql_queries.sql
-- SQL extraction and transformation queries for KRI compliance monitoring
-- Designed for ingestion into Power BI compliance dashboard

-- ============================================================
-- 1. Full KRI status summary with RAG classification
-- ============================================================
SELECT
    kri_id,
    kri_name,
    business_unit,
    regulatory_domain,
    current_value,
    threshold_warning,
    threshold_breach,
    unit,
    reporting_date,
    trend,
    CASE
        WHEN threshold_breach > threshold_warning THEN
            CASE
                WHEN current_value >= threshold_breach THEN 'Breach'
                WHEN current_value >= threshold_warning THEN 'Warning'
                ELSE 'Within Threshold'
            END
        ELSE
            CASE
                WHEN current_value <= threshold_breach THEN 'Breach'
                WHEN current_value <= threshold_warning THEN 'Warning'
                ELSE 'Within Threshold'
            END
    END AS kri_status,
    CASE
        WHEN trend = 'Increasing'
         AND threshold_breach > threshold_warning THEN 'Deteriorating'
        WHEN trend = 'Decreasing'
         AND threshold_breach < threshold_warning THEN 'Deteriorating'
        ELSE 'Stable or Improving'
    END AS outlook
FROM kri_data
ORDER BY reporting_date DESC;


-- ============================================================
-- 2. Breached KRIs requiring immediate escalation
-- ============================================================
SELECT
    kri_id,
    kri_name,
    business_unit,
    regulatory_domain,
    current_value,
    threshold_breach,
    unit,
    trend,
    reporting_date
FROM kri_data
WHERE
    (threshold_breach > threshold_warning
     AND current_value >= threshold_breach)
 OR (threshold_breach < threshold_warning
     AND current_value <= threshold_breach)
ORDER BY regulatory_domain, kri_name;


-- ============================================================
-- 3. KRI summary by regulatory domain (for heatmap)
-- ============================================================
SELECT
    regulatory_domain,
    COUNT(kri_id)                        AS total_kris,
    SUM(CASE
            WHEN (threshold_breach > threshold_warning
                  AND current_value >= threshold_breach)
              OR (threshold_breach < threshold_warning
                  AND current_value <= threshold_breach)
            THEN 1 ELSE 0
        END)                             AS breached_kris,
    SUM(CASE
            WHEN (threshold_breach > threshold_warning
                  AND current_value >= threshold_warning
                  AND current_value < threshold_breach)
              OR (threshold_breach < threshold_warning
                  AND current_value <= threshold_warning
                  AND current_value > threshold_breach)
            THEN 1 ELSE 0
        END)                             AS warning_kris
FROM kri_data
GROUP BY regulatory_domain
ORDER BY breached_kris DESC;


-- ============================================================
-- 4. Trend analysis — deteriorating KRIs
-- ============================================================
SELECT
    kri_id,
    kri_name,
    business_unit,
    regulatory_domain,
    current_value,
    threshold_warning,
    threshold_breach,
    trend,
    reporting_date
FROM kri_data
WHERE trend = 'Increasing'
  AND threshold_breach > threshold_warning
   OR trend = 'Decreasing'
  AND threshold_breach < threshold_warning
ORDER BY business_unit;


-- ============================================================
-- 5. Business unit compliance health scorecard
-- ============================================================
SELECT
    business_unit,
    COUNT(kri_id)           AS total_kris,
    SUM(CASE WHEN trend = 'Increasing'
             AND threshold_breach > threshold_warning
             THEN 1
             WHEN trend = 'Decreasing'
             AND threshold_breach < threshold_warning
             THEN 1
             ELSE 0 END)   AS deteriorating_kris,
    ROUND(
        SUM(CASE WHEN trend = 'Stable' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(kri_id), 1
    )                       AS pct_stable
FROM kri_data
GROUP BY business_unit
ORDER BY deteriorating_kris DESC;
