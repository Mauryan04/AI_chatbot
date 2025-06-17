from flask import Flask, request, jsonify
from flask_cors import CORS
from app.chatbot import ChatBot  # Ensure `chatbot.py` is in app/ or adjust the path

app = Flask(__name__)
CORS(app)

chatbot = ChatBot()

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    query = data.get('query', '')
    answer = chatbot.ask(query)
    return jsonify({'answer': answer})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

