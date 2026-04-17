from src.config.scoreReplyConfigManager import scoreReplyConfigurationManager
from src.modules.tests.test_main import testHandler
from src.utils.customLogger import logger
import os
logger.info(f"{os.path.abspath(__file__)}: testByDifficultyReplyFinal called")

def scoreReplyFinalForAll(data:dict):
  logger.info(f"{os.path.abspath(__file__)}: scoreReplyFinalForAll called")
  configManager=scoreReplyConfigurationManager(data)
  logger.info(f"{os.path.abspath(__file__)}: {data}")
  config=configManager.solutionDetailsConfigurationManager()
  logger.info(f"{os.path.abspath(__file__)}: Test Evaluating")
  testHandlerObj=testHandler(config)
  finalResult=testHandlerObj.returnResult()
  logger.info(f"{os.path.abspath(__file__)}: Evaluation Completed")
  # Database
  return finalResult