from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import Boolean, DateTime, Enum, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.enums.service_enums import ServiceEnum
from src.models.base import BaseModel


class Job(BaseModel):
    __tablename__ = "job"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    args: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)
    service: Mapped[ServiceEnum] = mapped_column(Enum(ServiceEnum), nullable=False)
    cron_expression: Mapped[str] = mapped_column(String(100), nullable=False)

    active: Mapped[bool] = mapped_column(Boolean, default=True)
    next_run: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    scheduler_id: Mapped[str] = mapped_column(String(100), nullable=False)

    histories: Mapped[List["JobHistory"]] = relationship(  # noqa
        "JobHistory", back_populates="job", lazy="noload", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"Job(id={self.id}, name={self.name}, url={self.url}, active={self.active})"
        )
