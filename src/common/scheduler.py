from typing import Any, Callable, Dict

from apscheduler.job import Job
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from src.common.db import DATABASE_URL
from src.configs.setting import get_settings

settings = get_settings()


class Scheduler:
    _instance = None

    def __new__(cls):
        """Ensure only one instance of Scheduler exists."""
        if cls._instance is None:
            cls._instance = super(Scheduler, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        """Initialize the scheduler only once when the first instance is created."""
        if not hasattr(self, "_initialized") or not self._initialized:
            self._scheduler = BackgroundScheduler()
            self._scheduler.add_jobstore(
                SQLAlchemyJobStore(url=DATABASE_URL, tableschema=settings.db_schema),
                "default",
            )
            self._scheduler.start()
            self._initialized = True

    def get_scheduler(self) -> BackgroundScheduler:
        """
        Get the application scheduler.
        Returns the instance of the BackgroundScheduler.
        """
        return self._scheduler

    def shutdown(self) -> None:
        """
        Properly shut down the scheduler.
        This method should be called when the application is terminated.
        """
        if self._scheduler:
            self._scheduler.shutdown()
            self._scheduler = None

    def create_job(
        self,
        job_id: str,
        name: str,
        func: Callable[..., Any],
        expression: str,
        **kwargs: Dict[str, Any]
    ) -> Job:
        """
        Create a new job in the scheduler.

        Args:
            job_id (str): A unique identifier for the job.
            name (str): The name of the job.
            func (Callable[..., Any]): The function to be executed by the job.
            expression (str): A cron expression defining the job's schedule.
            **kwargs (Dict[str, Any]): Additional arguments to configure the job.

        Returns:
            Job: The created job instance.
        """
        return self._scheduler.add_job(
            id=job_id,
            func=func,
            name=name,
            trigger=CronTrigger.from_crontab(expression),
            **kwargs
        )

    def delete_job(self, job_id: str) -> None:
        """
        Delete a job from the scheduler.

        Args:
            job_id (str): The unique identifier of the job to be deleted.
        """
        self._scheduler.remove_job(job_id)

    def change_job_status(self, job_id: str, active: bool = True) -> None:
        """
        Change the active status of a job in the scheduler.

        Args:
            job_id (str): The unique identifier of the job to modify.
            active (bool): If True, resume the job; if False, pause the job.
        """
        if active:
            self._scheduler.resume_job(job_id)
        else:
            self._scheduler.pause_job(job_id)
