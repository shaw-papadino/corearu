from linebot.models import (
        QuickReply, QuickReplyButton, LocationAction
)

quick_reply = QuickReply(
        items = [
            QuickReplyButton(
                action = LocationAction,
                label = 現在地を送る
                )
            ]
        )
