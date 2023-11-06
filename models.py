import datetime

from sqlalchemy import (
    Column, Integer, Float, String, DateTime, Boolean,
    ForeignKey, BINARY
)
from sqlalchemy.orm import Mapper, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from database import Base
import settings


class BaseInfoMixin:
    id = Column(Integer, primary_key=True)
    # id: Mapper[int] = mapped_column(primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)


class User(BaseInfoMixin, Base):
    __tablename__ = 'user'

    name = Column(String, nullable=False)
    surname = Column(String, default='')
    login = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    def __repr__(self) -> str:
        ddict = {'id': self.id, 'name': self.name, 'login': self.login, 'password': self.password, 'is_admin': self.is_admin}
        return str(ddict)

class Recipe(BaseInfoMixin, Base):
    __tablename__ = 'recipe'

    user_id = Column(ForeignKey('user.id'))
    # image_name = Column(String, unique=True)
    recipe_text = Column(String, unique=True)
    recipe_title = Column(String)
    def get_all_values(self):

        return {'id':self.id,
                'user_id':self.user_id,
                'text': self.recipe_text,
                'title': self.recipe_title}
    def __repr__(self) -> str:
        ddict = {'id': self.id, 'user_id': self.user_id, 'recipe_text': self.recipe_text, 'recipe_title': self.recipe_title}
        return str(ddict)

    
    
# https://github.com/irtiza07/photo-upload-full-stack
