from flask import Flask, request, jsonify
from flask_cors import CORS
from chat_bot import chat_bot_response

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_message = request.json['message']
        response = chat_bot_response(user_message)
        return jsonify({'response': response})
    else:
        return jsonify({'response': 'This is a GET request. Please use POST for chatting.'})

if __name__ == '__main__':
    app.run(debug=True)
