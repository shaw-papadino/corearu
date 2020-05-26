from pydantic import BaseModel

class Library(BaseModel):
    systemid: int
    libkey: str
    libid: str
    name: str
    geocode: List[str]
    
