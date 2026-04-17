# from langchain_groq import ChatGroq
# # from langchain.prompts import ChatPromptTemplate
# from langchain_core.prompts import ChatPromptTemplate
# from langchain.output_parsers import StructuredOutputParser, ResponseSchema
# import json, re, os
# from dotenv import load_dotenv
# from src.utils.customLogger import logger

# load_dotenv()

# groq_api_key = os.getenv("GROQ_API_KEY")
# if groq_api_key:
#     logger.info(f"{os.path.abspath(__file__)}: GROQ_API_KEY loaded successfully!")
# else:
#     logger.info(f"{os.path.abspath(__file__)}: GROQ_API_KEY not found. Make sure it's in your .env file.")

# # ---------------- Groq LLM ----------------
# llm = ChatGroq(
#     temperature=0.2,   # lower temperature = more deterministic
#     groq_api_key=groq_api_key,
#     model="llama-3.1-8b-instant"
# )

# # ---------------- Schema ----------------
# response_schemas = [
#     ResponseSchema(name="result", description="True if solution is correct, else False"),
#     ResponseSchema(name="testCase", description="The test case if incorrect, otherwise null"),
#     ResponseSchema(name="explanation", description="Explanation if incorrect, otherwise null"),
# ]

# parser = StructuredOutputParser.from_response_schemas(response_schemas)
# format_instructions = parser.get_format_instructions()

# # ---------------- Prompt ----------------
# prompt = ChatPromptTemplate.from_template(
#     """
# You are a DSA evaluator. 
# You are given a coding question and its proposed solution.
# Your task:
# 1. Verify if the solution is correct for the question.
# 2. If correct: return as per the JSON schema.
# 3. If incorrect: return as per the JSON schema with a failing test case and explanation.

# Question (ID: {qid}):
# {question}

# Proposed Solution:
# {solution}

# Return only a JSON object in this exact format:
# {format_instructions}
# """
# ).partial(format_instructions=format_instructions)

# # ---------------- Utils ----------------
# def extract_json(text: str):
#     """Fallback: extract JSON object from raw text if malformed."""
#     text = text.strip()
#     if text.startswith("```"):  # remove code fences
#         text = re.sub(r"^```(json)?", "", text)
#         text = re.sub(r"```$", "", text)

#     match = re.search(r"\{.*\}", text, re.DOTALL)
#     if match:
#         try:
#             cleaned = re.sub(r",\s*}", "}", match.group())
#             cleaned = re.sub(r",\s*]", "]", cleaned)
#             return json.loads(cleaned)
#         except Exception as e:
#             return {"result": False, "testCase": None, "explanation": f"Bad JSON parse: {e}\nRaw: {text}"}
#     return {"result": False, "testCase": None, "explanation": f"No JSON found. Raw: {text}"}

# def evaluate_solution(qid, question, solution):
#     """Evaluate a single solution against its question."""
#     chain = prompt | llm
#     response = chain.invoke({"qid": qid, "question": question, "solution": solution})
#     try:
#         return parser.parse(response.content)
#     except Exception as e:
#         logger.warning(f"Parser failed, falling back: {e}")
#         return extract_json(response.content)

# def evaluate_all(questions_dict, solutions_dict):
#     """Evaluate all solutions and return final dictionary."""
#     results = {}
#     logger.info(f"{os.path.abspath(__file__)}: evaluate_all func called for \n questions: {questions_dict}\n solutions: {solutions_dict}")
#     for qid, question in questions_dict.items():
#         logger.info(f"{os.path.abspath(__file__)}: qid: {qid}\n question: {question}")
#         sol = solutions_dict.get(qid)
#         if sol is None:
#             try:
#                 sol = solutions_dict.get(int(qid))
#             except ValueError:
#                 pass
#         logger.info(f"{os.path.abspath(__file__)}: sol:{sol}")
#         if sol is None:
#             results[qid] = {"result": False, "testCase": None, "explanation": "No solution provided"}
#             logger.info(f"{os.path.abspath(__file__)}: {results[qid]}")
#         else:
#             results[qid] = evaluate_solution(qid, question, sol)
#             logger.info(f"{os.path.abspath(__file__)}: {results[qid]}")
#     return results

# def count_correct_solutions(results_dict):
#     """Count how many solutions are correct in the results dict."""
#     return sum(
#         1 for res in results_dict.values()
#         if str(res["result"]).lower() == "true"
#     )


from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# ✅ FIXED IMPORT
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

import json
import re
import os
from dotenv import load_dotenv
from src.utils.customLogger import logger

# ---------------- ENV ----------------
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if groq_api_key:
    logger.info(f"{os.path.abspath(__file__)}: GROQ_API_KEY loaded successfully!")
else:
    logger.info(f"{os.path.abspath(__file__)}: GROQ_API_KEY not found. Set it in environment variables.")

# ---------------- LLM ----------------
llm = ChatGroq(
    temperature=0.2,
    api_key=groq_api_key,
    model="llama-3.1-8b-instant"
)

# ---------------- Schema ----------------
response_schemas = [
    ResponseSchema(name="result", description="True if solution is correct, else False"),
    ResponseSchema(name="testCase", description="The test case if incorrect, otherwise null"),
    ResponseSchema(name="explanation", description="Explanation if incorrect, otherwise null"),
]

parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = parser.get_format_instructions()

# ---------------- Prompt ----------------
prompt = ChatPromptTemplate.from_template(
    """
You are a DSA evaluator.

You are given a coding question and its proposed solution.

Your task:
1. Verify if the solution is correct for the question.
2. If correct: return as per the JSON schema.
3. If incorrect: return as per the JSON schema with a failing test case and explanation.

Question (ID: {qid}):
{question}

Proposed Solution:
{solution}

Return only a JSON object in this exact format:
{format_instructions}
"""
).partial(format_instructions=format_instructions)

# ---------------- Utils ----------------
def extract_json(text: str):
    """Fallback: extract JSON object from raw text if malformed."""
    text = text.strip()

    if text.startswith("```"):
        text = re.sub(r"^```(json)?", "", text)
        text = re.sub(r"```$", "", text)

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            cleaned = re.sub(r",\s*}", "}", match.group())
            cleaned = re.sub(r",\s*]", "]", cleaned)
            return json.loads(cleaned)
        except Exception as e:
            return {
                "result": False,
                "testCase": None,
                "explanation": f"Bad JSON parse: {e}\nRaw: {text}"
            }

    return {
        "result": False,
        "testCase": None,
        "explanation": f"No JSON found. Raw: {text}"
    }

# ---------------- Evaluate One ----------------
def evaluate_solution(qid, question, solution):
    chain = prompt | llm
    response = chain.invoke({
        "qid": qid,
        "question": question,
        "solution": solution
    })

    try:
        return parser.parse(response.content)
    except Exception as e:
        logger.warning(f"Parser failed, falling back: {e}")
        return extract_json(response.content)

# ---------------- Evaluate All ----------------
def evaluate_all(questions_dict, solutions_dict):
    results = {}

    logger.info(f"{os.path.abspath(__file__)}: evaluate_all called")

    for qid, question in questions_dict.items():
        sol = solutions_dict.get(qid)

        if sol is None:
            try:
                sol = solutions_dict.get(int(qid))
            except:
                pass

        if sol is None:
            results[qid] = {
                "result": False,
                "testCase": None,
                "explanation": "No solution provided"
            }
        else:
            results[qid] = evaluate_solution(qid, question, sol)

    return results

# ---------------- Count Correct ----------------
def count_correct_solutions(results_dict):
    return sum(
        1 for res in results_dict.values()
        if str(res["result"]).lower() == "true"
    )
