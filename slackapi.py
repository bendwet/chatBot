import os
from flask import Flask, request
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

app = Flask(__name__)

slack_token = os.environ["SLACK_BOT_TOKEN"]
channel = os.environ["CHANNEL"]

client = WebClient(token=slack_token)


@app.route("/slack/event", methods=["POST", "GET"])
def event_listener():

    # data = request.json
    #
    # if 'challenge' in data:
    #     return data['challenge'], 200

    print(client.chat_postMessage(channel=channel, text="Test 123"))

    return "", 200

app.run()
