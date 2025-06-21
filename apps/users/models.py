from flask_login import UserMixin

from apps.database import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import mapped_column
from apps.extensions import db, login_manager


@login_manager.user_loader
def user_loader(user_id):
    return db.session.execute(db.select(User).where(User.id == user_id))



class User(BaseModel, UserMixin):
    __tablename__ = 'users'

    username = mapped_column(String(80), unique=True)
    email = mapped_column(String(80), unique=True, nullable=False)
    password = mapped_column(String(256), nullable=False)


    def __repr__(self):
        return f"{self.__class__.__name__}('{self.username}, {self.email}')"