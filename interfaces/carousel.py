from linebot.models import (
            CarouselTemplate, CarouselColumn,
)
"""
CarouselColumn をfor文で生成
templateに入れてかえエス
"""

def create_columns(column_info):
    """
    [{"image":"",
    "title":,
    "text":,
    "actions":[PostbackAction(....)]},]
    out [CarouselColumn(),,,]
    """
    columns = []
    for i in column_info:
        columns.append(CarouselColumn(
                # thumbnail_image_url = i.get("image", ""),
                title = i.get("title", ""),
                text = i.get("text", ""),
                actions = i.get("actions", [])
                ))
    return columns

def create_template(columns):
    return CarouselTemplate(columns)
