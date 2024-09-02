from flask import Blueprint, render_template, request, jsonify
from app.models.faiss_model import handle_question

main = Blueprint('main', __name__)

@main.route('/')
def index_route():
    return render_template('index.html')

@main.route('/ask', methods=['POST'])
def ask_question():
    user_question = request.json.get('question')
    if not user_question:
        return jsonify({"error": "No question provided"}), 400

    response = handle_question(user_question)
    return jsonify({"response": response})
