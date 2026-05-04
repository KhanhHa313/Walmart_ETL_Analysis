import os 
import logging
from config import LOG_PATH
# LOGGING SETUP

os.makedirs(LOG_PATH, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_PATH, "pipeline.log")),
        logging.StreamHandler()
    ]
)