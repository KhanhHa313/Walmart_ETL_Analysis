import os

# FILE PATHS
BASE_DIR = os.getcwd() # get the current working directory 

RAW_DATA_PATH = os.path.join(BASE_DIR, 'raw data')
OUTPUT_PATH = os.path.join(BASE_DIR, 'outputs')
LOG_PATH = os.path.join(BASE_DIR,"logs")

SALES_FILE = os.path.join(RAW_DATA_PATH, "sales.csv")
STORES_FILE = os.path.join(RAW_DATA_PATH, "stores.csv")
FEATURES_FILE = os.path.join(RAW_DATA_PATH, "features.csv")

# ANALYSIS COMPONENTS

MARKDOWN_COLS = [
    'MarkDown1', 'MarkDown2', 'MarkDown3', 
    'MarkDown4', 'MarkDown5'
]

USE_MEDIAN = True