"""
Weekly Label Sampling Pipeline
------------------------------
This script extracts weekly samples of manual tags from BigQuery,
retrieves patch images from provided URLs, and uploads the sample
to a validation table in BigQuery (or mock equivalent).
"""

from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
from google.cloud import bigquery
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize BigQuery client (use your GCP project)
bq_client = bigquery.Client(project="your-project-id")


def get_patches_report(week: str = None, sample_size: int = 400) -> pd.DataFrame:
    """
    Query BigQuery to extract a weekly proportional sample of manual tags.

    Args:
        week (str): Year-week format (e.g., "2025-15"). Defaults to current week.
        sample_size (int): Total number of samples across groups.

    Returns:
        pd.DataFrame: Sampled tag records.
    """
    if not week:
        week = datetime.now().strftime("%Y-%W")

    query = f"""
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
    """

    logging.info(f"Running BigQuery for week {week}...")
    return bq_client.query(query).to_dataframe()


def fetch_patch_images(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fetch patch image links from patch_url in the DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame with 'patch_url'.

    Returns:
        pd.DataFrame: Same DataFrame with 'link' column containing image URL.
    """
    results = []
    for _, row in df.iterrows():
        url = row.get("patch_url")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            image_url = [img["src"] for img in soup.find_all("img")][0]

            row_dict = row.to_dict()
            row_dict["link"] = image_url
            results.append(row_dict)

        except Exception as e:
            logging.warning(f"Failed to fetch image for patch {row.get('patch_id')}: {e}")

    output = pd.DataFrame(results)

    # Optional cleanup: normalize test_name
    if "test_name" in output.columns:
        output["test_name"] = output["test_name"].str.replace(" samples", "", regex=False)

    return output


def upload_to_bigquery(df: pd.DataFrame, table_id: str, mode: str = "WRITE_TRUNCATE"):
    """
    Upload DataFrame to BigQuery.

    Args:
        df (pd.DataFrame): DataFrame to upload.
        table_id (str): Full BigQuery table ID (project.dataset.table).
        mode (str): Write disposition ("WRITE_TRUNCATE" or "WRITE_APPEND").
    """
    job_config = bigquery.LoadJobConfig(write_disposition=mode)
    job = bq_client.load_table_from_dataframe(df, destination=table_id, job_config=job_config)
    job.result()
    logging.info(f"Table {table_id} uploaded successfully. Rows: {len(df)}")


if __name__ == "__main__":
    # Example run
    week = "2025-15"  # Replace with dynamic or CLI argument if needed
    df_samples = get_patches_report(week=week, sample_size=400)
    df_with_links = fetch_patch_images(df_samples)
    upload_to_bigquery(df_with_links, "your-project-id.your_dataset.sample_validation_table")
