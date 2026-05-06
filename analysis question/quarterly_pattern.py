import logging 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.config import SALES_FILE, STORES_FILE, FEATURES_FILE
from utils.logging_set_up import setup_logging

def quarterly_sales_pattern(df):
    #How do sales move across quarters?
    logging.info ("Checking the quarterly sale patterns across years of all stores...")
    quarter_sales = df.groupby(['Year', 'Quarter'])['Weekly_Sales'].agg(['median']).unstack()
    quarter_sales.columns = ['Q1', 'Q2', 'Q3', 'Q4'] 

    
    #Draw visualisable plots
    melted = quarter_sales.reset_index().melt (id_vars = 'Year', 
                                 value_vars = quarter_sales.columns,
                                  value_name = 'Median Sales',
                                  var_name = 'Quarter'
                                 )
    
    fig, ax = plt.subplots()
    sns.lineplot (x = 'Quarter', 
              y = 'Median Sales', 
              data = melted,
             hue = 'Year', palette='bright')
    plt.ticklabel_format(style='plain', axis='y')
    return quarter_sales, fig 

# TEST RUN

if __name__ == "__main__":
    setup_logging()
    quarterly_sales_pattern(df)

