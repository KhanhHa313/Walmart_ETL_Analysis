import os
import logging 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from utils.logging_set_up import setup_logging
from utils.config import OUTPUT_PATH, MARKDOWN_COLS

def holiday_vs_md_amplify(df): 
    #Check whether holiday and md amplify impacts of one another and which have more impacts on sales individually
    logging.info ("Checking the combined impacts of both holiday and markdowns on sales acorss store...")

    df['Holiday_vs_Markdown'] = df['Is_Holiday'].map ({True : 'Holiday', False : 'Non_Holiday'}) \
    +' + '+ df['Has_Markdown'].map ({True : 'Markdown', False : 'Non_Markdown'}) 
    
    combo_effect = df.groupby(['Holiday_vs_Markdown'])['Weekly_Sales'].agg(['median','count']).reset_index()
    
    combo_effect.insert (1, 'Interpretation', 
                        pd.Series (['Baseline Demand', 
                                    'Markdown effects only',
                                    'Holiday Demand spike', 
                                    'Peak demand (stacked effects)']))
                                             
     
    baseline = combo_effect[combo_effect['Holiday_vs_Markdown'] == 'Non_Holiday + Non_Markdown']['median'].values[0]
     
    combo_effect['Uplift %'] = (combo_effect['median'] -  baseline)/baseline *100
    combo_effect = combo_effect.rename(columns = {'median': 'Median Sales', 'count':'Week Counts'})

    fig, ax = plt.subplots()
    sns.barplot (x = 'Uplift %', y = 'Holiday_vs_Markdown', data = combo_effect, palette = 'bright')
    
    logging.info ("Returning results and chart...")
    logging.info ("Done the holiday and markdown amplify impact analysis!!")

    return combo_effect.sort_values(by = 'Uplift %'), fig

if __name__ == "__main__":
    df = pd.read_csv(os.path.join(OUTPUT_PATH, 'transformed_dataset.csv'), 
                 parse_dates=['Date'])
                 
    setup_logging()
    holiday_vs_md_amplify(df)
