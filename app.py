from fastapi import FastAPI

from linebot import (
        LineBotApi, WebhookHandler
)


from entity import (
        CHANNEL_ACCESS_TOKEN, CHANNEL_SECRET
)

from controller.router import router, handler

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = handler 
app = FastAPI()
# router 登録処理
app.include_router(router)
