from flask_restful import Resource, marshal_with

from src.models.job import Job
from src.services.job import JobService
from src.validators.job import job_fields, job_parser


class Job(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.job_service = JobService()

    @marshal_with(job_fields)
    def get(self, job_id: str) -> Job:
        return self.job_service.get_job(job_id)

    @marshal_with(job_fields)
    def put(self, job_id: str) -> Job:
        args = job_parser.parse_args()
        return self.job_service.update_job(job_id, args)

    def delete(self, job_id) -> (dict, int):
        self.job_service.delete_job(job_id)
        return {"result": True}, 200
