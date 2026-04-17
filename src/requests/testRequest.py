from src.config.testReplyConfigManager import testReplyConfigurationManager
from src.modules.database.dbTestReply import databaseInitTestReplyHandler, databaseTestDetailsTestReplyHandler
from src.utils.customException import handle_exceptions 
from src.utils.customLogger import logger 
from pathlib import Path
import os

# The `testRequestHandler` will handle any incoming request to the backend for test-generation. 
# It fill update the database that a new test is been requested.
# It will direct the code towards the type of test requested by the user. 
# Only if there is no duplicate entry for the request, the code will proceed. 

class testRequestHandler:
    def __init__(self,data:dict):

        # Data object from the frontend
        self.data=data
        logger.info(f"{os.path.abspath(__file__)}: Request handler called for {self.data}")

        # Configuration Manager for the testReply module of the code
        self.config=testReplyConfigurationManager(data=self.data)
        logger.info(f"{os.path.abspath(__file__)}: `testReplyConfigurationManager` called.")

        # Database test-user details entry 
        self.dbConfig=self.config.databaseTestInitManager()
        db=databaseInitTestReplyHandler(self.dbConfig)
        self.success=db.dbInit()
        logger.info(f"{os.path.abspath(__file__)}: returning from database")
    @handle_exceptions
    def returnConfig(self):

        # Cheking for the duplicate entries in the database
        if self.success:
            
            # There is no duplicate entry in the database for the request
            logger.info(f"{os.path.abspath(__file__)}: There is no duplicate entry for the data.")

            # If the test is `testByDifficulty`
            if self.data["testType"]=="testByDifficulty":
                logger.info(f"{os.path.abspath(__file__)}: The test type is `testByDifficulty`")

                # Preparing and returning the configuration for the test type
                configuration=self.config.testByDifficultyConfiguration()

                # Saving the test details in the database
                dbConfig=self.config.databaseTestDetailsManager()
                db=databaseTestDetailsTestReplyHandler(dbConfig)
                db.dbTestDetailsInit()

                logger.info(f"{os.path.abspath(__file__)}: Test Details are saved in database.")

                return configuration
            
            # If the test is `testByCompanies`
            elif self.data["testType"]=="testByCompanies":
                logger.info(f"{os.path.abspath(__file__)}: The test type is `testByCompanies`")

                # Preparing and returning the configuration for the test type
                configuration=self.config.testByCompaniesConfiguration()

                # Saving the test details in the database
                dbConfig=self.config.databaseTestDetailsManager()
                db=databaseTestDetailsTestReplyHandler(dbConfig)
                db.dbTestDetailsInit()

                logger.info("{os.path.abspath(__file__)}: Test Details are saved in database.")

                return configuration
            
            # If the test is `testByGenAI`
            elif self.data["testType"]=="testByGenAI":
                logger.info(f"{os.path.abspath(__file__)}: The test type is `testByGenAI`")

                # Preparing and returning the configuration for the test type
                configuration=self.config.testByGenAIConfiguration()
                logger.info(f"{os.path.abspath(__file__)}: COnfiguration is {configuration}")
                # Saving the test details in the database
                dbConfig=self.config.databaseTestDetailsManager()
                db=databaseTestDetailsTestReplyHandler(dbConfig)
                db.dbTestDetailsInit()

                logger.info(f"{os.path.abspath(__file__)}: Test Details are saved in database.")
                if configuration==None:
                  logger.info(f"{os.path.abspath(__file__)}: None configuration returned")
                return configuration
        else:
            
            # Duplicate entries found
            logger.info("{os.path.abspath(__file__)} duplicates found.")
            return None
        
    
            

    