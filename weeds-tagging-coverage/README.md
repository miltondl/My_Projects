# 🌱 Weeds Tagging & Coverage Analysis

## Description
This project demonstrates **advanced SQL analysis** on crop imagery annotation data.  

It combines multiple data sources to evaluate **weed tagging performance** and **weed coverage scores** across fields, crops, and clients.  

The SQL query:  
- Calculates counts of manually tagged weeds in **different categories**: `broad_unidentified`, `grass_unidentified`, `broad_identified`, `grass_identified`.  
- Computes **coverage scores** for each weed species using JSON insights from `global_insights`.  
- Produces a **comprehensive report** by order, linking tag counts, scores, and field metadata.  

This project uses **realistic examples** but can be adapted to portfolio-safe datasets.  

---

## Why This Matters
Tracking weeds accurately is essential for:  

- ✅ **Quality control of manual annotations** – Identify areas where taggers may mislabel or miss weeds.  
- ✅ **Field coverage insights** – Understand which fields have higher proportions of unidentified weeds.  
- ✅ **Data-driven decision-making** – Support agronomy teams and crop consultants with actionable metrics.  

---

## Key Skills Demonstrated
- SQL **CTEs** (Common Table Expressions) for modular query building  
- **JSON extraction** (`JSON_EXTRACT`) and regex parsing for nested insights  
- Conditional aggregation with `CASE WHEN`  
- Window functions (`ROW_NUMBER() OVER`) for deduplication  
- Joins across multiple tables for integrated reporting  
- Calculating percentages and coverage metrics  

---

## Project Workflow
1. **Weed counts**: Aggregate the number of tags per category from `Eti_Images_Crops_Subcat_Jira_Master_Table`.  
2. **Coverage scores**: Extract species-level scores from JSON stored in `global_insights`.  
3. **Join metadata**: Combine tag counts and coverage scores with project, field, and crop information.  
4. **Compute derived metrics**: Percentages for identified/unidentified weeds and broad/grass categories.  
5. **Produce final report**: A comprehensive dataset per order with both counts and coverage scores.  

---

## Example Output

| order_id | total_weeds | broad_unidentified | grass_unidentified | broad_identified | grass_identified | broad_unidentified_perc | grass_unidentified_perc | broad_identified_perc | grass_identified_perc | unique_score | total_score | total_broad_pressure | broad_158_pressure | total_grass_pressure | grass_212_pressure |
|----------|------------|------------------|------------------|----------------|----------------|-----------------------|-----------------------|---------------------|---------------------|--------------|------------|-------------------|-----------------|-------------------|-----------------|
| 729783   | 1631       | 1141             | 65               | 60             | 365            | 0.70                  | 0.04                  | 0.04                | 0.22                | 0.0338       | 0.0338     | 0.0245            | 0.0233          | 0.0092            | 0.0014          |

---

## How to Use
1. **Run the query in BigQuery** against the `BI_MASTER_TABLES` and `BI_POSTGRES` datasets.  
2. Adjust category IDs (`158`, `212`) to match your internal tagging taxonomy.  
3. Optionally, export the results to CSV or visualize in **Looker Studio** for further reporting.  

---

## Potential Enhancements
- Add **dashboard visualizations**: pie charts for tag proportions, time-series coverage charts, heatmaps by field.  
- Make it **parameterized**: filter by date range, crop type, or organization.  
- Store intermediate CTE results as **views** for faster access on large datasets.  
