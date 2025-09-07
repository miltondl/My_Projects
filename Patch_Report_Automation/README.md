# Automated Annotation Tracker

## Description
This project demonstrates an **automated pipeline to process patch-level data**, extract image links, and assign taggers. It simulates integration with BigQuery and Dataloop-like annotation platforms using **mock data** to keep the project portfolio-safe.  

The pipeline is designed to show your skills in **data processing, ETL automation, and API integration** without exposing any sensitive company data.

---

## Key Skills Demonstrated
- Python data processing with **pandas**  
- Web scraping and data extraction using **BeautifulSoup**  
- API integration (simulated Dataloop dataset interaction)  
- ETL pipeline automation  
- Handling and cleaning datasets for analysis  

---

## Project Workflow
1. **Fetch patch reports** from a simulated BigQuery table.  
2. **Extract image links** for each patch using a mock AppSheet-like process.  
3. **Assign taggers** to patches based on annotation item IDs.  
4. **Clean and prepare the dataset** for further analysis or reporting.  
5. Optional: Upload processed data to BigQuery (mock example included).  

---

## How to Run
1. Install the dependencies:
```bash
pip install dtlpy pandas requests beautifulsoup4
