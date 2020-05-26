from fastapi import (
        APIRouter, Request, BackgroundTasks
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

from service.GetBookService import GetBookService
from service.GetLibraryService import  (
        GetZoushoService, GetLibraryService
)
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
router = APIRouter()
handler = WebhookHandler(CHANNEL_SECRET)

get_book_service = GetBookService()
get_library_service = GetLibraryService()
get_zousho_service = GetZoushoService()

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
user_status = {}
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    # print(event.source.sender_id)
    # jsonのkeyとは違うから注意
    uid = event.source.user_id
    print(user_status)
    if (uid in user_status.keys()):
        #useridが登録されている場合
        print(user_status.keys())
        isbn = background_tasks.add_task(get_book_service, message)
        # isbn = get_book_service.get(message)
        print(isbn)

    else:
        if (message == "蔵書を検索する"):
            user_status[uid] = 1
            print(user_status)
            reply = "本のタイトルを入力してください"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply))
        else:
            print(event)

    # line_bot_api.push_message(event.source.user_id, TextSendMessage(text=event.message.text))
"""
[] 蔵書検索モード
[] 本 -> isbn
[] 位置情報 -> 最寄りの図書館
[] isbn 最寄りの図書館 -> 蔵書
"""
