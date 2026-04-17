from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
import json
from dotenv import load_dotenv
import os
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if groq_api_key:
    print("GROQ_API_KEY loaded successfully!")
else:
    print("GROQ_API_KEY not found. Make sure it's in your .env file.")
# Initialize Groq LLM
llm = ChatGroq(
    temperature=0.7,
    groq_api_key=groq_api_key,
    model="llama-3.1-8b-instant"
)

# Prompt template for generating DSA questions
prompt = ChatPromptTemplate.from_template("""
You are a DSA question generator.
Generate exactly {num_questions} coding questions from the following topics: {topics}.
Each question must have one of these difficulty levels: {difficulties}.
Distribute them randomly among the generated questions, but ensure all requested difficulty levels appear at least once if possible.

⚠️ IMPORTANT: Return ONLY valid JSON, with no extra text, no comments, no explanations.

Format:
{{
  "1": {{
    "question": "problem_statement",
    "difficultyLevel": "difficultyLevelofthequestion",
    "examples": {{
      "1": {{
        "input": "some_input",
        "output": "some_output",
        "explanation": "some_explanation"
      }}
    }},
    "constraints": {{
      "1": "someConstraint",
      "2": "someConstraint"
    }}
  }},
  "2": ...
}}
""")

def safe_json_parse(text: str):
    """Extract and parse JSON even if model adds extra text."""
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        json_str = text[start:end]
        return json.loads(json_str)
    except Exception as e:
        print("❌ JSON parse failed:", e)
        print("Raw response:", text)
        return None

def generate_questions(num_questions: int, topics: list, difficulties: list):
    chain = prompt | llm
    response = chain.invoke({
        "num_questions": num_questions,
        "topics": topics,
        "difficulties": difficulties
    })
    return safe_json_parse(response.content)