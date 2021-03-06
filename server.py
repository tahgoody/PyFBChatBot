# Import Flask and request module from Flask
from flask import Flask, request

# Import request
import requests

# create a flask app instance
app = Flask(__name__)

# Tokens from the facebook page web hooks
ACCESS_TOKEN = "EAAUzNdZCxv8oBAD8qIaw2j1kfSsGgEXmpPimxMUDgeV5mp8gHyMMss6lcY1ZBbrdz1KZB5OYeZBNuflZAzgtT1vVvjzpRBZC37sitmXvojpIHXBTSTHaYM0JbuuTZAhLSfXHLZAn6b9m804eHTBpNY5u4njXoTcjtBdZCjYOxMLrvDgZDZD"
VERIFY_TOKEN = "secret"

# method to reply to a message from the sender
def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)

# GET request to handle the verification of tokens
@app.route('/', methods=['GET'])
def handle_verification():
    if request.args['hub.verify_token'] == VERIFY_TOKEN:
        return request.args['hub.challenge']
    else:
        return "Invalid verification token"

# POST request to handle in coming messages then call reply()
@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']
    reply(sender, message)

    return "ok"


if __name__ == '__main__':
    app.run(debug=True)
