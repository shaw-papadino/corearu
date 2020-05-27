from fastapi import (
        APIRouter, Request, Depends
)

from linebot import (
        LineBotApi, WebhookHandler
)

from linebot.models import (
        MessageEvent, TextMessage, TextSendMessage
        LocationMessage
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

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
router = APIRouter()
handler = WebhookHandler(CHANNEL_SECRET)

get_book_service = GetBookService()
get_library_service = GetLibraryService()
get_zousho_service = GetZoushoService()


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
# 
# async def get_user(user_id: str, db: Session = Depends(get_db)):
#     return db.query(User).filter(User.id == user_id).first()
# 
# async def create_user(userIn: UserCreate, db: Session = Depends(get_db)):
#     user = User(id = userIn.id)
#     db.add(user)
#     db.commit()
#     user = get_user(userIn.id)
#     return user
# 
# async def update_user(user_id: str, user_book: str, db: Session = Depends(get_db)):
#     user = get(db, user_id)
#     user.book = user_book
#     db.commit()
#     user = get_user(user_id)
#     return user

def get(user_id: str, db: Session = SessionLocal):
    user = dao.get_user(user_id, db)
    return user

def create(userid: str, db: Session = SessionLocal):
    user = dao.create_user(user_id = userid, db = db)
    # print(user)
    return user

def update(user_id: str, user_book: str, db: Session = SessionLocal):
    user = dao.update_user(user_id, user_book, db)
    return user

@router.get("/users")
def users(db: Session = Depends(dao.get_db)):
    # user = create("1")
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
    geocode = [event.message.latitude, event.message.longitude]
    uid = event.source.user_id
    print(user_status)
    user = get(uid)
    get_library_service(user.book, geocode)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global user_status
    message = event.message.text
    # print(event.source.sender_id)
    # jsonのkeyとは違うから注意
    uid = event.source.user_id
    print(user_status)
    user = get(uid)
    if (user is  None):
        if (message == "蔵書を検索する"):
            user = create(UserCreate(uid))
            reply = "本のタイトルを入力してください"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply))
        else:
            print(event)
    # if (uid in user_status.keys()):
        #useridが登録されている場合
        # print(user_status.keys())

    else:
        if (user.is_status == 1):
            # isbn検索
            isbn = get_book_service.get(message)
            user = update(uid, isbn, user.is_status += 1)
            print(user)
            reply = "下のボタンを押して現在地を送信してね"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply, quick_reply))
        elif (user.is_status == 2):
            # 図書館蔵書検索
            pass

    # line_bot_api.push_message(event.source.user_id, TextSendMessage(text=event.message.text))
"""
[] 蔵書検索モード
[] 本 -> isbn
[] 位置情報 -> 最寄りの図書館
[] isbn 最寄りの図書館 -> 蔵書
"""
