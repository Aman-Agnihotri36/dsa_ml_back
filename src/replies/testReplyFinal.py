from src.requests.testRequest import testRequestHandler
from src.modules.testReply.testByDifficulty import testByDifficultyGeneration
from src.modules.testReply.testByCompanies import testByCompaniesGeneration
from src.modules.testReply.testByGenAI import testByGenAIGeneration
from src.utils.customException import handle_exceptions
from src.config.testReplyConfigManager import testReplyConfigurationManager
from src.modules.database.dbTestReply import databaseQuestionDetailsTestReplyHandler
from pathlib import Path
import os
from src.utils.customLogger import logger

@handle_exceptions
def testByDifficultyReplyFinal(data:dict):

    # Getting configuration
    logger.info(f"{os.path.abspath(__file__)}: testByDifficultyReplyFinal called")

    requestConfigurationManager=testRequestHandler(data)
    requestConfiguration=requestConfigurationManager.returnConfig()

    # Generating the test
    logger.info(f"{os.path.abspath(__file__)}: generating test...")

    testGenerator=testByDifficultyGeneration(requestConfiguration)
    testDict,dbDict=testGenerator.generateTest()

    logger.info(f"{os.path.abspath(__file__)}: test generated")

    # Database - saving the question ids in the database
    dbdata={
        "userId": data["userId"],
        "testId": data["testId"],
        "questionIds": dbDict,
    }

    if testDict and dbDict:
        
        # If there are no duplicate enteries then
        dbConfigManager=testReplyConfigurationManager(dbdata)
        dbConfig=dbConfigManager.dataQuestionsDetailsManager()

        logger.info(f"{os.path.abspath(__file__)}: saving question ids in the database")

        db=databaseQuestionDetailsTestReplyHandler(dbConfig)
        db.dbQuestionDetailsInit()

        logger.info(f"{os.path.abspath(__file__)}: question ids saved in the database")

    return testDict, dbDict

@handle_exceptions
def testByCompaniesReplyFinal(data:dict):
    
    # Getting configuration
    logger.info(f"{os.path.abspath(__file__)}: testByCompaniesReplyFinal called")

    requestConfigurationManager=testRequestHandler(data)
    requestConfiguration=requestConfigurationManager.returnConfig()

    # Generating test
    logger.info(f"{os.path.abspath(__file__)}: generating test...")

    testGenerator=testByCompaniesGeneration(requestConfiguration)
    testDict,dbDict=testGenerator.generateTest()

    logger.info(f"{os.path.abspath(__file__)}: test generated")

    # Database - saving question ids in the database
    dbdata={
        "userId": data["userId"],
        "testId": data["testId"],
        "questionIds": dbDict,
    }

    if testDict and dbDict:

        # If there are no duplicate enteries in the database
        dbConfigManager=testReplyConfigurationManager(dbdata)
        dbConfig=dbConfigManager.dataQuestionsDetailsManager()

        logger.info(f"{os.path.abspath(__file__)}: saving the question ids in the database")

        db=databaseQuestionDetailsTestReplyHandler(dbConfig)
        db.dbQuestionDetailsInit()

        logger.info(f"{os.path.abspath(__file__)}: question ids saved in the database")
        
    return testDict, dbDict

@handle_exceptions
def testByGenAIReplyFinal(data:dict):
    
    # Getting configuration
    logger.info(f"{os.path.abspath(__file__)}: testByGenAIReplyFinal called")

    requestConfigurationManager=testRequestHandler(data)
    requestConfiguration=requestConfigurationManager.returnConfig()

    # Generating test
    logger.info(f"{os.path.abspath(__file__)}: generating test...")

    testGenerator=testByGenAIGeneration(requestConfiguration)
    testDict,dbDict=testGenerator.generateTest()

    logger.info(f"{os.path.abspath(__file__)}: test generated")

    # Database - saving question ids in the database
    dbdata={
        "userId": data["userId"],
        "testId": data["testId"],
        "questionIds": dbDict,
    }

    if testDict and dbDict:

        # If there are no duplicate enteries in the database
        dbConfigManager=testReplyConfigurationManager(dbdata)
        dbConfig=dbConfigManager.dataQuestionsDetailsManager()

        logger.info(f"{os.path.abspath(__file__)}: saving the question ids in the database")

        db=databaseQuestionDetailsTestReplyHandler(dbConfig)
        db.dbQuestionDetailsInit()

        logger.info(f"{os.path.abspath(__file__)}: question ids saved in the database")
        
    return testDict, dbDict