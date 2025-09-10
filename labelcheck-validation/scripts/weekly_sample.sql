 -- Step 1: Base data for the given week
      WITH base_data AS (
        SELECT
          taggers_company,
          test_name,
          patch_url,
          patch_id,
          image_id,
          tagger,
          FORMAT_TIMESTAMP('%Y-%W', response_insert_time) AS week
        FROM `your-project-id.your_dataset.your_table`
        WHERE FORMAT_TIMESTAMP('%Y-%W', response_insert_time) = "{week}"
      ),

      -- Step 2: Group sizes
      group_counts AS (
        SELECT taggers_company, test_name, COUNT(*) AS group_size
        FROM base_data
        GROUP BY taggers_company, test_name
      ),

      -- Step 3: Proportional allocation
      proportional_targets AS (
        SELECT
          g.taggers_company,
          g.test_name,
          g.group_size,
          ROUND(SAFE_DIVIDE(g.group_size, SUM(g.group_size) OVER ()) * {sample_size}) AS raw_target
        FROM group_counts g
      ),

      -- Step 4: Rank rows randomly within each group
      ranked_data AS (
        SELECT *,
          ROW_NUMBER() OVER (PARTITION BY taggers_company, test_name ORDER BY RAND()) AS row_num
        FROM base_data
      )

      -- Step 5: Filter rows based on proportional targets
      SELECT r.*
      FROM ranked_data r
      JOIN proportional_targets t
        ON r.taggers_company = t.taggers_company AND r.test_name = t.test_name
      WHERE r.row_num <= t.raw_target
