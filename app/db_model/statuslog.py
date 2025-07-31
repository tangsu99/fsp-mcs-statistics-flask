from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from . import db

class StatusLog(db.Model):
    __tablename__ = "statuslog"
    id: Mapped[int] = mapped_column(primary_key=True)
    server_address: Mapped[str] = mapped_column(nullable=False)
    player_count: Mapped[str] = mapped_column(nullable=False)
    log_datetime: Mapped[datetime] = mapped_column(nullable=False)