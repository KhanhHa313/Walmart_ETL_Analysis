import os
import logging 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from utils.logging_set_up import setup_logging
from utils.config import OUTPUT_PATH, MARKDOWN_COLS


def markdown_count_storesize_impact (df):
    #See how different number of markdown at the same time have on each store size
    logging.info ("Checking impacts of different number of markdowns acorss store sizes...")

    melted = df.melt (id_vars = ['Store','Size_Category', 'Date', 'Weekly_Sales'], 
                         value_vars = MARKDOWN_COLS,
                var_name = 'Markdown_Type', value_name = 'Values')
    
    grouped_melted = melted.groupby (['Store','Size_Category', 'Date', 'Weekly_Sales'],   observed=True  )\
    .agg(Markdown_Counts = ('Values', lambda x: (x.notna()).sum()))\
    .reset_index()
    
    final = grouped_melted.groupby (['Size_Category', 'Markdown_Counts']).agg(Weekly_Sales = ('Weekly_Sales', 'median'),
                                                                        Store_Week_Obs = ('Date', 'count')).reset_index()

    
    #Define the uplift function for each store size based on their according baseline
    def uplift (row): 
        baseline = final [ (final['Size_Category'] == row['Size_Category']) & 
                           (final['Markdown_Counts'] == 0) ]['Weekly_Sales'].values[0] 
        return (row['Weekly_Sales'] - baseline)/baseline*100
    
    final['Uplift %'] = final.apply(uplift, axis = 1)

    
    #Draw the visual plot 
    logging.info ("Drawing visualisable plot...")

    plot_data = final[['Size_Category',
                       'Markdown_Counts',
                      'Uplift %']].pivot (index = 'Size_Category',
                                         columns = 'Markdown_Counts',
                                         values = 'Uplift %')

    fig, ax = plt.subplots()
    sns.heatmap (plot_data, annot = True, cmap = 'Blues')

    logging.info ("Returning results and chart...")
    logging.info ("Done the number of markdowns impact analysis!!")

    return final.set_index (['Size_Category','Markdown_Counts']), fig


# TEST RUN

if __name__ == "__main__":
    df = pd.read_csv(os.path.join(OUTPUT_PATH, 'transformed_dataset.csv'), 
                 parse_dates=['Date'])
                 
    setup_logging()
    markdown_count_storesize_impact (df)
