from apps.database import BaseModel
from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import mapped_column



class Post(BaseModel):
    __tablename__ = 'posts'

    title = mapped_column(String(256), nullable=False)
    body = mapped_column(Text, nullable=False)
    user_id = mapped_column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return f"{self.__class__.__name__} ({self.id}, {self.title[:30]})"