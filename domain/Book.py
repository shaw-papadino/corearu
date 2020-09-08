from typing import List
from pydantic import BaseModel, validator, ValidationError

class Book(BaseModel):
    title: str
    image_link: str
    isbn: str = ""
    authors: List[str] = []

    @validator("isbn")
    def isbn_13(cls, v):
        if len(v) != 10 and len(v) != 13:
            raise ValidationError("must be 10 or 13 characters")
        return v

    @validator("image_link")
    def isImageLink(cls, v):
        if v == "":
            v = "https://3.bp.blogspot.com/-09TaaQbkXv4/WMZxD_LmjAI/AAAAAAABCg8/cnL_5x6RubUF1QG-LN1HTBR_EXuUtZckQCLcB/s400/kaban_sagasu_woman_komaru.png"
        return v
