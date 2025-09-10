from utilis import *
from datetime import datetime


# Iterate through all files in the folder
list_dates = [datetime.strptime(file_name.rsplit("_", 1)[1].replace(".csv",""),"%Y-%m-%d")  for file_name in os.listdir(FOLDER_PATH) if 'csv' in file_name]

latest_date = max(list_dates).strftime("%Y-%m-%d")

## Get the list of dates between the day after the lastest until the day before today.
date_list = generate_date_list(latest_date)

# Generating the whole report to get the daily report for each day

for s_date in date_list:
    start_date, finish_date = get_range_day(s_date)
    download_daily_report(start_date, finish_date)

update_df = generate_updated_df()
update_google_sheet(update_df)
