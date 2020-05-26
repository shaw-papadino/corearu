from typing import List
from pydantic import BaseModel, validator, ValidationError

class Book(BaseModel):
    title: str
    isbn: str
    authors: List[str] = []

    @validator("isbn")
    def isbn_13(cls, v):
        if len(v) != 13:
            raise ValidationError("must be 13 characters")
        return v
