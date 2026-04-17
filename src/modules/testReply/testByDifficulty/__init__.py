# from src.utils import readData
# from src.entity.testReplyConfigs import testByDifficultyConfig
# from src.utils.customException import handle_exceptions
# from src.utils.customLogger import logger
# from pathlib import Path

# class testByDifficultyGeneration:

#     # This module will generate the test for the testByDifficulty or testByDataStructure Module

#     def __init__(self,data:testByDifficultyConfig):

#         logger.info(f"{Path(__file__).name}: test by difficuly generation...")

#         self.data=data

#     @handle_exceptions
#     def generateTest(self):

#         if self.data==None:

#             logger.info(f"{Path(__file__).name}: duplicates found")

#             return None, None

#         numberOfQuestions=self.data.numberOfQuestions
#         difficultyLevel=self.data.difficultyLevel
#         dataStructure=self.data.dataStructure
#         excelPath=self.data.excelPath
#         seed=self.data.seed
        
#         logger.info(f"{Path(__file__).name}: Parameter: noq: {numberOfQuestions}, diff: {difficultyLevel}, DSA:{dataStructure}, seed:{seed}")

#         df=readData(excelPath)

#         index=[i for i in range(1,numberOfQuestions+1)]

#         filteredDf=df[df['difficulty'].isin(difficultyLevel) & df['dataStructure'].isin(dataStructure)]

#         sampleDf=filteredDf.sample(n=min(numberOfQuestions, len(filteredDf)), random_state=seed)
#         questionsForFrontend=dict(zip(sampleDf["id"], sampleDf["question"]))
#         questionsForDatabase=dict(zip(index, questionsForFrontend.keys()))

#         logger.info(f"{Path(__file__).name}: questions found, returning dictionaries...")

#         return questionsForFrontend, questionsForDatabase

import json
import re
from src.utils import readData
from src.entity.testReplyConfigs import testByDifficultyConfig
from src.utils.customException import handle_exceptions
from src.utils.customLogger import logger
from pathlib import Path

class testByDifficultyGeneration:
    # This module will generate the test for the testByDifficulty or testByDataStructure Module

    def __init__(self, data: testByDifficultyConfig):
        logger.info(f"{Path(__file__).name}: test by difficulty generation...")
        self.data = data

    @handle_exceptions
    def generateTest(self):
        if self.data is None:
            logger.info(f"{Path(__file__).name}: no data provided")
            return None, None

        numberOfQuestions = self.data.numberOfQuestions
        difficultyLevel = self.data.difficultyLevel
        dataStructure = self.data.dataStructure
        excelPath = self.data.excelPath
        seed = self.data.seed
        
        logger.info(f"{Path(__file__).name}: Parameters: noq: {numberOfQuestions}, diff: {difficultyLevel}, DSA: {dataStructure}, seed: {seed}")

        # Read the Excel file
        df = readData(excelPath)

        # Filter DataFrame based on difficulty and data structure
        filteredDf = df[df['difficulty'].isin(difficultyLevel) & df['dataStructure'].isin(dataStructure)]

        if len(filteredDf) == 0:
            logger.info(f"{Path(__file__).name}: no questions found for the given criteria")
            return None, None

        # Sample the required number of questions
        sampleDf = filteredDf.sample(n=min(numberOfQuestions, len(filteredDf)), random_state=seed)

        # Function to preprocess and parse dsa_problem string
        def parse_dsa_problem(dsa_string):
            if not isinstance(dsa_string, str) or not dsa_string.strip():
                logger.error(f"{Path(__file__).name}: Invalid or empty dsa_problem string: {dsa_string}")
                return None
            
            try:
                # Remove leading/trailing whitespace and check for prefix
                dsa_string = dsa_string.strip()
                if not dsa_string.startswith('dsa_problem = '):
                    logger.error(f"{Path(__file__).name}: Missing 'dsa_problem = ' prefix in: {dsa_string}")
                    return None
                
                # Extract JSON part
                json_string = dsa_string.split('dsa_problem = ', 1)[1]
                if not json_string.strip():
                    logger.error(f"{Path(__file__).name}: Empty JSON content after prefix in: {dsa_string}")
                    return None
                
                # Preprocess JSON to convert numeric keys to string keys
                # Match numeric keys followed by a colon (e.g., "1:" or "2:") and add quotes
                json_string = re.sub(r'(\n\s*)(\d+)(:)', r'\1"\2"\3', json_string)
                
                # Parse JSON
                return json.loads(json_string)
            except json.JSONDecodeError as e:
                logger.error(f"{Path(__file__).name}: JSON parsing error in: {dsa_string}, Error: {e}")
                return None
            except IndexError as e:
                logger.error(f"{Path(__file__).name}: IndexError in: {dsa_string}, Error: {e}")
                return None

        # Create questionsForFrontend and questionsForDatabase
        questionsForFrontend = {}
        questionsForDatabase = {}
        index = 1
        for _, row in sampleDf.iterrows():
            parsed_question = parse_dsa_problem(row["question"])
            if parsed_question is not None:  # Only include valid parsed questions
                questionsForFrontend[row["id"]] = parsed_question
                questionsForDatabase[str(index)] = row["id"]
                index += 1

        if not questionsForFrontend:
            logger.info(f"{Path(__file__).name}: no valid questions found after parsing")
            return None, None

        logger.info(f"{Path(__file__).name}: questions found, returning dictionaries...")

        return questionsForFrontend, questionsForDatabase