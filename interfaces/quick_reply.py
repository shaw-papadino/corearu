from linebot.models import (
        QuickReply, QuickReplyButton, LocationAction
)

quick_reply = QuickReply(
        items = [
            QuickReplyButton(
                action = LocationAction,
                label = "Location"
                )
            ]
        )
