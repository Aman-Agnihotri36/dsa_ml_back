from src.entity.testReplyConfigs import testByGenAIConfig
from src.utils.customException import handle_exceptions
from src.utils.customLogger import logger
from pathlib import Path
from src.modules.testReply.testByGenAI.genAINew import generate_questions
import os

class testByGenAIGeneration:

    # This module will generate the test for the testByDifficulty or testByDataStructure Module

    def __init__(self,data:testByGenAIConfig):

        logger.info(f"{os.path.abspath(__file__)}: test by generative ai generation...")

        self.data=data

    @handle_exceptions
    def generateTest(self):

        if self.data==None:

            logger.info(f"{os.path.abspath(__file__)}: duplicates found")

            return None, None

        numberOfQuestions=self.data.numberOfQuestions
        difficultyLevel=self.data.difficultyLevel
        dataStructure=self.data.dataStructure
        
        
        logger.info(f"{os.path.abspath(__file__)}: Parameter: noq: {numberOfQuestions}, diff: {difficultyLevel}, DSA:{dataStructure}")

        #num_questions: int, topics: list, difficulties: list, retries=2
        output = generate_questions(num_questions=numberOfQuestions,topics=dataStructure,difficulties=difficultyLevel)
        questionsForFrontend=output
        questionsForDatabase=output
        logger.info(f"{os.path.abspath(__file__)}: questions generated, returning dictionaries...")

        return questionsForFrontend, questionsForDatabase

    