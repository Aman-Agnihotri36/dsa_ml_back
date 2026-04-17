import os
from src.entity.scoreReplyConfigs import solutionDetailsConfig
from src.modules.sidereq.retrieveQuestions import get_questions_from_excel
from src.modules.tests.testGenAI import evaluate_all, count_correct_solutions
from src.modules.database.dbDetails import generalRetrieval
from src.utils.customLogger import logger


class testHandler:
  def __init__(self,config:solutionDetailsConfig):
    self.config=config
    logger.info(f"{os.path.abspath(__file__)}: userId: {self.config.userId}, testId: {self.config.testId}")
    self.dbret=generalRetrieval(self.config.userId, self.config.testId)
    self.testDetails=self.dbret.get_test_details()
    logger.info(f"{os.path.abspath(__file__)}: testDetails: {self.testDetails}")
    self.questionIds=self.dbret.retrieveQuestionIdsGeneral()

  def testbyAI(self):
   
    if self.testDetails["testType"]!="testByGenAI":
      questions=get_questions_from_excel(self.config.excelPath, self.config.solutions.keys())
    else:
      questions=self.questionIds
    
    logger.info(f"{os.path.abspath(__file__)}: Questions: {questions}")
    solutions=self.config.solutions
    logger.info(f"{os.path.abspath(__file__)}: Solutions: {solutions}")
    result=evaluate_all(questions, solutions)
    logger.info(f"{os.path.abspath(__file__)}: result: {result}")
    correctCount=count_correct_solutions(result)
    return result, correctCount

  def returnResult(self):
    result,correctCount=self.testbyAI()
    finalReply={"result":result, "correctCount":correctCount, "timeTaken":self.config.timeTaken, "testDetails":self.testDetails}
    return finalReply


