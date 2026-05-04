import logging
import pandas as pd
from logging_set_up import setup_logging
from extract import load_raw_data
from config import MARKDOWN_COLS 

 
# TRANSFORM FUNCTIONS
def merge_tables(sales, stores, features):
    #Group the department sales in sales table by store and dates
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
    df['Store'] = df['Store'].astype (int)
    df['Is_Holiday'] = df['Is_Holiday'].astype (bool)

    float_cols = ['Size', 'Weekly_Sales'] + MARKDOWN_COLS
    for i in float_cols:
        df[i] = pd.to_numeric (df[i])

    logging.info("Data astype complete!!")
    print (df.info())
    return df



# TEST RUN

if __name__ == "__main__":
    setup_logging()
    sales, stores, features = load_raw_data()
    df = merge_tables(sales, stores, features)
    df = update_data_types(df)
    # df = fix_negative_markdowns(df)
    # df = add_feature_flags(df)
    # validate_dataframe(df)
    print(f"Shape of dataframe: {df.shape}")
    print(f"Columns of dataframe: {df.columns.tolist()}")