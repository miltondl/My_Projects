"""
Taggers Qualification Task Pipeline
-----------------------------------

This script automates the creation of a taggers qualification task:

Steps:
1. Get the golden dataset.
2. Group items by threat type.
3. Select a fixed number of items per threat for the task.
4. Create the qualification task and update item metadata.

"""

import dtlpy as dl
from datetime import datetime
import random
import numpy as np
import pandas as pd

# Login if token expired
if dl.token_expired():
    dl.login()

# -----------------------------
# Step 1: Connect to project and dataset
# -----------------------------
GOLDEN_PROJECT_ID = '0c8c900e-468c-4c77-aaab-1871333f772b'
GOLDEN_DATASET_ID = '65941df20d5a6843e79c93ed'

golden_project = dl.projects.get(project_id=GOLDEN_PROJECT_ID)
golden_dataset = golden_project.datasets.get(dataset_id=GOLDEN_DATASET_ID)

# -----------------------------
# Helper Functions
# -----------------------------

def filters_funct(list_subcat):
    """Create filters for a list of subcategories"""
    filters = dl.Filters()
    filters.resource = dl.FiltersResource.ITEM
    filters.add(field="metadata.user.Subcategory_id", values=list_subcat, operator=dl.FiltersOperations.IN)
    return filters

def item_grouped_by_threats_with_filters(dataset, filters):
    """Group items by threat using provided filters"""
    item_per_threat = {}
    for folder in dataset.items.list(filters=filters):
        for item in folder:
            sub_name = item.metadata['user']['Subcategory_name']
            item_per_threat.setdefault(sub_name, []).append(item)
    return item_per_threat

def item_grouped_by_threats_without_filters(dataset):
    """Group items by threat without specific filters (exclude archived and unwanted crops)"""
    filters = dl.Filters()
    filters.resource = dl.FiltersResource.ITEM
    filters.add(field="metadata.user.archived", values=True, operator=dl.FiltersOperations.NOT_EQUAL)
    filters.add(field="metadata.user.Crop", values="Sugarcane", operator=dl.FiltersOperations.NOT_EQUAL)
    filters.add(field="metadata.user.Subcategory_name", values="Volunteer Corn", operator=dl.FiltersOperations.NOT_EQUAL)
    
    item_per_threat = {}
    for folder in dataset.items.list(filters=filters):
        for item in folder:
            sub_name = item.metadata['user']['Subcategory_name']
            item_per_threat.setdefault(sub_name, []).append(item)
    return item_per_threat

def get_fixed_items_number(item_grouped_by_threats: dict, n_samples: int):
    """
    Select a fixed number of items per threat proportionally
    """
    total_items = sum(len(lst) for lst in item_grouped_by_threats.values())
    selected_items = []

    for threat, item_list in item_grouped_by_threats.items():
        num_samples = round((len(item_list) * n_samples) / total_items)
        selected_items.extend(random.sample(item_list, num_samples))
    return selected_items

def create_qualification_task(items_list, task_name, user_list, task_owner):
    """Create the qualification task in the dataset"""
    # Filter for selected items
    filters = dl.Filters()
    filters.resource = dl.FiltersResource.ITEM
    filters.add(field='id', values=[item.id for item in items_list], operator=dl.FiltersOperations.IN)

    # Create the task
    task = golden_dataset.tasks.create(
        filters=filters,
        task_name=task_name,
        assignee_ids=user_list,
        task_owner=task_owner,
        consensus_task_type=dl.entities.ConsensusTaskType.QUALIFICATION
    )

    # Update item metadata
    for folder in task.get_items():
        for item in folder:
            item.metadata['user'].pop('Subcategory_id', None)
            item.metadata['user'].pop('Subcategory_name', None)
            item.metadata['system'].pop('originalname', None)
            item.move(new_path=rf'/.consensus/{item.id}')
            item.update(system_metadata=True)
    
    print(f'Task "{task_name}" created successfully.')

# -----------------------------
# Step 2: Define taggers and task info
# -----------------------------
taggers_company_owner = {
    'Agteam': 'milton.delaguila@taranis.com',
    'Indivillage': 'raghunath.m@indivillage.com',
    'Apex': 'taranis-apex@aci.apexcovantage.com'
}

num_samples = 100
taggers_company = 'Indivillage'
user_list = ["guddi.sharma@indivillage.co", "minakshi.meena@indivillage.co"]
task_owner = taggers_company_owner[taggers_company]
task_name_base = f'{taggers_company}_weeds_{datetime.today().strftime("%Y-%m-%d")}'.lower()

# -----------------------------
# Step 3: Group items by threat and select images
# -----------------------------
item_grouped_by_threats = item_grouped_by_threats_without_filters(golden_dataset)
broad_threats = [
    'Pigweed', 'Common lambsquarters', 'Canada Thisltle', 'Morning Glory',
    'Black bindweed-Wild buckwheat', 'Fleabane-Horseweed', 'Dandelion',
    'Sowthisles', 'Cockleburs', 'Velvetleaf', 'Common Ragweed',
    'Waterhemp', 'Giant Ragweed', 'Nightshades'
]
grass_threats = ['Barnyard grass', 'Johnsongrass', 'Foxtail', 'Nutsedges', 'Crabgrass', 'Wheat']

item_grouped_broad = {k: item_grouped_by_threats[k] for k in broad_threats}
item_grouped_grass = {k: item_grouped_by_threats[k] for k in grass_threats}

datasets_to_process = [item_grouped_broad, item_grouped_grass]

# -----------------------------
# Step 4: Create qualification tasks for each dataset
# -----------------------------
for dt in datasets_to_process:
    broad_grass_type = dt[list(dt.keys())[0]][0].dir.split("/")[2]
    task_name_final = f'{task_name_base}_{broad_grass_type}'
    selected_items = get_fixed_items_number(dt, num_samples)
    create_qualification_task(selected_items, task_name_final, user_list, task_owner)
