# 🌱 Weeds Tagging & Coverage Analysis

## 📖 Description  
This project focuses on **measuring the quality of weed tagging** in crop imagery and understanding the **proportion of identified vs. unidentified weeds** across fields.  

Using advanced SQL queries, it combines multiple data sources to generate **weed coverage reports** for different crops, clients, and fields.  

The pipeline measures weeds in **two ways**:  
1. **Annotation counts per label** – Counts the number of manually tagged weeds for each species.  
2. **Weed coverage score** – Calculates coverage per weed automatically based on field-level annotations (`global_insights`).  

It produces a **comprehensive report** linking weed counts, coverage scores, and field metadata, helping identify areas with **low identification rates** and enabling targeted re-annotation to improve dataset quality.  

All examples here use **realistic data**, but the workflow can be adapted for **portfolio-safe datasets**.

---

## 🚀 Why This Matters  
Accurate weed tagging is essential for both **AI model training** and **field-level decision-making**:  

- ✅ **Evaluate tagger performance** – Detect where weeds are being missed or mislabeled.  
- ✅ **Understand field coverage** – Identify fields or crops with high proportions of unidentified weeds.  
- ✅ **Enable targeted re-annotation** – Focus on fields with low identification rates to improve dataset quality.  
- ✅ **Support agronomy teams** – Provide actionable metrics for crop management and reporting.  

---

## 🛠️ Key Skills Demonstrated  
- Writing **modular SQL queries** with CTEs (Common Table Expressions)  
- Extracting and parsing nested data from **JSON fields**  
- Conditional aggregation (`CASE WHEN`) to calculate metrics  
- Using **window functions** (`ROW_NUMBER() OVER`) for deduplication  
- Joining multiple tables for integrated reporting  
- Calculating **percentages and coverage scores** across clients, crops, and flights  

---

## 📊 Use Case / Workflow  
1. Measure the proportion of unidentified weeds in **two ways**:  
   - By counting the number of annotations per label.  
   - By calculating the **weed coverage score** automatically.  
2. Analyze results **by client, organization, country, crop, and flight date**.  
3. Filter fields with **low unidentified proportions** to understand gaps.  
4. Optionally **re-annotate** these fields to increase identification quality.  
5. Generate reports to track improvements over time.
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
