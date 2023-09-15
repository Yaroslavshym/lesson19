import datetime

from sqlalchemy import (
    Column, Integer, Float, String, DateTime, Boolean,
    ForeignKey,
)
from sqlalchemy.orm import Mapper, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from database import Base
import settings


class BaseInfoMixin:
    id = Column(Integer, primary_key=True)
    # id: Mapper[int] = mapped_column(primary_key=True)
    notes = Column(String(settings.Settings.MAX_NOTES_LENGTH))
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)


class User(BaseInfoMixin, Base):
    __tablename__ = 'user'

    name = Column(String, nullable=False)
    login = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_conflict = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return f'User {self.name} -> #{self.id}'


class Order(BaseInfoMixin, Base):
    __tablename__ = 'order'

    pizza_quantity = Column(Integer, nullable=False)
    pizza_price = Column(Float, nullable=False)
    customer = Column(ForeignKey('user.id'))
    # customer: Mapper[int] = mapped_column(ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f'Order #{self.id}'