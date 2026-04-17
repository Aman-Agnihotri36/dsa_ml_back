from src.utils.customException import handle_exceptions
from src.utils.customLogger import logger
from pathlib import Path
import os
from src.entity.scoreReplyConfigs import solutionDetailsConfig

class scoreReplyConfigurationManager:
    def __init__(self,data:dict):
        
        # This class returns all the configurations required for scoreReply Module

        self.data=data
        logger.info(f"{os.path.abspath(__file__)}: running scoreReplyConfigurationManager")
    
    def solutionDetailsConfigurationManager(self):
      config=solutionDetailsConfig(
          userId=self.data["userId"],
          testId=self.data["testId"],
          solutions=self.data["solutions"],
          timeTaken=self.data["timeTaken"],
          excelPath="data/questions.xlsx"
      )
      logger.info(f"{os.path.abspath(__file__)}: returning solutionDetailsConfig")
      return config