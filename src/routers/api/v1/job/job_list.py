from typing import List

from flask_restful import Resource, marshal_with

from src.models.job import Job
from src.services.job import JobService
from src.validators.job import job_fields, job_parser


class JobList(Resource):
    def __init__(self):
        super().__init__()
        self.job_service = JobService()

    @marshal_with(job_fields)
    def get(self) -> List[Job]:
        return self.job_service.get_jobs()

    @marshal_with(job_fields)
    def post(self) -> Job:
        args = job_parser.parse_args()
        return self.job_service.create_job(args)
