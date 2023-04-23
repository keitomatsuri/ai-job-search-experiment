import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import openai
from searcher import Searcher
from proposer import Proposer

# flask
app = Flask(__name__)
CORS(app)

# openai
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL")


@app.route("/ask", methods=["POST"])
def ask():
    question = request.json["question"]
    history = request.json["history"]

    searcher = Searcher(model)
    try:
        search_results = searcher.search(question, history)
    except:
        return jsonify({"answer": "検索に失敗しました。再度お試しください。"})

    proposer = Proposer(model)
    try:
        propose_result = proposer.propose(search_results, question, history)
        return jsonify({"answer": propose_result})
    except:
        return jsonify({"answer": "提案に失敗しました。再度お試しください。"})


if __name__ == '__main__':
    app.debug = True
    app.run()
