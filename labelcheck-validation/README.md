# ✅ LabelCheck Validation  

## 📖 Description  
The **LabelCheck Validation** pipeline improves **precision tracking** in manual tagging QC workflows.  

It demonstrates how to combine **BigQuery, SQL, Python, Google Sheets, and AppSheet** (with mock/fake data) to:  
- Generate weekly samples of manual tags using proportional random sampling in SQL  
- Enable human-in-the-loop validation via AppSheet  
- Track errors made by taggers and QC teams  
- Calculate precision metrics over time  

This project uses **mock/fake data** to remain portfolio-safe.  

---

## 🚀 Why This Matters  
This pipeline supports the **feedback loop between QC teams and taggers**:  

- **Measure tagger precision** – Random weekly samples allow tracking of manual tagging accuracy.  
- **Identify QC errors** – Double-check validation highlights mistakes made by the QC team.  
- **Enable data-driven improvement** – Weekly metrics support coaching and process optimization.  
- **Demonstrate SQL expertise** – Complex queries compute proportional sample sizes, ranking, and joining metadata.  

---

## 🛠️ Key Skills Demonstrated  
- SQL data extraction, grouping, proportional sampling, and joins  
- Python data processing with pandas  
- Web scraping and patch link extraction with BeautifulSoup  
- ETL pipeline automation (Extract → Transform → Load)  
- Data cleaning & preparation for BigQuery  
- Integration of multiple tools (**BigQuery, Google Sheets, AppSheet**)  

---

# 🔎 LabelCheck Validation  

## Description  
The **LabelCheck Validation** project is a pipeline designed to improve the **accuracy measurement of manual tags** in annotation workflows.  

It combines **BigQuery (SQL)**, **Python**, **Google Sheets**, and **AppSheet** to:  
- Randomly sample manual tags each week (proportional to categories & companies).  
- Double-check QC decisions by assigning samples to validators.  
- Feed validated results back into BigQuery to calculate **true precision metrics**.  

All examples here use **fake/simulated data** to keep the project portfolio-safe.  

---

## 🚀 Why This Matters  
In annotation workflows, **QC is the “ground truth”**, but QC can also make mistakes.  
This pipeline helps by:  

- ✅ Building a **second validation layer** to measure QC accuracy.  
- ✅ Detecting **systematic QC errors** (by tag type or company).  
- ✅ Generating **weekly metrics** to track precision over time.  
- ✅ Improving feedback loops with tagging companies.  

---

## 🛠️ Key Skills Demonstrated  
- Advanced **SQL sampling logic** in BigQuery  
- Data processing & pipeline orchestration with **Python**  
- Integration between **BigQuery ↔ Google Sheets ↔ AppSheet**  
- Data validation workflows for **quality assurance**  
- Portfolio-safe project structure with **mock data**  

---

## 🔄 Project Workflow
1. Create weekly samples from BigQuery using SQL to compute proportional random sampling.
2. Export samples to Google Sheets (via Data Connectors).
3. Human validation via AppSheet – reviewers mark correct/wrong tags.
4. Update BigQuery validation table with validated data.
5. Calculate precision metrics by tagger and QC team.

Note: The Google Sheets → AppSheet step cannot be reproduced in this repo due to private connectors. Fake CSVs simulate this step.

---

## 📂 Example Table (with fake data)

| patch_id | image_id | test_name | tagger | tagger_company | manual_tag | qc_tag | validated_by | link                       |
|----------|----------|-----------|--------|----------------|------------|--------|--------------|----------------------------|
| 101      | IMG_01   | Test 1    | Alice  | Company_A      | Yes        | Yes    | Sergio       | https://fake-link/img1.png |
| 102      | IMG_02   | Test 2    | Bob    | Company_B      | No         | Yes    | Shiran       | https://fake-link/img2.png |
| 103      | IMG_03   | Test 1    | Carla  | Company_C      | Yes        | No     | Sergio       | https://fake-link/img3.png |

---

## ▶️ How to Run

1. Install dependencies:
``pip install pandas numpy requests beautifulsoup4 google-cloud-bigquery gspread oauth2client``


2. Run the Python script (main.py) step by step:
- Generate weekly samples from BigQuery (SQL query included in main.py)
- Fetch patch image links
- Simulate AppSheet validation using fake CSV
- Prepare the dataset for BigQuery upload

3. Upload the dataset to BigQuery:
```python
from google.cloud import bigquery

client = bigquery.Client(project="portfolio-project")
table_id = "portfolio_dataset.validation_table"

job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
job = client.load_table_from_dataframe(validation_report, table_id, job_config=job_config)
job.result()
```

## 📁 Repository Structure

```
labelcheck-validation/
├── notebooks/
│   └── sampling_demo.ipynb      # Demo notebook with fake data
├── sql/
│   └── weekly_sample.sql        # BigQuery SQL for sampling
├── src/
│   └── sample_generator.py      # Python script with pipeline logic
├── data/
│   └── fake_annotations.csv     # Example fake dataset
├── requirements.txt
└── README.md
```

## 📌 Notes

- Real data and credentials are not included.
- All datasets here are synthetic and created for demonstration purposes only.
- The focus is on pipeline design and data sampling logic.
