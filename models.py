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
        return f'User {self.name} -> #{self.id}'


# https://github.com/irtiza07/photo-upload-full-stack
