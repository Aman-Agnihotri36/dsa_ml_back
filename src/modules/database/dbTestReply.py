import pandas as pd
from src.modules.database import ensureDbFiles
from src.utils import loadConfig
from src.entity.testReplyConfigs import databaseTestInitConfig, databaseTestDetailsConfig, databaseQuestionDetailsConfig
import os
from src.utils.customLogger import logger
from src.utils.customException import handle_exceptions
from pathlib import Path
import os

class databaseInitTestReplyHandler:
    def __init__(self,config:databaseTestInitConfig):

        # This is to handle test-user realted enteries in the database

        self.config=config
        self.fileConfig=loadConfig("config/dbconfig.yaml")

        logger.info(f"{os.path.abspath(__file__)}: Ensuring DB exists...")

        ensureDbFiles(self.fileConfig.target,vars(self.fileConfig.filesAndColumns))

    @handle_exceptions
    def dbInit(self):

        filePath=self.fileConfig.userTestFilePath
        columns=self.fileConfig.testUserDetails

        values=[self.config.userId,self.config.testId, self.config.testType, self.config.timeStamp]
        newRow=pd.DataFrame([values], columns=columns)

        if os.path.exists(filePath):
            df=pd.read_excel(filePath)
            for col in columns:
                if col not in df.columns:
                    df[col]=None
            
            if {"userId","testId"}.issubset(df.columns):
                newUser=newRow.iloc[0]["userId"]
                newTest=newRow.iloc[0]["testId"]

                if((df["userId"]==newUser)&(df["testId"]==newTest)).any():

                    logger.info(f"{os.path.abspath(__file__)}: Duplicate entry to {values[0]} having testId {values[1]} found. Not Registered.")

                    return False
            
            logger.info(f"{os.path.abspath(__file__)}: no duplicate found for {values[0]} having testId {values[1]}")

            df=pd.concat([df,newRow],ignore_index=True)

        else:
            df=newRow

        df.to_excel(filePath,index=False)

        logger.info(f"{os.path.abspath(__file__)}: User-Test Details {values} Added to table {filePath}")
        return True

class databaseTestDetailsTestReplyHandler:
    def __init__(self,config:databaseTestDetailsConfig):

        # This is to handle test details entry in the database

        self.config=config
        self.fileConfig=loadConfig("config/dbconfig.yaml")

        logger.info(f"{os.path.abspath(__file__)}: Ensuring DB exists...")

        ensureDbFiles(self.fileConfig.target,vars(self.fileConfig.filesAndColumns))

    @handle_exceptions
    def dbTestDetailsInit(self):

        filePath=self.fileConfig.testDetailsFilePath
        columns=self.fileConfig.testDetails

        values=[self.config.userId,self.config.testId, self.config.numberOfQuestions, self.config.difficultyLevel,self.config.companies, self.config.dataStructures, self.config.timeLimit]
        newRow=pd.DataFrame([values], columns=columns)

        if os.path.exists(filePath):
            df=pd.read_excel(filePath)
            for col in columns:
                if col not in df.columns:
                    df[col]=None
            
            if {"userId","testId"}.issubset(df.columns):
                newUser=newRow.iloc[0]["userId"]
                newTest=newRow.iloc[0]["testId"]

                if((df["userId"]==newUser)&(df["testId"]==newTest)).any():

                    logger.info(f"{os.path.abspath(__file__)}: Duplicate entry to {values[0]} having testId {values[1]} found. Not Registered.")

                    return False
                
            logger.info(f"{os.path.abspath(__file__)}: no duplicate found for {values[0]} having testId {values[1]}")
    
            df=pd.concat([df,newRow],ignore_index=True)
        else:
            df=newRow

        df.to_excel(filePath,index=False)

        logger.info(f"{os.path.abspath(__file__)}: Test Details {values} Added to table {filePath}")
        return True


class databaseQuestionDetailsTestReplyHandler:
    def __init__(self,config:databaseQuestionDetailsConfig):

        # This is to handle all question details entry in the database

        self.config=config
        self.fileConfig=loadConfig("config/dbconfig.yaml")

        logger.info(f"{Path(__file__).name}: Ensuring DB exists...")

        ensureDbFiles(self.fileConfig.target,vars(self.fileConfig.filesAndColumns))

    @handle_exceptions
    def dbQuestionDetailsInit(self):

        filePath=self.fileConfig.questionDetailsFilePath
        columns=self.fileConfig.questionDetails

        values=[self.config.userId,self.config.testId, self.config.questionIds]
        newRow=pd.DataFrame([values], columns=columns)

        if os.path.exists(filePath):
            df=pd.read_excel(filePath)
            for col in columns:
                if col not in df.columns:
                    df[col]=None
            
            if {"userId","testId"}.issubset(df.columns):
                newUser=newRow.iloc[0]["userId"]
                newTest=newRow.iloc[0]["testId"]

                if((df["userId"]==newUser)&(df["testId"]==newTest)).any():

                    logger.info(f"{Path(__file__).name}: Duplicate entry to {values[0]} having testId {values[1]} found. Not Registered.")

                    return False

            logger.info(f"{Path(__file__).name}: no duplicate found for {values[0]} having testId {values[1]}")
        
            df=pd.concat([df,newRow],ignore_index=True)
        else:
            df=newRow

        df.to_excel(filePath,index=False)
        
        logger.info(f"{Path(__file__).name}: Test Details {values} Added to table {filePath}")
        return True