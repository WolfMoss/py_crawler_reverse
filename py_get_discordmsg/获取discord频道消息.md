```python
# GET请求的headers
headers = {
    'Authorization': f'Bot {你的机器人TOKEN}',
    'Content-Type': 'application/json'
}

# 获取消息的URL
channel_messages_url = f'https://discord.com/api/v9/channels/{频道ID}/messages?limit={限制最新多少条消息}'

# 发送GET请求
response = requests.get(channel_messages_url, headers=headers)

# 对结果进行处理
if response.status_code == 200:
    messages = response.json()
    print(messages[0]['content'])

else:
    print(f"Failed to get messages with status code {response.status_code} and response: {response.text}")
```

