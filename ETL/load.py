import os
import logging 
import pandas as pd
import matplotlib.pyplot as plt
from utils.logging_set_up import setup_logging
from utils.config import OUTPUT_PATH 
from analysis_question.combined_impact import holiday_vs_md_amplify
from analysis_question.holiday_impact import holiday_impact
from analysis_question.markdown_combo import markdown_count_storesize_impact, each_store_md_combo  
from analysis_question.markdown_impact import markdown_uplift_analysis_store, markdown_uplift_analysis_store_size 
from analysis_question.quarterly_pattern import quarterly_sales_pattern


def load_results (df, output_path = OUTPUT_PATH):
    '''Acts as a generalised loader that takes a dataframe and any analysis function, run it and save the result as CSVs 
    and corresponding charts as PNG'''

    #Listing out all the function that user could choose from 
    function_map = {
        '1' : quarterly_sales_pattern,
        '2' : markdown_uplift_analysis_store,
        '3' : markdown_uplift_analysis_store_size,
        '4' : markdown_count_storesize_impact,
        '5' : each_store_md_combo,
        '6' : holiday_impact,
        '7' : holiday_vs_md_amplify
    }
    
    logging.info("Letting user choose the analysis question they want to look at...")
    print("What analysis question you want to look at (Pick a number): ")

    #While true is used for in case user choose function that is not listed 
    while True: 
        print(''' 1. quarterly_sales_pattern \n 2. markdown_uplift_analysis_store \n 3. markdown_uplift_analysis_store_size \n 4. markdown_count_storesize_impact \n 5. each_store_md_combo \n 6. holiday_impact \n 7. holiday_vs_md_amplify \n
                ''')
        
        
        #Ask for user input 
        analysis_func_number = input('Analysis function you want to look at: ')

        if analysis_func_number not in function_map:
            print ('Function you choose are not in the list. Please try again!!')
            logging.info('User is choosing the function again...')
            continue 

        else: 
            analysis_func = function_map[analysis_func_number] 
            logging.info(f'Analysis function about {analysis_func.__name__} is chosen')
            break 

    file_name = input('What title do you want to save the file as: ')
    
    result_df, fig = analysis_func(df)

    # Create output folder if it doesn't exist
    logging.info("Checking output folder exist, if not, create")
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    
    # Save CSV file for the analytical df and merged df
    logging.info(f"Saving the data file into {file_name}.csv... ")

    file_path = os.path.join(OUTPUT_PATH, f"{file_name}.csv")
    result_df.to_csv(file_path, index=True)
    
    #As there are some function does not return chart 
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

    # for i in range (7):
    #     #As there are 7 function in total THIS IS FOR THE RUN TEST ONLY 
    #     load_results(df)

    load_results(df)
    while True: 
        preference = input("Do you want to run another analysis (Y/N): ").lower()
        if preference not in ['yes', 'no', 'y', 'n']:
            print ("Please choose Yes or No!!!")
            continue 
        elif preference == 'y' or preference == 'yes':
            info.logging('User decided to run another analysis')
            load_results(df)
            break
        else: 
            info.logging('User want to stop this analysis for now!')
            break 

    
