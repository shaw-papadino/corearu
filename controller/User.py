from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from controller.db_create import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(50), primary_key=True, unique = True)
    book = Column(String(255))
    is_status = Column(Integer, default=1)

