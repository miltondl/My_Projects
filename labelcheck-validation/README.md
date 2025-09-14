# ✅ LabelCheck Validation  

## 📖 What This Project Is About  
In annotation workflows, humans (annotators) label images, and then a **QC team** reviews their work to catch mistakes. Normally, the QC team is considered the “ground truth,” but even they can make errors.  

This project, **LabelCheck Validation**, was built to **measure the accuracy of both annotators and QC members**. It provides a **simple, automated pipeline** to:  

- Randomly select samples of annotated data.  
- Have **two independent reviewers** validate the samples.  
- Detect mistakes made by **annotators and QC members**.  
- Track performance over time with clear metrics.  

All the data in this project is **fake or simulated** to keep it portfolio-safe.  

---

## 🧐 Why This Project Matters  
In real-world annotation projects:  

- **Annotators** make mistakes occasionally.  
- **QC reviewers** can also miss errors, but we usually don’t check their performance.  
- Without a proper feedback loop, it’s hard to **improve quality** or identify systematic issues.  

This pipeline solves that by:  

- ✅ Building a **second validation layer** to evaluate QC performance.  
- ✅ Identifying **patterns of errors** in both annotators and QC reviewers.  
- ✅ Generating **weekly metrics** for continuous improvement.  
- ✅ Creating a **clear feedback loop** to coach teams and improve accuracy.  

---

## 🛠️ Skills Demonstrated  

- Advanced **SQL sampling**: proportional random selection per category.  
- **Python data processing** with Pandas and NumPy.  
- **Pipeline automation**: extract → transform → load.  
- Integration of multiple tools: **BigQuery, Google Sheets, AppSheet**.  
- **Data quality tracking**: precision, error reports, confusion matrices.  
- Portfolio-safe examples using **mock/fake data**.  

---

## 🔄 How the Pipeline Works  

1. **Generate weekly samples** from BigQuery using SQL proportional sampling.  
2. **Export samples** to Google Sheets (simulating the real workflow).  
3. **Validate samples** using AppSheet: two reviewers mark correct/wrong tags.  
4. **Handle disagreements**: reviewers discuss to reach a consensus.  
5. **Update metrics** in BigQuery: track both annotator and QC performance.  

> Note: AppSheet steps are simulated with fake CSVs in this repo.  

---

## 📂 Example Table (Fake Data)

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
labelcheck_validation/
├── README.md # Project description (this file)
├── queries/
│ └── weekly_sample.sql # SQL query for weekly sampling
│ └── main.py # End-to-end Python script
├── notebooks/
│ └── sampling_demo.ipynb # Notebook demonstrating workflow
├── data/
│ ├── fake_sample.csv # Example input dataset
│ └── output_example.csv # Example pipeline output
├── docs/
│ ├── flow_diagram.png # Pipeline diagram
│ └── validation_ui.png # Screenshot of AppSheet interface
```

## 📌 Notes

- Real data and credentials are not included.
- All datasets here are synthetic and created for demonstration purposes only.
- The focus is on pipeline design and data sampling logic.
