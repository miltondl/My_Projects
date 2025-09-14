# ======================================
# Taggers Qualification Pipeline - Step 1
# Building Golden Dataset
# ======================================

import dtlpy as dl
import os
import random
from tqdm import tqdm

# -----------------------------
# Authentication
# -----------------------------
if dl.token_expired():
    dl.login()


# -----------------------------
# Helper Functions
# -----------------------------
def get_project_dataset(project_id: str, dataset_id: str):
    """
    Returns the project and dataset objects
    """
    project = dl.projects.get(project_id=project_id)
    dataset = project.datasets.get(dataset_id=dataset_id)
    return project, dataset


def create_weed_filter(weed_name: str):
    """
    Create Dataloop filter for a specific weed
    """
    weed_name = weed_name.title()
    filters = dl.Filters()
    filters.add(field="metadata.user.Subcategory_name", values=weed_name)
    filters.add(field="metadata.user.archived", values=True, operator=dl.FiltersOperations.NOT_EQUAL)
    return filters


def download_items(dataset, filters, local_path: str):
    """
    Download all items matching the filters to a local folder
    """
    os.makedirs(local_path, exist_ok=True)
    for item in dataset.items.get_all_items(filters=filters):
        item.download(local_path)


def upload_images_to_dataset(dataset, folder_path: str):
    """
    Upload images from local folder to the dataset, generating unique IDs and preserving metadata
    """
    used_ids = set(item.metadata['user']['ID'] for folder in dataset.items.list() for item in folder)
    
    for root, dirs, files in os.walk(folder_path):
        for file_name in tqdm(files):
            file_path = os.path.join(root, file_name)
            
            # Extract remote path and metadata from filename
            remote_path = file_path.split("\\", 6)[6].rsplit("\\", 1)[0]
            name_threat = file_path.rsplit("\\", 2)[1].split(' - ')
            subcategory_id = name_threat[0]
            subcategory_name = name_threat[1]
            original_dataset_name = file_path.split('\\')[5]
            
            # Generate unique ID
            unique_id = random.randint(100000, 1000000)
            while unique_id in used_ids:
                unique_id = random.randint(100000, 1000000)
            used_ids.add(unique_id)
            
            # Upload item
            dataset.items.upload(
                local_path=file_path,
                remote_path='Weeds\\' + remote_path,
                item_metadata={
                    "user": {
                        "ID": unique_id,
                        "Subcategory_id": subcategory_id,
                        "Subcategory_name": subcategory_name,
                        "origin": original_dataset_name
                    }
                }
            )


# -----------------------------
# Main Pipeline Execution
# -----------------------------
if __name__ == "__main__":
    # Download from existing AI dataset

    ai_project_id = '0c8c900e-468c-4c77-aaab-1871333f772b'
    ai_dataset_id = '65941df20d5a6843e79c93ed'
    ai_project, ai_dataset_gd = get_project_dataset(ai_project_id, ai_dataset_id)

    weed_name = "weed_to_add"
    local_download_path = fr'C:/Users/Administrator/Desktop/{weed_name}'
    filters = create_weed_filter(weed_name)
    download_items(ai_dataset_gd, filters, local_download_path)

    # Upload to golden dataset
    golden_project_id = 'golden_project_id'
    golden_dataset_id = 'golden_dataset_id'
    project_golden, dataset_golden = get_project_dataset(golden_project_id, golden_dataset_id)

    upload_images_to_dataset(dataset_golden, folder_path=local_download_path)
