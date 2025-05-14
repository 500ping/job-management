from typing import Optional

from sqlalchemy import Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.enums.job_enum import JobEnum
from src.models.base import BaseModel
from src.models.job import Job


class JobHistory(BaseModel):
    __tablename__ = "job_history"

    job_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("job.id", ondelete="CASCADE"), index=True
    )
    job: Mapped[Job] = relationship("Job", back_populates="histories", lazy="noload")

    status: Mapped[str] = mapped_column(
        Enum(JobEnum), nullable=False, default=JobEnum.SUCCESS
    )
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
