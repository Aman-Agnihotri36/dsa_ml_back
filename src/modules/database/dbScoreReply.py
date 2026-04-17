from src.utils.customLogger import logger
from src.utils.customException import handle_exceptions
from pathlib import Path
import os
import pandas as pd
from src.modules.database import ensureDbFiles
from src.utils import loadConfig

class databaseInitTestReplyHandler:
    def __init__(self,config):

        # This is to handle test-user realted enteries in the database

        self.config=config
        self.fileConfig=loadConfig("config/dbconfig.yaml")

        logger.info(f"{os.path.abspath(__file__)}: Ensuring DB exists...")

        ensureDbFiles(self.fileConfig.target,vars(self.fileConfig.filesAndColumns))

    