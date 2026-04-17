import os
import pandas as pd
from src.utils.customLogger import logger
from src.utils.customException import handle_exceptions
from pathlib import Path
import os

@handle_exceptions
def ensureDbFiles(targetFolder,fileSpecs):
    
    # This function is to check that the database exists or not in the backend,
    # if not then create.

    if not os.path.exists(targetFolder):

        logger.info(f"{os.path.abspath(__file__)}: Database not found. Creating...")

        os.makedirs(targetFolder)
    
    logger.info(f"{os.path.abspath(__file__)}: Database found. Checking Tables...")

    for fileName,columns in fileSpecs.items():
        filePath=os.path.join(targetFolder,fileName)
        if not os.path.exists(filePath):
            logger.info(f"{os.path.abspath(__file__)}: Creating {filePath}...")
            df=pd.DataFrame(columns=columns)
            df.to_excel(filePath,index=False)
        else:
            logger.info(f"{os.path.abspath(__file__)}: {filePath} already exists.")

