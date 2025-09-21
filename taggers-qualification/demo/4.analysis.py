import pandas as pd


assigned_df = pd.read_csv("annotator_results_simulated.csv")
golden_dataset_df = pd.read_csv("golden_dataset.csv")



merged_df = assigned_df.merge(golden_dataset_df, on="ID", how="left")

#Reorder columns
new_column_order = ["ID", "Golden_label", "Annotator_label", "Annotator", "ImageLink"]
report_final = merged_df[new_column_order]

report_final.to_csv('analysis_reports/final_report.csv', index=False)

# print(report_final.head())



import pandas as pd
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Load your analysis report (already merged with golden labels)
# df = pd.read_csv("annotator_analysis_report.csv")


df = report_final
# Compute confusion matrix
cm = confusion_matrix(df["Golden_label"], df["Annotator_label"], labels=df["Golden_label"].unique())

# Plot confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=df["Golden_label"].unique())
disp.plot(cmap="Blues", xticks_rotation=45)

plt.title("Confusion Matrix - Annotators vs Golden Dataset")
plt.tight_layout()

# Save as PNG
plt.savefig("analysis_reports/confusion_matrix.png", dpi=300)
plt.show()
plt.close()

