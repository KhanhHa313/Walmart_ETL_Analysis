import os 
import logging
from config import LOG_PATH

# LOGGING SETUP
def setup_logging():
    os.makedirs(LOG_PATH, exist_ok=True)
        
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f"{LOG_PATH}/pipeline.log"),
            logging.StreamHandler()
        ]
    )
    
    logging.info("Logging initialised successfully")

if __name__ == "__main__":
    setup_logging()
    logging.info("hello")