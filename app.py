from fastapi import FastAPI

from linebot import (
        LineBotApi, WebhookHandler
)


from entity import (
        CHANNEL_ACCESS_TOKEN, CHANNEL_SECRET
)

from controller.router import router, handler
from controller.db_create import SessionLocal, engine
from controller.User import User, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
# router 登録処理
app.include_router(router)
