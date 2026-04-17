from flask import Flask, request, jsonify
from src.replies.testReplyFinal import testByCompaniesReplyFinal,testByDifficultyReplyFinal, testByGenAIReplyFinal
from src.replies.scoreReplyFinal import scoreReplyFinalForAll
from src.utils.customException import handle_exceptions
from src.utils.customLogger import logger
from pathlib import Path
from flask_cors import CORS
import os

app=Flask(__name__)

# Configure CORS to allow requests from http://localhost:8080
CORS(
    app,
    supports_credentials=True,
    resources={r"/*": {"origins": ["https://major-front.onrender.com"]}}
)


# Global error handler
@app.errorhandler(500)
def handle_500(error):
    return jsonify({"error": "Internal Server Error"}), 500

@app.errorhandler(400)
def handle_400(error):
    return jsonify({"error": "Bad Request"}), 400

@handle_exceptions
@app.route("/get_questions_dsa",methods=["POST"])
def get_questions_dsa():
    data=request.get_json()

    logger.info(f"{os.path.abspath(__file__)}: new request at /get_questions_dsa")

    if not data:
        logger.info(f"{os.path.abspath(__file__)}: No data recieved")
        return jsonify({"error":"No JSON data recieved"}), 400
    
    questionsDict,dbDict=testByDifficultyReplyFinal(data)
    
    logger.info(f"{os.path.abspath(__file__)}: response sent to frontend")

    return jsonify({
        "questionsDict":questionsDict,
        "dbDict":dbDict
    })

@handle_exceptions
@app.route("/get_questions_companies",methods=["POST"])
def get_questions_companies():
    data=request.get_json()

    logger.info(f"{os.path.abspath(__file__)}: new request at /get_questions_companies")

    if not data:
        return jsonify({"error":"No JSON data recieved"}), 400
    
    questionsDict,dbDict=testByCompaniesReplyFinal(data)

    logger.info(f"{os.path.abspath(__file__)}: response sent to frontend")

    return jsonify({
        "questionsDict":questionsDict,
        "dbDict":dbDict
    })

@app.route("/get_questions_genai",methods=["POST"])
def get_questions_genai():
    data=request.get_json()

    logger.info(f"{os.path.abspath(__file__)}: new request at /get_questions_genai")

    if not data:
        return jsonify({"error":"No JSON data recieved"}), 400
    
    print(f"Calling testByGenAIReplyFinal function from {os.path.abspath(__file__)}")
    questionsDict,dbDict=testByGenAIReplyFinal(data)

    logger.info(f"{os.path.abspath(__file__)}: response sent to frontend")

    return jsonify({
        "questionsDict":questionsDict,
        "dbDict":dbDict
    })

@app.route("/submit",methods=["POST"])
def submit():

    # print("Headers:", request.headers)
    # print("Raw body:", request.get_data(as_text=True))

    data=request.get_json()

    logger.info(f"{os.path.abspath(__file__)}: new request at /submit")

    if not data:
        return jsonify({"error":"No JSON data recieved"}), 400
    
    finalResult=scoreReplyFinalForAll(data)

    logger.info(f"{os.path.abspath(__file__)}: response sent to frontend")

    return jsonify({
        "result":finalResult
    })

if __name__=="__main__":
    app.run(debug=False)



