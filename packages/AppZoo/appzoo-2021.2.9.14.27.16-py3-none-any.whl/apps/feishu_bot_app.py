#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : feishu_bot_app
# @Time         : 2021/1/28 8:32 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :

"""
todo:
增加卡片@
增加get/post发送消息
"""
from fastapi import FastAPI
from starlette.requests import Request
import pandas as pd
from miwork.feishu import Feishu
from meutils.http_utils import request

app = FastAPI()

fs = Feishu()


@app.post("/hive/{chat}/{title}")
async def report(request: Request, chat, title, at_users=None):
    """
    at_users 逗号分割
    """

    print(at_users)

    data_str = dict(await request.form()).get('data', '')
    if data_str:
        data = eval(data_str)
        df = pd.DataFrame(data[1:], columns=data[0])
    else:
        df = pd.DataFrame()

    fs.send_by_card(
        chat_name=chat,  # 'PUSH算法组',
        title=title,
        text=df.to_string(index=True),
        md_text="",
        at_user=at_users.split(',')[0] if at_users else None  # card 增加@
    )


@app.post("/common/{chat}/{title}")
def report(chat, title, kwargs: dict):
    text = kwargs.get('text', '')

    fs.send_by_card(chat_name=chat, title=title, text="", md_text=text)


@app.get("/common/{chat}/{title}")
def report(request: Request, chat, title):
    input = dict(request.query_params)
    text = input.get('text', '')

    fs.send_by_card(chat_name=chat, title=title, text="", md_text=text)


# wehooks
@app.post("/wehook")
def wehook(kwargs: dict):
    url = kwargs.get('url')
    post = kwargs.get('post')
    return request(url, json=post)


# card
@app.post("/dfi")
def wehook(kwargs: dict):
    print(kwargs)
    if 'df_json' not in kwargs:
        df = pd.DataFrame()
    else:
        df = pd.DataFrame(kwargs.get('df_json'))
    fs.send_by_df_card(chat_name=kwargs.get('chat_name', 'PUSH算法组'),
                       title=kwargs.get('title', '我是一个标题'),
                       subtitle=kwargs.get('subtitle', ''),
                       df=df,
                       image_desc=kwargs.get('image_desc', '我是图片描述'))


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0')
