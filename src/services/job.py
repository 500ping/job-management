import uuid
from typing import Any, Dict, List

from flask_restful import abort
from sqlalchemy.orm import joinedload

from src.common.db import get_db_session
from src.common.scheduler import Scheduler
from src.models.job import Job
from src.utils.trigger_api import main_job


class JobService:
    def __init__(self) -> None:
        self.scheduler = Scheduler()

    def create_job(self, request: Dict[str, Any]) -> (Job, int):
        # Create the job and persist to database
        with get_db_session() as session:
            try:
                scheduler_id = str(uuid.uuid4())

                job_name = request.get("name")
                cron_expression = request.get("cron_expression")
                job_args = request.get("args", {})
                url = request.get("url", "")

                # Create job record in database
                db_job = Job(
                    name=job_name,
                    url=url,
                    service=request.get("service"),
                    cron_expression=cron_expression,
                    args=job_args,
                    active=True,
                    scheduler_id=scheduler_id,
                )
                session.add(db_job)
                session.flush()

                # Add job to scheduler
                job = self.scheduler.create_job(
                    func=main_job,
                    expression=cron_expression,
                    job_id=scheduler_id,
                    name=job_name,
                    kwargs={
                        "job_id": db_job.id,
                        "scheduler_id": scheduler_id,
                        "url": url,
                        "body": job_args,
                    },
                )

                # Update job record with next run time
                db_job.next_run = job.next_run_time
                session.add(db_job)
                session.commit()

                return db_job, 201
            except Exception:
                session.rollback()
                raise

    @staticmethod
    def get_jobs() -> List[Job]:
        with get_db_session() as session:
            result = session.query(Job).options(joinedload(Job.histories)).all()
        return result

    @staticmethod
    def get_job(job_id: str) -> Job:
        with get_db_session() as session:
            job = (
                session.query(Job)
                .filter(Job.id == int(job_id))
                .options(joinedload(Job.histories))
                .first()
            )
            if not job:
                abort(404, message=f"Job {job_id} not found")
        return job

    def update_job(self, job_id: str, request: Dict[str, Any]) -> Job | None:
        with get_db_session() as session:
            try:
                db_job = session.query(Job).filter(Job.id == int(job_id)).one()
                if not db_job:
                    abort(404, message=f"Job {job_id} not found")

                job_name = request.get("name")
                cron_expression = request.get("cron_expression")
                job_args = request.get("args", {})
                url = request.get("url", "")

                # Update job properties
                db_job.name = job_name
                db_job.url = url
                db_job.service = request.get("service")
                db_job.cron_expression = cron_expression
                db_job.args = job_args
                db_job.active = request.get("active", True)

                session.add(db_job)
                session.flush()

                # Remove old job from scheduler
                scheduler_id = db_job.scheduler_id
                self.scheduler.delete_job(job_id)

                # Create new job
                job = self.scheduler.create_job(
                    func=main_job,
                    expression=cron_expression,
                    job_id=scheduler_id,
                    name=job_name,
                    kwargs={
                        "job_id": db_job.id,
                        "scheduler_id": scheduler_id,
                        "url": url,
                        "body": job_args,
                    },
                )

                # Update job record with next run time
                db_job.next_run = job.next_run_time
                session.add(db_job)
                session.commit()

                return job
            except Exception:
                session.rollback()
                raise

    def delete_job(self, job_id: str) -> None:
        with get_db_session() as session:
            try:
                db_job = session.query(Job).filter(Job.id == int(job_id)).one()
                if not db_job:
                    abort(404, message=f"Job {job_id} not found")

                scheduler_id = db_job.scheduler_id

                session.delete(db_job)
                session.commit()

                # Delete scheduler job
                self.scheduler.delete_job(scheduler_id)
            except Exception:
                session.rollback()
                raise

    def change_job_status(self, job_id: str, active: bool) -> Job | None:
        with get_db_session() as session:
            try:
                db_job = session.query(Job).filter(Job.id == int(job_id)).one_or_none()
                if not db_job:
                    abort(404, message=f"Job {job_id} not found")

                # Update job status
                scheduler_id = db_job.scheduler_id
                db_job.active = active
                session.add(db_job)
                session.flush()

                # Change job status in scheduler
                self.scheduler.change_job_status(scheduler_id, active)

                session.commit()
                session.refresh(db_job)
                return db_job
            except Exception:
                session.rollback()
                raise
