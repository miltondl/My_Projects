import pandas as pd
import random


used_ids = set()

def generate_unique_id():
    unique_id = random.randint(100000, 1000000)  # Adjust the range as needed
    while unique_id in used_ids:
        unique_id = random.randint(100000, 1000000)  # Adjust the range as needed
    used_ids.add(unique_id)
    return unique_id



# Reading CSV file
df = pd.read_csv("golden_dataset_source.csv")

# Count annotators per label and ItemID
counts = df.groupby(['ItemID', 'Golden_label']).size().reset_index(name='count')

# Filter labels that have at leats 2 annotators
golden_df = counts[counts['count'] >= 2].copy()

# Remove count column
golden_df = golden_df[['ItemID', 'Golden_label']]

# Adding unique ID that will be used in the analysis
golden_df["ID"] = golden_df.apply(lambda row: generate_unique_id(), axis=1)

# In the new dataset the itemid won't be the same
golden_df["ItemID"] = golden_df.apply(lambda row: random.randint(10000, 100000), axis=1)


# Save golden dataset
golden_df.to_csv("golden_dataset.csv", index=False)
print("Golden dataset generated in data/golden_dataset.csv")

