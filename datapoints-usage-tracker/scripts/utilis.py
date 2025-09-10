import dtlpy as dl
from datetime import datetime, timedelta

import os
import pandas as pd

from sqlalchemy import create_engine
import gspread
from oauth2client.service_account import ServiceAccountCredentials

if dl.token_expired():
    dl.login()

token_id = dl.token()
import requests



# Replace with your actual API key and account ID
API_KEY = token_id
ACCOUNT_ID = 'ACCOUNT_ID'

# Define the folder path
FOLDER_PATH = r"folder_path"

import pygsheets
def write_to_gsheet(service_file_path, spreadsheet_id, sheet_name, data_df):
    """
    this function takes data_df and writes it under spreadsheet_id
    and sheet_name using your credentials under service_file_path
    """
    gc = pygsheets.authorize(service_account_file=service_file_path)
    sh = gc.open_by_key(spreadsheet_id)
    try:
        sh.add_worksheet(sheet_name)
    except:
        pass
    wks_write = sh.worksheet_by_title(sheet_name)
    wks_write.clear('A1',None,'*')
    # Replace None values in the DataFrame with empty strings
    wks_write.set_dataframe(data_df, (1,1), encoding='utf-8', fit=True)
    wks_write.frozen_rows = 1
    return (print("Report updated", datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
    


def download_daily_report(start_date, end_date):

    # Construct the API endpoint
    url = f'https://gate.dataloop.ai/api/v1/billing/account/{ACCOUNT_ID}/csv'
    params = {
        'startDate': start_date,
        'endDate': end_date,
        'monthly': True
    }

    # Set up the headers with the API key
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    # Make the GET request
    response = requests.get(url, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Write the CSV content to a file
        file_path = os.path.join(FOLDER_PATH, f'usage_report_{start_date}.csv')
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f'CSV report has been saved as usage_report_{start_date}.csv')
    else:
        print(f'Failed to retrieve the report: {response.status_code} - {response.text}')



def generate_updated_df():

    # Define the folder path

    # Create an empty list to store DataFrames
    dataframes = []

    # Iterate through all files in the folder
    for file_name in os.listdir(FOLDER_PATH):
        # Check if the file is a CSV file
        if file_name.endswith(".csv"):
            # Extract the date from the filename (assuming 'usage_report_YYYY-MM-DD' format)
            date = file_name.split('_')[-1].replace('.csv', '')
            
            # Read the CSV file into a DataFrame
            file_path = os.path.join(FOLDER_PATH, file_name)
            df = pd.read_csv(file_path)
            
            # Add a new column with the extracted date
            df['date'] = date
            
            # Append the DataFrame to the list
            dataframes.append(df)

    # Concatenate all DataFrames in the list into one
    combined_df = pd.concat(dataframes, ignore_index=True)

    # # combined_df
    combined_df['date'] = pd.to_datetime(combined_df['date'])
    combined_df = combined_df.sort_values(by=['Project Name', 'date'])

    combined_df["Max Managed Items Diff"] = combined_df.groupby("Project Name")["Max Managed Items"].diff()
    combined_df["Max Annotations Diff"] = combined_df.groupby("Project Name")["Max Annotations"].diff()
    combined_df["Daily Validated Items"] = combined_df['Max Managed Items Diff'].apply(lambda x: x if x > 0 else 0)
    combined_df["Daily Validated Annot"] = combined_df['Max Annotations Diff'].apply(lambda x: x if x > 0 else 0)
    combined_df["Total DP"] = combined_df["Daily Validated Items"] + combined_df["Daily Validated Annot"]
    return combined_df


def update_google_sheet (df):

    service_file_path = r'credentials_taranis.json'
    spreadsheet_id = '1EW6IfZWtbad5fnOTZc7Cl58r-fh2kZtvhTcHuro7Xd8'
    sheet_name = 'Dataloop Report Usage'
    table_name = 'Combined report'

    write_to_gsheet(service_file_path,spreadsheet_id, sheet_name, df)



def generate_date_list(start_date: str) -> list:
    # Convert the input date string to a datetime object
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    
    # Get today's date
    yesterday = datetime.today() - timedelta(days=1)
    
    # Create an empty list to store the dates
    date_list = []
    
    # Iterate and add each date to the list, from start_date + 1 day until the day before today
    current_date = start_date + timedelta(days=1)
    while current_date < yesterday:
        date_list.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    
    return date_list

def get_range_day(start_date: str) -> str:
    start_date_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_datatime = start_date_datetime + timedelta(days=1)
    end_time = end_date_datatime.strftime("%Y-%m-%d")
    return (start_date, end_time)