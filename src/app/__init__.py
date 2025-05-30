from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
app.config.from_pyfile('config.py')
from service.messageService import MessageService
messageService = MessageService()
@app.route("/v1/ds/message",methods = ["POST"])
def handle_message():
    message = request.json.get('message')
    result = messageService.process_message(message)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="localhost",port=8000,debug=True)