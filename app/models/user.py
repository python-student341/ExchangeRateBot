from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger
import enum

from app.models.base import Base


class Currency(enum.Enum):
    rub = "rub"
    kzt = "kzt"
    usd = "usd"

class NotificationMode(enum.Enum):
    on_change = "on_change"
    by_time = "by_time"

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    currency: Mapped[Currency] = mapped_column(default=Currency.usd, nullable=True)
    notification_mode: Mapped[NotificationMode] = mapped_column(default=NotificationMode.on_change, nullable=True)