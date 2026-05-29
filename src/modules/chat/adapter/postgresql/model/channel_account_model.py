from datetime import datetime
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from src.pkg.database.database import Base

class ChannelAccountModel(Base):
    __tablename__ = "channel_accounts"

    page_id: Mapped[str] = mapped_column(String, primary_key=True)
    page_name: Mapped[str] = mapped_column(String, nullable=False)
    page_access_token: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)