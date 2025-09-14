"""
report_analysis.py

Main script to generate tagger validation reports and metrics.
"""

from utils import (
    get_task,
    get_duplicates_items,
    get_general_report_v_4,
    get_general_report_v_4_version2,
    write_to_gsheet,
    general_confusion_matrix_2,
    get_precision_recall
)
import pandas as pd

# -----------------------------
# Step 1: Define task IDs
# -----------------------------
GENERAL_BROAD_TASK_1 = "67c9994cb0d280b5139252cf"
GENERAL_GRASS_TASK_1 = "67c9998e546ed5d1720d0c36"
INDIVILLAGE_TASKS = ['6810e0d6486e677094cdb670', '6810eef3486e67bbf4cdd20f']

# -----------------------------
# Step 2: Generate reports
# -----------------------------
df_list = []
df_list_v2 = []

for task_id in INDIVILLAGE_TASKS:
    task = get_task(task_id)
    duplicates_list = get_duplicates_items()
    df_report = get_general_report_v_4(task, duplicates_list)
    df_report_v2 = get_general_report_v_4_version2(df_report)
    df_list.append(df_report)
    df_list_v2.append(df_report_v2)

df_report_general = pd.concat(df_list)
df_report_general_v2 = pd.concat(df_list_v2)

# -----------------------------
# Step 3: Upload report to Google Sheets
# -----------------------------
service_file_path = r'G:\My Drive\credentials_taranis.json'
spreadsheet_id = '1ugF9jxaqM1WAxRMsoPqXzW5R-1jwNxMy6zIjt_i14GY'
sheet_name_report = 'general_report_new_report'

write_to_gsheet(service_file_path, spreadsheet_id, sheet_name_report, df_report_general_v2)

# -----------------------------
# Step 4: Generate confusion matrix
# -----------------------------
general_confusion_matrix_2(df_report_general)

# -----------------------------
# Step 5: Generate precision/recall metrics for each annotator
# -----------------------------
for annotator in df_report_general.columns[6:-2]:
    df_metrics = get_precision_recall(df_report_general, annotator)
    print(f"Metrics for {annotator}:\n", df_metrics)
