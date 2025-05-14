from datetime import datetime

from sqlalchemy import TIMESTAMP, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.common.db import Base


class BaseModel(Base):
    __abstract__ = True  # This prevents SQLAlchemy from creating a table for this model

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Audit fields
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    created_by: Mapped[str] = mapped_column(String(100), default="system")
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), server_onupdate=func.now()
    )
    updated_by: Mapped[str] = mapped_column(String(100), default="system")
