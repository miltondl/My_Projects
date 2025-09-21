import pandas as pd
import random

# Read the golden dataset
golden_df = pd.read_csv("golden_dataset.csv")

# List of annotators or QC members to assign tasks
annotators = ["Alice", "Bob", "Carla", "David"]

# Number of items to assign per annotator
samples_per_annotator = 5

# Create an empty list to store task assignments
tasks = []


# Take a random sample of items for the task
sample = golden_df.sample(n=samples_per_annotator, replace=False)

# TaskID
task_id = random.randint(100000, 999999)


# Creating task

for _, row in sample.iterrows():
# Simulate task assignment (like Dataloop)
    for annotator in annotators:
        # Take a random sample of items for this annotator
        sample = golden_df.sample(n=samples_per_annotator, replace=False)
    
        # Generate a demo image link (simulated)
        image_link = f"https://demo-images.com/{row['ItemID']}.jpg"
        # Append task info to the tasks list
        tasks.append({
            "ID": row["ID"],
            "TaskID": task_id,
            "ItemID": random.randint(10000, 100000), # Each item in the task has a new ItemID,
            "Annotator": annotator,
            "Status": "Open",  # Simulate task status
            "ImageLink": image_link
        })

# Convert tasks list to a DataFrame
tasks_df = pd.DataFrame(tasks)

# Save the simulated assigned tasks to CSV
tasks_df.to_csv("assigned_tasks_simulated.csv", index=False)

print("✅ Tasks simulated successfully!")
print(tasks_df.head())