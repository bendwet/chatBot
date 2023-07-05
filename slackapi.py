import os
from flask import Flask, request
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from langchain.llms import OpenAI

app = Flask(__name__)

slack_token = os.environ["SLACK_BOT_TOKEN"]
channel = os.environ["CHANNEL"]

client = WebClient(token=slack_token)
# bot user id to prevent response to bot messages
bot_user_id = client.auth_test()['user_id']
llm = OpenAI(temperature=0.9)


@app.route("/slack/message", methods=["POST", "GET"])
def handle_message():

    data = request.json

    if 'challenge' in data:
        return data['challenge'], 200

    channel_id = data["event"]["channel"]
    text = data["event"]["text"]
    user_id = data["event"]["user"]

    answer = llm.predict(text)

    # check if the message is a DM and not from the bot
    if channel_id.startswith("D") and user_id != bot_user_id:
        try:
            client.chat_postMessage(channel=channel_id, text=answer)
        except SlackApiError as e:
            print(e)

    return "", 200


app.run()
