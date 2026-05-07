import os 
import logging
import pandas as pd
from utils.logging_set_up import setup_logging
from ETL.extract import load_raw_data
from utils.config import MARKDOWN_COLS, OUTPUT_PATH  
import numpy as np
from ETL.transform import merge_tables, update_data_types, fix_negative_or_zero_markdowns, add_columns, validate_dataframe, fix_negative_or_zero_sales

def main():

    # 1. Setup
    setup_logging()

    # 2. Extract
    logging.info ("Extracting the 3 dataset...")
    sales, stores, features = load_raw_data()

    # 3. Transform
    logging.info ("Merging and tranforming the dataset")
    df = merge_tables(sales, stores, features)
    df = update_data_types(df)
    fix_negative_or_zero_markdowns(df, pct = 0.05)
    df = add_columns(df) 
    validate_dataframe(df)
    df = fix_negative_or_zero_sales(df, pct = 0.05)

    
    #4. First Load — saves processed CSV
    logging.info ("First load, saving the processed dataset in outputs folder")
    df.to_csv(os.path.join(OUTPUT_PATH, 'transformed_dataset.csv') , index = False)

    # 5. Second Load for analysis questions — interactive analysis menu
 