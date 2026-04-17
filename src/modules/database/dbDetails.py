import pandas as pd
from src.modules.database import ensureDbFiles
from src.utils import loadConfig
from src.utils.customLogger import logger
from src.utils.customException import handle_exceptions
from pathlib import Path
import os
import ast


class generalRetrieval:
  def __init__(self, userId, testId):
    self.userId=userId
    self.testId=testId
    logger.info(f"{os.path.abspath(__file__)}: generalRetrieval called")

  def retrieveQuestionIdsGeneral(self):
    logger.info(f"{os.path.abspath(__file__)}: generalRetrieval: restrieveQuestionIdsGeneral called")
    df=pd.read_excel("db/questionDetails.xlsx")

    # Ensure required columns exist
    required_cols = {"userId", "testId", "questionIds"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Excel file must contain columns: {required_cols}")

    # Filter row
    row = df[(df["userId"] == self.userId) & (df["testId"] == self.testId)]

    if row.empty:
        return {}

    # Get the questionIds value
    question_ids_value = row.iloc[0]["questionIds"]

    # If it's stored as a string (like '{"q1":"What is...","q2":"..."}'), parse it
    if isinstance(question_ids_value, str):
        try:
            logger.info(f"{os.path.abspath(__file__)}: questionIds: {ast.literal_eval(question_ids_value)}")
            return ast.literal_eval(question_ids_value)  # safe conversion
        except Exception:
            raise ValueError("questionIds column is not a valid dictionary string")

    # If already a dict, return as is
    if isinstance(question_ids_value, dict):
        logger.info(f"{os.path.abspath(__file__)}: questionsIds: {question_ids_value}")
        return question_ids_value

    # Fallback
    raise TypeError("questionIds column must be a dict or string-representation of dict")


  def get_test_details(self):
      """
      Fetch test details from two Excel files based on (userId, testId).
      The pair (userId, testId) is unique across both files.
      """
      logger.info(f"{os.path.abspath(__file__)}: generalRetrieval: getTestDetails called")
      # Load both Excel files
      df1 = pd.read_excel("db/testUserDetails.xlsx")
      df2 = pd.read_excel("db/testDetails.xlsx")
      logger.info(f"{os.path.abspath(__file__)}: userId: {self.userId}\ntestId: {self.testId}")
      # Ensure required columns exist
      required1 = {"userId", "testId", "timeStamp", "testType"}
      required2 = {"userId", "testId", "numberOfQuestions", "difficultyLevel", "companies", "dataStructure", "timeLimit"}
      
      if not required1.issubset(df1.columns):
          raise ValueError(f"File1 must contain columns: {required1}")
      if not required2.issubset(df2.columns):
          raise ValueError(f"File2 must contain columns: {required2}")

      # Filter rows
      row1 = df1[(df1["userId"] == self.userId) & (df1["testId"] == self.testId)]
      row2 = df2[(df2["userId"] == self.userId) & (df2["testId"] == self.testId)]
      if row1.empty or row2.empty:
          return {}

      # Convert both rows to dicts
      dict1 = row1.iloc[0].to_dict()
      dict2 = row2.iloc[0].to_dict()
      logger.info(f"{os.path.abspath(__file__)}: dict1: {dict1}\n dict2: {dict2}")
      # Merge dictionaries (dict2 overrides dict1 if duplicate keys exist)
      result = {**dict1, **dict2}
      logger.info(f"{os.path.abspath(__file__)}: result: {result}")
      return result


