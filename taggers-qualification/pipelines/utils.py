"""

Utility functions for taggers validation and analysis.

Includes:
- Dataloop dataset access
- Google Sheets export/import
- Report generation
- Confusion matrix and precision/recall calculation
"""

import dtlpy as dl
import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import datetime
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
import seaborn as sns
import matplotlib.pyplot as plt
import pygsheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# -----------------------------
# Dataloop setup
# -----------------------------
if dl.token_expired():
    dl.login()

PROJECT_ID = '0c8c900e-468c-4c77-aaab-1871333f772b'
PROJECT = dl.projects.get(project_id=PROJECT_ID)
DATASET_ID = '65941df20d5a6843e79c93ed'
DATASET = PROJECT.datasets.get(dataset_id=DATASET_ID)

# -----------------------------
# Google Sheets utilities
# -----------------------------
def write_to_gsheet(service_file_path, spreadsheet_id, sheet_name, data_df):
    """
    Write a DataFrame to a Google Sheet.
    """
    gc = pygsheets.authorize(service_file=service_file_path)
    sh = gc.open_by_key(spreadsheet_id)

    try:
        sh.add_worksheet(sheet_name)
    except:
        pass

    wks = sh.worksheet_by_title(sheet_name)
    wks.clear('A1', None, '*')
    wks.set_dataframe(data_df, (1,1), encoding='utf-8', fit=True)
    wks.frozen_rows = 1
    print(f"Report updated: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

def export_gsheet(service_file_path, spreadsheet_id, sheet_name):
    """
    Export a Google Sheet worksheet into a pandas DataFrame.
    """
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(service_file_path, scope)
    client = gspread.authorize(credentials)
    sheet = client.open_by_key(spreadsheet_id)
    worksheet = sheet.worksheet(sheet_name)
    data = worksheet.get_all_values()
    return pd.DataFrame(data[1:], columns=data[0])

# -----------------------------
# Dataloop dataset utilities
# -----------------------------
def get_task(task_id):
    return DATASET.tasks.get(task_id=task_id)

def get_duplicates_items():
    """
    Return a list of duplicated item IDs in the dataset.
    """
    list_ids = [item.metadata['user']['ID'] for folder in DATASET.items.list() for item in folder]
    return [val for val in set(list_ids) if list_ids.count(val) > 1]

# -----------------------------
# Reports generation
# -----------------------------
def get_general_report_v_4(task, duplicates):
    """
    Generate general report for a task.
    """
    def get_item_link(item):
        return f'https://console.dataloop.ai/projects/{PROJECT_ID}/datasets/{DATASET_ID}/items/{item.id}'

    dict_report = []
    assig_ids = [assig.id for assig in task.assignments.list()]
    list_ids_no_dup = [x for x in set([item.metadata['user']['ID'] for folder in task.get_items() for item in folder])
                       if x not in duplicates]

    filters = dl.Filters()
    filters.resource = dl.FiltersResource.ITEM
    filters.add(field='metadata.user.ID', values=list_ids_no_dup, operator=dl.FiltersOperations.IN)
    filters.add(field='metadata.user.archived', values=True, operator=dl.FiltersOperations.NOT_EQUAL)

    items = DATASET.items.get_all_items(filters=filters)

    for item in items:
        item_id = item.metadata['user']['ID']
        entry = {
            'Item_id': item_id,
            'Crop': item.metadata['user']['Crop'],
            'Link': get_item_link(item),
            'Team': task.name.split('_')[0],
            'Date': task.name.split('_')[2],
            'Broad/Grass': item.dir.split('/')[2].capitalize(),
            'Label_ground_truth': item.metadata['user']['Subcategory_name']
        }

        assign_report = {}
        filters_assign = dl.Filters(use_defaults=False)
        filters_assign.add(field='metadata.user.ID', values=item_id)
        filters_assign.add(field='metadata.system.refs.id', values=assig_ids, operator=dl.FiltersOperations.IN)

        for folder in task.get_items(filters=filters_assign):
            for item_asg in folder:
                annotations_list = item_asg.annotations.list()
                label_annot = 'No label'
                if annotations_list:
                    label_annot = annotations_list[0].label.split(' - ')[1] if ' - ' in annotations_list[0].label else annotations_list[0].label
                assignment_id = [ref['id'] for ref in item_asg.metadata['system']['refs'] if ref['type'] == 'assignment'][0]
                annotator = DATASET.assignments.get(assignment_id=assignment_id).annotator
                assign_report[annotator] = label_annot

        entry.update(assign_report)
        dict_report.append(entry)

    df = pd.DataFrame(dict_report)
    annot_cols = df.columns[6:]
    df['num_matching_annotators'] = df.apply(lambda row: sum(row[annot_cols] == row['Label_ground_truth']), axis=1)
    df['num_non_matching_annotators'] = len(annot_cols) - df['num_matching_annotators']
    return df

def get_general_report_v_4_version2(df_report):
    """
    Reshape report for analysis.
    """
    df_melted = pd.melt(df_report[df_report.columns[:-2]],
                        id_vars=df_report.columns[:7],
                        value_vars=df_report.columns[7:],
                        var_name='Annotator',
                        value_name='Annotator_value')
    df_melted.sort_values(by=['Label_ground_truth', 'Item_id', 'Annotator'], inplace=True, ignore_index=True)
    return df_melted

# -----------------------------
# Confusion matrix and metrics
# -----------------------------
def general_confusion_matrix_2(df_report):
    labels_gt = df_report['Label_ground_truth'].unique()
    labels_taggers = np.unique(np.concatenate([df_report[col].to_numpy() for col in df_report.columns[6:-2]]))
    labels = np.union1d(labels_gt, labels_taggers)
    conf_matrix_sum = pd.DataFrame(index=labels, columns=labels, data=0)

    for col in df_report.columns[6:-2]:
        conf_matrix_sum += pd.DataFrame(confusion_matrix(df_report['Label_ground_truth'], df_report[col], labels=labels), index=labels, columns=labels)

    plt.figure(figsize=(10, 8))
    sns.heatmap(conf_matrix_sum, annot=True, fmt='d', cmap='Greens', cbar=False)
    plt.xlabel('Predicted Labels')
    plt.ylabel('True Labels')
    plt.title('Unique Confusion Matrix')
    plt.show()

def get_precision_recall(df, tested):
    """
    Calculate precision, recall, and f1-score per label.
    """
    true_labels = df['Label_ground_truth']
    predicted_labels = df[tested]
    unique_labels = df['Label_ground_truth'].unique()

    results = []
    for label in unique_labels:
        true_bin = (true_labels == label).astype(int)
        pred_bin = (predicted_labels == label).astype(int)
        results.append({
            'Label': label,
            'Count': true_bin.sum(),
            'Precision': precision_score(true_bin, pred_bin, zero_division=0),
            'Recall': recall_score(true_bin, pred_bin),
            'F1': f1_score(true_bin, pred_bin)
        })

    return pd.DataFrame(results)
