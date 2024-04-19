import requests
import json
import discord
from flask import Flask
import threading

# Discord bot initialization
bottoken = '***'
channel='***'
botid = '***'
usertoken = '***'
post_botmsg_url = ''
# 配置结束

url = f"https://discord.com/api/v9/channels/{channel}/messages"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    print(message.content)
    payload = json.dumps({
        "content": f"{message.content}"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", post_botmsg_url, headers=headers, data=payload)
    print(response.text)

# Flask app initialization
app = Flask(__name__)

@app.route('/')
def say_to_bot(askmsg):
    payload = json.dumps({
        "content": f"<@{botid}> {askmsg}"
    })
    headers = {
        'Authorization': f'{usertoken}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response

def run_discord_bot():
    client.run(bottoken)

def run_flask_app():
    app.run(threaded=True)

if __name__ == '__main__':
    # Start Discord bot and Flask app in separate threads
    bot_thread = threading.Thread(target=run_discord_bot)
    app_thread = threading.Thread(target=run_flask_app)

    bot_thread.start()
    app_thread.start()

    # Keep main thread alive to prevent premature exit
    while True:
        pass