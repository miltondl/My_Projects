## Getting the count tags per category

WITH weeds_proportion_by_tags AS (
    SELECT 
        jira.orderid,
        SUM(CAST(jira.number_of_tags AS INT64)) total_weeds,
        SUM(CASE WHEN subcat_id = 158 THEN CAST(jira.number_of_tags AS INT64) ELSE 0 END) AS broad_unidentified,
        SUM(CASE WHEN subcat_id = 212 THEN CAST(jira.number_of_tags AS INT64) ELSE 0 END) AS grass_unidentified,
        SUM(CASE WHEN subcat_id != 158 AND jira.broad_grass = 'broad' THEN CAST(jira.number_of_tags AS INT64) ELSE 0 END) AS broad_identified,
        SUM(CASE WHEN subcat_id != 212 AND jira.broad_grass = 'grass' THEN CAST(jira.number_of_tags AS INT64) ELSE 0 END) AS grass_identified,
        ROUND(SUM(CASE WHEN subcat_id = 158 THEN CAST(jira.number_of_tags AS INT64) ELSE 0 END) / SUM(CAST(jira.number_of_tags AS INT64)), 2) AS broad_unidentified_perc,
        ROUND(SUM(CASE WHEN subcat_id = 212 THEN CAST(jira.number_of_tags AS INT64) ELSE 0 END) / SUM(CAST(jira.number_of_tags AS INT64)), 2) AS grass_unidentified_perc,
        ROUND(SUM(CASE WHEN jira.subcat_id != 158 AND jira.broad_grass = 'broad' THEN CAST(jira.number_of_tags AS INT64) ELSE 0 END) / SUM(CAST(jira.number_of_tags AS INT64)), 2) AS broad_identified_perc,
        ROUND(SUM(CASE WHEN jira.subcat_id != 212 AND jira.broad_grass = 'grass' THEN CAST(jira.number_of_tags AS INT64) ELSE 0 END) / SUM(CAST(jira.number_of_tags AS INT64)), 2) AS grass_identified_perc
    FROM `fake_dataset.weeds_tags` jira
    -- Sample/fake table used instead of company data
    GROUP BY jira.orderid
),


## Getting score report (weeds coverage)
## Getting score by weed_id (dict)
base AS (
    SELECT
        orderid,
        JSON_EXTRACT(statistics, '$.scoresBySpecie') AS scores_json
    FROM `fake_dataset.global_insights`
    WHERE type = 'weed'
    QUALIFY ROW_NUMBER() OVER (PARTITION BY orderid ORDER BY updated_at DESC) = 1 ## Getting the latest scores by order
),


## Table with order_id, weed_id, and score
key_value_pairs AS (
    SELECT
        orderid,
        REGEXP_REPLACE(TRIM(REGEXP_REPLACE(kv, r'^"(.*?)":.*$', r'\1')), r'\\', '') AS species,
        SAFE_CAST(REGEXP_EXTRACT(kv, r':\s*([0-9.eE+-]+)') AS FLOAT64) AS score
    FROM base,
    UNNEST(REGEXP_EXTRACT_ALL(TO_JSON_STRING(scores_json), r'"[^"]+":\s*[0-9.eE+-]+')) AS kv
), 

## Adding weed type (broad/grass)
report_by_score AS (
    SELECT
        r.orderid,
        CAST(r.species AS INT64) AS species,
        t.Broad_Grass,
        CAST(FORMAT('%.10f', r.score) AS FLOAT64) AS score
    FROM key_value_pairs r
    JOIN `fake_dataset.global_threats` t
    ON t.id = CAST(r.species AS INT64)
    WHERE r.species NOT IN ('all', 'broad', 'grass')
    ORDER BY score DESC
),


## Getting the general weed score
score_unique AS (
    SELECT
        r.orderid,
        r.species,
        CAST(FORMAT('%.10f', r.score) AS FLOAT64) AS score
    FROM key_value_pairs r
    WHERE r.species IN ('all')
    ORDER BY score DESC
),


## Table summarizing weeds coverage by broad_unidentified, broad_identified, grass_unidentified, grass_identified
weeds_coverage_insights AS (
    SELECT 
        CAST(r.orderid AS STRING) AS orderid,
        s.score AS unique_score,
        SUM(r.score) AS total_score,
        SUM(CASE WHEN r.species = 158 THEN r.score ELSE 0 END) AS broad_unidentified_coverage,
	SUM(CASE WHEN r.Broad_Grass = 'broad' and r.species != 158  THEN r.score ELSE 0 END) AS broad_identified_coverage,
        SUM(CASE WHEN r.species = 212 THEN r.score ELSE 0 END) AS grass_unidentified_coverage
        SUM(CASE WHEN r.Broad_Grass = 'broad' and r.species != 212 THEN r.score ELSE 0 END) AS grass_identified_coverage,

    FROM report_by_score r
    JOIN score_unique s ON s.orderid = r.orderid
    GROUP BY orderid, s.score
)

SELECT
    jira.key,
    jira.actual_flight_time,
    jira.delivery_date,
    jira.order_id,
    jira.organization_root_value,
    jira.organization_name',
    jira.client_name,
    jira.field_name',
    jira.field_id,
    jira.country_value as country,
    jira.instructions_value as Instructions,
    jira.crop_value, as crop
    jira.area_acres,
    jira.area_hectare,
    jira.status_name,
    COALESCE(weed.total_weeds, 0) AS total_weeds,
    COALESCE(weed.broad_unidentified, 0) AS broad_unidentified,
    COALESCE(weed.grass_unidentified, 0) AS grass_unidentified,
    COALESCE(weed.broad_identified, 0) AS broad_identified,
    COALESCE(weed.grass_identified, 0) AS grass_identified,
    weed.broad_unidentified_perc,
    weed.grass_unidentified_perc,
    weed.broad_identified_perc,
    weed.grass_identified_perc,
    wci.*
FROM `fake_dataset.jira_master` jira
LEFT JOIN weeds_proportion_by_tags weed
ON CAST(weed.orderid AS STRING) = jira.order_id
LEFT JOIN weeds_coverage_insights wci
ON CAST(wci.orderid AS STRING) = jira.order_id;
