


import json
import re
import pandas as pd
import numpy as np
from src.utils import readData
from src.entity.testReplyConfigs import testByCompaniesConfig
from src.utils.customException import handle_exceptions
from src.utils.customLogger import logger
from pathlib import Path

class testByCompaniesGeneration:

    # This module finds questions for test by companies module

    def __init__(self, data: testByCompaniesConfig):
        logger.info(f"{Path(__file__).name}: generating test by companies...")
        self.data = data

    @handle_exceptions
    def generateTest(self):
        if self.data is None:
            logger.info(f"{Path(__file__).name}: no data provided")
            return None, None

        numberOfQuestions = self.data.numberOfQuestions
        difficultyLevel = self.data.difficultyLevel
        companies = self.data.companies
        excelPath = self.data.excelPath
        seed = self.data.seed

        logger.info(
            f"{Path(__file__).name}: Parameters: noq={numberOfQuestions}, "
            f"diff={difficultyLevel}, comp={companies}, seed={seed}"
        )

        df = readData(excelPath)

        # Apply filters
        df = df[df['difficulty'].isin(difficultyLevel)]
        companies_lower = [c.lower().strip() for c in companies]

        df['companies_lower'] = (
            df['companies']
            .str.lower()
            .str.split(',')
            .apply(lambda x: [item.strip() for item in x])
        )

        df = df[df['companies_lower'].apply(lambda x: any(comp in x for comp in companies_lower))]

        df = df.drop(columns=['companies_lower'])
        np.random.seed(seed)

        if len(df) == 0:
            logger.info(f"{Path(__file__).name}: no questions found for given criteria")
            return None, None

        sampleDf = df.sample(n=min(numberOfQuestions, len(df)), random_state=seed)

        # --- Helper to parse JSON-style question strings ---
        def parse_dsa_problem(dsa_string):
            if not isinstance(dsa_string, str) or not dsa_string.strip():
                logger.error(f"{Path(__file__).name}: Invalid or empty dsa_problem string: {dsa_string}")
                return None

            try:
                dsa_string = dsa_string.strip()
                if not dsa_string.startswith('dsa_problem = '):
                    # If not prefixed, assume it's already JSON
                    json_string = dsa_string
                else:
                    json_string = dsa_string.split('dsa_problem = ', 1)[1]

                if not json_string.strip():
                    return None

                # Fix numeric keys (e.g., 1: -> "1":)
                json_string = re.sub(r'(\n\s*)(\d+)(:)', r'\1"\2"\3', json_string)

                return json.loads(json_string)

            except json.JSONDecodeError as e:
                logger.error(f"{Path(__file__).name}: JSON parsing error: {e}")
                return None
            except Exception as e:
                logger.error(f"{Path(__file__).name}: Unexpected error parsing question: {e}")
                return None

        # --- Build frontend + db dictionaries ---
        questionsForFrontend = {}
        questionsForDatabase = {}
        index = 1

        for _, row in sampleDf.iterrows():
            parsed_question = parse_dsa_problem(row["question"])
            if parsed_question is not None:
                questionsForFrontend[row["id"]] = parsed_question
                questionsForDatabase[str(index)] = row["id"]
                index += 1

        if not questionsForFrontend:
            logger.info(f"{Path(__file__).name}: no valid questions after parsing")
            return None, None

        logger.info(f"{Path(__file__).name}: Found questions, returning...")
        return questionsForFrontend, questionsForDatabase
