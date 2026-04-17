import pandas as pd
import os
from src.utils.customLogger import logger
def get_questions_from_excel(file_path, question_ids):
    """
    Fetch questions from an Excel file based on given IDs.
    
    Args:
        file_path (str): Path to the Excel file.
        question_ids (list): List of question IDs to search for.
    
    Returns:
        dict: {id: question} for all matching IDs.
    """
    # Load Excel file
    logger.info(f"{os.path.abspath(__file__)}: filePath: {file_path}, question_ids: {question_ids}")
    df = pd.read_excel(file_path)

    # Ensure required columns exist
    if "id" not in df.columns or "question" not in df.columns:
        raise ValueError("Excel file must contain 'id' and 'question' columns")

    # Filter rows where id is in the question_ids list
    filtered_df = df[df["id"].isin(question_ids)]
    print(df)
    # Convert to dictionary {id: question}
    result = dict(zip(filtered_df["id"], filtered_df["question"]))
    logger.info(f"{os.path.abspath(__file__)}: result: {result}")
    return result


# -------- Example Usage --------
# Suppose Excel file has:
# id | question
# q1 | What is Kadane's Algorithm?
# q2 | What is a palindrome?
