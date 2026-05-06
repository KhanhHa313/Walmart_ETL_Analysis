import os
import logging 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from utils.logging_set_up import setup_logging
from utils.config import OUTPUT_PATH, MARKDOWN_COLS
from analysis_question.combined_impact import holiday_vs_md_amplify
from analysis_question.holiday_impact import holiday_impact
from analysis_question.markdown_combo import markdown_count_storesize_impact, each_store_md_combo  
from analysis_question.markdown_impact import markdown_uplift_analysis_store, markdown_uplift_analysis_store_size 
from analysis_question.quarterly_pattern import quarterly_sales_pattern


def load_results (df, output_path = OUTPUT_PATH):
    '''Acts as a generalised loader that takes a dataframe and any analysis function, run it and save the result as CSVs 
    and corresponding charts as PNG'''
    analysis_func = input('Analysis function you want to look at: ')
    file_name = input('What title do you want to save the file as: ')
    
    result_df, fig = analysis_func(df)

    # Create output folder if it doesn't exist
    logging.info("Checking output folder exist, if not, create")
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    
    # Save CSV file for the analytical df and merged df
    logging.info(f"Saving the data file into {file_name}.csv... ")

    file_path = os.path.join(OUTPUT_PATH, f"{file_name}.csv")
    result_df.to_csv(file_path, index=True)
    
    if fig is not None:
        logging.info(f"Saving the chart as image into {file_name}.png... ")

        returned_output = "Table and chart"
        
        # Save the chart as PNG
        image_path = os.path.join(OUTPUT_PATH, f"{file_name}.png")

        # dpi and bbox_inches are used to ensure high-res, perfectly cropped image saved
        fig.savefig(image_path, dpi=300, bbox_inches='tight')
        
        #Help to free memory
        plt.close(fig)   

    else:
        logging.info("This analytical question you asked does not have charts along...")

        returned_output = "Table only (no chart)"
 
    logging.info( f"{returned_output} for {analysis_func.__name__} saved to: {file_path}")

# TEST RUN 

if __name__ == "__main__":
    df = pd.read_csv(os.path.join(OUTPUT_PATH, 'transformed_dataset.csv'), 
                 parse_dates=['Date'])
    setup_logging()

    for i in range (7):
        #As there are 7 function in total
        load_results(df)


    # load_results(df, quarterly_sales_pattern, 
    #             "quarterly_pattern")

    # load_results(df, markdown_uplift_analysis_store,  
    #             "markdown_uplift_per_store")

    # load_results(df, markdown_uplift_analysis_store_size,  
    #             "markdown_uplift_per_store_size")

    # load_results(df, markdown_count_storesize_impact, 
    #             "markdown_count_impact_on_storesize")

    # load_results(df, lambda f: each_store_md_combo(f, "Less than 50k"), 
    #             "md_combo_popularity_across_storesize")

    # load_results(df, holiday_impact, 
    #             "holiday_impact")

    # load_results(df, holiday_vs_md_amplify, 
    #             "holiday_markdown_combined_impact")

