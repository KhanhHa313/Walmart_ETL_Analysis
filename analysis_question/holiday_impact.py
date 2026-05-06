import os
import logging 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from utils.logging_set_up import setup_logging
from utils.config import OUTPUT_PATH, MARKDOWN_COLS

def holiday_impact (df): 
    logging.info ("Checking the sale uplift impact from holidays acorss store sizes...")

    test = df.groupby(['Size_Category', 'Is_Holiday']).agg(Count_Obs = ('Date', 'count'),
                                                   Median_Sales = ('Weekly_Sales', 'median'))\
    .unstack().swaplevel (0,1, axis = 1)
     
    test.columns = pd.MultiIndex.from_tuples([('Non_Holiday','Count_Obs'),
                ( 'Holiday','Count_Obs'),
                ('Non_Holiday', 'Median_Sales'),
                ( 'Holiday', 'Median_Sales')])

    test[('Uplift %')] =  (test[('Holiday', 'Median_Sales')] - test[('Non_Holiday', 'Median_Sales')])\
    / test[('Non_Holiday', 'Median_Sales')] *100
    
    
    # Draw visualisable plots
    logging.info ("Drawing visualisable plot...")

    plot = test.iloc[:, [2,3]].reset_index() 
    plot.columns = plot.columns.droplevel(1)
    plot = plot.melt (id_vars = 'Size_Category',
                     value_name = 'Median_Sales',
                     var_name = 'Holidays?')

    fig, ax = plt.subplots()
    sns.barplot (x = 'Size_Category',
                y = 'Median_Sales',
                data = plot,
                hue = 'Holidays?',
                palette = 'bright')
    
    plt.xticks(rotation = 45)

    logging.info ("Returning results and chart...")
    logging.info ("Done the holiday sale uplift analysis!!")

    return test, fig

if __name__ == "__main__":
    df = pd.read_csv(os.path.join(OUTPUT_PATH, 'transformed_dataset.csv'), 
                 parse_dates=['Date'])
                 
    setup_logging()
    holiday_impact(df)