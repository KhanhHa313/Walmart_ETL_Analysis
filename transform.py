import logging
import pandas as pd
from logging_set_up import setup_logging
from extract import load_raw_data
from config import MARKDOWN_COLS 
import numpy as np

 
# TRANSFORM FUNCTIONS
def merge_tables(sales, stores, features):
    #Group the department sales in sales table by store and dates
    logging.info("Proceed to merging the three tables")
    sales = sales.groupby(['Store', 'Date'])['Weekly_Sales'].sum ().reset_index()
    
    #Merge the table based on the dates available in the sales data, main metrics for this report
    merged_df = sales.merge (features, on = ['Store', 'Date'], how = 'left')
    merged_df = merged_df.merge (stores, on = 'Store', how = 'left')

    #Drop the 'Type' column as this will not be included in this analysis due to its vague idea
    merged_df = merged_df.drop ('Type', axis = 1)

    #Also drop the CPI, Unemployment column as these are not focus of these projects
    merged_df = merged_df.drop (['CPI', 'Unemployment'], axis = 1)

    #Rename columns for consistency 
    merged_df = merged_df.rename (columns = {'IsHoliday': 'Is_Holiday'})

    logging.info("Data merged successfully!!")
    return merged_df


def update_data_types(df):
    #Update all the dtypes across all the columns for later operations on them 

    logging.info("Proceed to updating the data type for the merged data frame")

    df['Store'] = df['Store'].astype (int)
    df['Is_Holiday'] = df['Is_Holiday'].astype (bool)

    float_cols = ['Size', 'Weekly_Sales'] + MARKDOWN_COLS
    for i in float_cols:
        df[i] = pd.to_numeric (df[i])

    logging.info("Data astype complete!!")
    print (df.info())
    return df


def fix_negative_or_zero_markdowns(df, pct = 0.05):
    #Quick investigations reveal some negative and 0 mardown values which are supposed to have either Null or postive values
    #Therefore, these functions will check the number of these 'problematic' problems, if its more than 5% of total number of columns
    #this will return errors and ask to recheck the data and import again, if not, converted to Null values
    #The default is 5% but can change according to users
    logging.info("Proceed to looking into negative and zero markdown data")

    total_records = len (df) 
    neg_mds = (df[MARKDOWN_COLS] <= 0).sum()
    n = len (neg_mds)

    #Checking the number of 0 or negative markdown values for each type of markdown
    for i in neg_mds.index:
        if neg_mds[i] > total_records*pct:
            n = n-1
            logging.warning(f'{i} has more than {pct*100}% of negative markdown')

    #Print out comments based on the results of each function 
    if n == len(MARKDOWN_COLS):
        logging.info(f'There is no markdown having more than {pct*100}% of negative')
        logging.info('The negatives have then been converted to NaN')

        df[MARKDOWN_COLS] = df[MARKDOWN_COLS].mask(
            df[MARKDOWN_COLS] <= 0, np.nan)

        logging.info("Negative and Zero markdown data records have been converted to NaN")

        
    elif n <= len(MARKDOWN_COLS)/2: 
        logging.warning('Please check the data before proceeding')
        
    else:
        logging.info(f'There is less than half of markdown types having more than {pct*100}% of negative each')
        logging.info('The negative will then still be converted to NaN unless stated otherwise')
        df[MARKDOWN_COLS] = df[MARKDOWN_COLS].mask(
            df[MARKDOWN_COLS] <= 0, np.nan)
        logging.info("Negative and Zero markdown data records have been converted to NaN!!")

    return None

def add_columns(df): 
    #Find the total markdown 
    logging.info("Adding the total markdown column")

    df['Total_Markdown'] = df[MARKDOWN_COLS].sum(axis = 1)

    #Create the binary flag for the markdown for each week 
    logging.info("Adding the markdown flag column")
    df['Has_Markdown'] = df['Total_Markdown'] > 0

    #Add quarter and year columns 
    logging.info("Adding date component columns")
    df.insert(2, 'Year', df['Date'].dt.year) 
    df.insert(3, 'Quarter', df['Date'].dt.quarter) 
    df.insert(4, 'Month', df['Date'].dt.month) 
    

    #Add size category column
    logging.info("Adding the store size category column")
    size_buckets = [0, 50000, 100000,150000, 200000, np.inf]
    size_bucket_labels = ['Less than 50k',
                          'Between 50k and 100k',
                         'Between 100k and 150k',
                         'Between 150k and 200k',
                          'More than 200k']
    df['Size_Category'] = pd.Categorical (pd.cut (df['Size'], bins = size_buckets, 
                                     labels = size_bucket_labels),
                                        categories = size_bucket_labels,
                                        ordered = True,
                                         )
    logging.info("Adding the columns successfully!!")

    return df


def validate_dataframe(df):
    #To facilitate later analysis, this funtion is for checking whether our data at the time have all the needed columns 
    logging.info("Checking all the required columns for the analysis")

    required_columns = [
        'Store',
        'Date',
        'Year',
        'Quarter',
        'Month',
        'Weekly_Sales',
        'Is_Holiday', 
        'Has_Markdown',
        'Total_Markdown',
        'Size',
        'Size_Category',
    ] + MARKDOWN_COLS
    
    missing = [col for col in required_columns if col not in df.columns]
    
    if missing:
        logging.warning(f"Missing columns: {missing}")
    else:
        logging.info("Dataframe validated - all required columns present")

# TEST RUN

if __name__ == "__main__":
    setup_logging()
    sales, stores, features = load_raw_data()
    df = merge_tables(sales, stores, features)
    df = update_data_types(df)
    fix_negative_or_zero_markdowns(df, pct = 0.05)
    df = add_columns(df) 
    validate_dataframe(df)
    
    print(f"Shape of dataframe: {df.shape}")
    print(f"Columns of dataframe: {df.columns.tolist()}")