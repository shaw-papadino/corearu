from fastapi import (
        APIRouter, Request, Depends
)

from linebot import (
        LineBotApi, WebhookHandler
)

from linebot.models import (
        MessageEvent, TextMessage, TextSendMessage,
        LocationMessage, URIAction, TemplateSendMessage,
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

import controller.UserDAO as dao
import controller.UserIn as userin
from sqlalchemy.orm import Session
from controller.db_create import SessionLocal

from interfaces.quick_reply import quick_reply
from interfaces.carousel import create_columns, create_template

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
router = APIRouter()
handler = WebhookHandler(CHANNEL_SECRET)

get_book_service = GetBookService()
get_library_service = GetLibraryService()
get_zousho_service = GetZoushoService()

def get(user_id: str, db: Session = SessionLocal):
    user = dao.get_user(user_id, db)
    return user

def create(user_id: str, db: Session = SessionLocal):
    user = dao.create_user(user_id = user_id, db = db)
    # print(user)
    return user

def update(user_id: str, user_book: str, user_status: int, db: Session = SessionLocal):
    user = dao.update_user(user_id, user_book, user_status, db)
    return user

@router.get("/users")
def users(db: Session = Depends(dao.get_db)):
    user = get("1")
    print(user)

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

@handler.add(MessageEvent, message=LocationMessage)
def location_message(event):
    geocode = [str(event.message.longitude), str(event.message.latitude)]
    uid = event.source.user_id
    # print(geocode)
    user = get(uid)
    if user is None or user.is_status == 0:
        reply = "「蔵書を検索する」と入力してください"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply))

    elif user.is_status == 1:
        reply = "本のタイトルを入力してください"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply))
    elif user.is_status == 2:
        # 最寄りの図書館を検索する
        lib_info = get_library_service.get(geocode)
        lib_info = get_library_service.adapt(lib_info)
        # 受け取った本が蔵書されているかのチェック
        zousho_info = get_zousho_service.get(user.book, lib_info)
        print(zousho_info)
        column_info = []
        for i in zousho_info:
            column_info.append({"title": i["formal"], "text": i["status"], "actions" :[URIAction(label = "図書館情報ページ",uri = i["uri"]),URIAction(label = "図書館の場所",uri = i["mapuri"])]})
        reply_template = create_template(create_columns(column_info))
        # 最寄りの図書館の情報と蔵書状況を整形
        # print(zousho_info)
        status = user.is_status + 1
        user = update(uid, "", 0)
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text = "library info", template = reply_template))

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    # print(event.source.sender_id)
    # jsonのkeyとは違うから注意
    uid = event.source.user_id
    user = get(uid)
    if message == "蔵書を検索する":
        # ユーザー登録処理
        if user is  None:
            user = create(uid)
        elif user.is_status == 0:
            user = update(uid, "", 1)

        reply = "本のタイトルを入力してください"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply))
    elif user is None or user.is_status == 0:
        reply = "「蔵書を検索する」と入力してください"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply))

    elif user.is_status == 1:
        # isbn検索
        isbn = get_book_service.get(message)
        status = user.is_status + 1
        user = update(uid, isbn, status)
        reply = "下のボタンを押して現在地を送信してね"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply, quick_reply=quick_reply))

    elif user.is_status == 2:
        # 図書館蔵書検索
        reply = "蔵書検索をします"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply))
