import logging 
import pandas as pd
from config import SALES_FILE, STORES_FILE, FEATURES_FILE

# EXTRACT FUNCTIONS

def load_raw_data():
    "Load raw CSVs and return three dataframes"
    
    logging.info("Will start data extraction...")
    
    sales = pd.read_csv(SALES_FILE, parse_dates=['Date'])
    logging.info(f"Sales loaded: {len(sales)} rows")
    
    stores = pd.read_csv(STORES_FILE)
    logging.info(f"Stores loaded: {len(stores)} rows")
    
    features = pd.read_csv(FEATURES_FILE, parse_dates=['Date'])
    logging.info(f"Features loaded: {len(features)} rows")
    
    logging.info("Extraction complete!!")
    
    return sales, stores, features

if __name__ == "__main__":
    sales, stores, features = load_raw_data()

 

