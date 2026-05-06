import os
import logging 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from utils.logging_set_up import setup_logging
from utils.config import OUTPUT_PATH

def markdown_uplift_analysis_store (df):
    #Group store based on each store and markdown as initial discovery show that smaller store have less markdown so 
    #group by stores help to avoid skew the data
    logging.info ("Checking the markdown sales uplift across all stores...")
    
    store_markdown = df.groupby(['Store', 'Has_Markdown'])['Weekly_Sales'].agg(['median','count']).unstack()
    store_markdown.columns = ['No_Markdown_Median','Markdown_Median',
                           'No_Markdown_Count','Markdown_Count']
    
    store_markdown ['Uplift %'] = (store_markdown ['Markdown_Median'] - store_markdown ['No_Markdown_Median'])\
                                                                        / store_markdown ['No_Markdown_Median']*100


    #Draw visualisable plots
    #As there are 45 stores hence the plot will show the top 5 and worst 5 stores 
    logging.info ("Drawing visualisable plot...")

    plot_data = store_markdown.reset_index() 
    top5 = plot_data.sort_values ('Uplift %', ascending = False).head (5)
    tail5 = plot_data.sort_values ('Uplift %', ascending = True).head (5)

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    x1 = range(len(top5))
    x2 = range(len(tail5))

    axes[0].bar(x1, top5['Uplift %'], color = 'blue')
    axes[0].set_xticks(x1)
    axes[0].set_xticklabels(top5['Store'])
    axes[0].set_xlabel ('Stores')
    axes[0].set_title('Top five stores in with highest Uplift percents')
    
    axes[1].bar(x2, tail5['Uplift %'], color = '#ff7f0e')
    axes[1].set_xticks(x2)
    axes[1].set_xticklabels(tail5['Store'])
    axes[1].set_xlabel ('Stores')
    axes[1].set_title('Top five stores in with lowest Uplift percents')

    plt.tight_layout()

    logging.info ("Returning results and chart...")
    logging.info ("Done the store-level markdown uplift analysis!!")

    return store_markdown.sort_values ('Uplift %', ascending = False), fig
 

def markdown_uplift_analysis_store_size (df):
    #As the size each store is unique to itself so I will divide into each category for this analysis question 
    logging.info ("Checking the markdown sales uplift across all stores...")

    size_buckets = [0, 50000, 100000,150000, 200000, np.inf]
    size_bucket_labels = ['Less than 50k',
                          'Between 50k and 100k',
                         'Between 100k and 150k',
                         'Between 150k and 200k',
                          'More than 200k']
    
    df['Size_Category'] = pd.cut (df['Size'], bins = size_buckets, labels = size_bucket_labels)
     
    size_markdown = df.groupby(['Size_Category', 'Has_Markdown'])['Weekly_Sales'].agg(['median','count']).unstack()
    
    size_markdown.columns = ['No_Markdown_Median','Markdown_Median',
                           'No_Markdown_Count','Markdown_Count']
    
    size_markdown['Uplift %'] = (size_markdown['Markdown_Median'] - size_markdown['No_Markdown_Median'])/ size_markdown['No_Markdown_Median']*100

    
    #Draw visualisable plots
    logging.info ("Drawing visualisable plot...")
    plot_data = size_markdown.reset_index()

    #Create figure explicitly
    fig, ax = plt.subplots()
    sns.barplot (x = 'Size_Category', y = 'Uplift %', data = plot_data, color = '#1AC938')
    plt.xticks (plot_data['Size_Category'],rotation = 45)
    plt.title ('Markdown uplift by store size category')

    logging.info ("Returning results and chart...")
    logging.info ("Done the store size markdown uplift analysis!!")
    
    return size_markdown.sort_values ('Uplift %', ascending = False), fig


# TEST RUN

if __name__ == "__main__":
    df = pd.read_csv(os.path.join(OUTPUT_PATH, 'transformed_dataset.csv'), 
                 parse_dates=['Date'])
                 
    setup_logging()
    markdown_uplift_analysis_store(df)
    markdown_uplift_analysis_store_size(df)

