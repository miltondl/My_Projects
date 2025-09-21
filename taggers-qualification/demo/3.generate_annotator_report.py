import pandas as pd
import random

# Read the assigned tasks CSV
tasks_df = pd.read_csv("assigned_tasks_simulated.csv")
#Possible answers
labels = ["Dandelion", "Pigweed", "Sowthisles", 'Other label']

# Simulate annotator submissions
results = []

for _, row in tasks_df.iterrows():
    submitted_label = random.choice(labels)  # Getting annotator answer

    # Record the submission
    results.append({
        "ID": row["ID"],
        "Annotator": row["Annotator"],
        "Annotator_label": submitted_label,
        "ImageLink": row["ImageLink"]
    })

# Convert to DataFrame
results_df = pd.DataFrame(results)

# Save the simulated annotator results
results_df.to_csv("annotator_results_simulated.csv", index=False)

print("✅ Annotator results simulated successfully!")
print(results_df.head())
