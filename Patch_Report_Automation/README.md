# 📊 Automated Annotation Tracker  

## Description  
The **Automated Annotation Tracker** is a pipeline that automates the processing of annotation reports to improve **visibility** and **feedback** in quality control workflows.  

It demonstrates how to combine **BigQuery**, **BeautifulSoup**, and **Dataloop APIs** (simulated with mock data) to:  
- Make patch images accessible to external partners  
- Identify taggers responsible for annotations  
- Provide feedback loops to improve annotation quality  

This project is built with **mock/fake data** to remain portfolio-safe.  

---

## 🚀 Why This Matters  
This tool supports the **feedback loop between QC teams and external tagging companies**:  

- ✅ **Make patch images accessible** – Patches stored behind VPN in Google Cloud are made visible by scraping their direct image links. External taggers can now review the mistakes flagged by QC.  
- ✅ **Track taggers’ responsibility** – For each patch, the pipeline identifies which tagger(s) annotated the source image and when it was marked as completed.  
- ✅ **Support training & accountability** – Since images can be completed multiple times by different taggers, the system builds a tagger-history dictionary. This helps companies see **who contributed** and provide targeted coaching where errors occur.  

---

## 🛠️ Key Skills Demonstrated  
- Python data processing with **pandas**  
- Web scraping and link extraction with **BeautifulSoup**  
- API integration (mock Dataloop dataset interaction)  
- ETL pipeline automation (Extract → Transform → Load)  
- Data cleaning & preparation for BigQuery upload  

---

## 🔄 Project Workflow  
1. **Fetch patch reports** from a simulated BigQuery table.  
2. **Extract patch image links** from AppSheet-like pages using BeautifulSoup.  
3. **Identify taggers** from simulated Dataloop metadata (name + completion date).  
4. **Enrich the dataset** with image path, tagger info, and correct labels.  
5. **Upload cleaned data to BigQuery** (mocked in this portfolio example).  

---

## 📂 Example Table (with fake data)  

| patch_id | image_id | annotation_item_ids | tagger        | tagger_company | correct_label | date       | link                        |  
|----------|----------|----------------------|---------------|----------------|---------------|------------|-----------------------------|  
| 101      | IMG_01   | [“ann1”]            | Alice         | Company_A      | Weed          | 2025-09-06 | https://fake-link/img1.png  |  
| 102      | IMG_02   | [“ann2”]            | Bob           | Company_B      | Disease       | 2025-09-06 | https://fake-link/img2.png  |  
| 103      | IMG_02   | [“ann3”]            | Carla, David  | Company_C      | Crop          | 2025-09-07 | https://fake-link/img2.png  |  

---

## ▶️ How to Run  

1. Install the dependencies:  
```bash
pip install dtlpy pandas requests beautifulsoup4 google-cloud-bigquery
