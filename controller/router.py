from fastapi import (
        APIRouter, Request
)

from linebot import WebhookHandler

from linebot.models import (
        MessageEvent, TextMessage, TextSendMessage
)

from entity import CHANNEL_SECRET

router = APIRouter()
handler = WebhookHandler(CHANNEL_SECRET)

@router.post("/callback")
async def callback(req: Request):
    signature = req.headers.get("X-Line-Signature")

    body = (await req.body()).decode("utf-8")
    print(body)
    print(signature)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return {"status": "OK"}

@handler.add(MessageEvent, message=TextMessage)
async def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
