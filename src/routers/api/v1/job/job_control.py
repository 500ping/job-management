from typing import Any, Dict

from flask_restful import Resource, abort

from src.common.scheduler import Scheduler
from src.services.job import JobService

custom_scheduler = Scheduler()


class JobControl(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.job_service = JobService()
        self.scheduler = custom_scheduler.get_scheduler()

    def post(self, job_id: str, action: str) -> (Dict[str, Any], int):
        if action not in ("pause", "resume"):
            abort(400, message=f"Invalid action: {action}")

        active = action != "pause"
        db_job = self.job_service.change_job_status(job_id, active)

        return {"active": db_job.active}, 200
