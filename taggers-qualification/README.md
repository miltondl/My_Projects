# 🎯 Taggers Qualification

**End-to-end pipeline for evaluating annotation quality and performance.**  

---

## ❓ Why This Project Matters

In many data-driven projects, the **accuracy of human annotations** directly impacts the performance of AI models and the quality of insights. This project addresses that challenge by providing a **reproducible and automated pipeline** to:

- Ensure a **high-quality “golden dataset”** for benchmarking.
- Evaluate annotators consistently and fairly.
- Identify **patterns of errors or inconsistencies** in tagging.
- Generate actionable reports for improving both **human and AI workflows**.

The techniques and workflows demonstrated here are **transferable to any domain** where human labeling or validation is critical, such as document classification, image/video annotation, or quality control in datasets.

---

## 🛠️ Core Workflow

The project consists of **three main steps**:

### 1️⃣ Build Golden Dataset
- Extract images and metadata from existing AI datasets.
- Assign **unique IDs** and organize images into a “golden” dataset for evaluation.
- Ensures a clean and controlled dataset for benchmarking human or AI annotations.

**Key skills:** Data wrangling, APIs, automation, dataset versioning.

---

### 2️⃣ Create Qualification Tasks
- Select images for each tagger based on labels and sampling strategy.
- Create controlled annotation tasks in Dataloop for specific tagger companies or users.
- Updates metadata and file paths to ensure consistency.

**Key skills:** Python scripting, random sampling, workflow automation, API usage.

---

### 3️⃣ Analyze Results
- Aggregate annotation results and compare them against the golden dataset.
- Generate **confusion matrices**, **precision/recall per label**, and error reports.
- Outputs can be exported to Google Sheets for dashboards or reporting.

**Key skills:** Data analysis, Pandas, NumPy, visualization (Matplotlib, Seaborn), reporting automation.

---

## 📂 Project Structure

```
taggers-qualification/
│
├── data/
│   ├── notebooks/
│   │   └── weeds_report_analysis.ipynb
│   └── reports/
│       ├── general_report_new_report.csv
│       └── general_report_new_report_2.csv
│
├── pipelines/
│   ├── 1.building_golden_dataset.py
│   ├── 2.create_task.py
│   ├── 3.report_analysis.py
│   └── utils.py
│
├── README.md
```

---

## 🚀 Tech & Tools
- **Languages:** Python  
- **Data:** Pandas, NumPy  
- **Databases & APIs:** Dataloop API, Google Sheets API  
- **Visualization:** Matplotlib, Seaborn  
- **Workflow:** Automation scripts, data pipelines 
