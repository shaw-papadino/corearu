from fastapi import (
        APIRouter, Request
)

from linebot import (
        LineBotApi, WebhookHandler
)

from linebot.models import (
        MessageEvent, TextMessage, TextSendMessage
)

from linebot.exceptions import (
    InvalidSignatureError
)

from entity import (
        CHANNEL_ACCESS_TOKEN, CHANNEL_SECRET
)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
router = APIRouter()
handler = WebhookHandler(CHANNEL_SECRET)

@router.post("/callback")
async def callback(req: Request):
    signature = req.headers.get("X-Line-Signature")

    body = (await req.body()).decode("utf-8")
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return {"status": "OK"}

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
