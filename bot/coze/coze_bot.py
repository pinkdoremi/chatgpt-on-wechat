# encoding:utf-8

import json
import requests

from bot.bot import Bot
from bridge.reply import Reply, ReplyType
from common.log import logger
from config import conf, load_config


# Coze对话模型API (可用)
class CozeBot(Bot):
    def reply(self, query, context=None):
        url = conf().get("coze_api_base")
        token = conf().get("coze_api_key")
        botId = conf().get("coze_bot_id")
        post_data = {
            "bot_id": f"{botId}",
            "query": f"{query}",
            "user": "default",
            "conversation_id":"0",
            "stream": False
        }
        print(post_data)

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type":"application/json",
            "Accept":"*/*",
            "Host":"api.coze.com",
            "Connection": "keep-alive"
        }
        response = requests.post(url, data=json.dumps(post_data), headers=headers)
        if response:
            print(response.json())
            messages = response.json()["messages"]
            answers = [obj for obj in messages if obj["type"] == "answer"]
            reply = Reply(
                ReplyType.TEXT,
                answers[0]['content'],
            )
            return reply