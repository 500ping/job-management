from flask_restful import fields, reqparse

from src.enums.job_enum import JobEnum
from src.enums.service_enums import ServiceEnum


class EnumField(fields.Raw):
    def __init__(self, enum_class, **kwargs):
        self.enum_class = enum_class
        super(EnumField, self).__init__(**kwargs)

    def format(self, value):
        if isinstance(value, self.enum_class):
            return value.value
        return value


job_history_fields = {
    "id": fields.String,
    "job_id": fields.String,
    "status": EnumField(JobEnum),
    "error_message": fields.String,
    "created_at": fields.String,
}

job_fields = {
    "id": fields.String,
    "name": fields.String,
    "url": fields.String,
    "args": fields.Raw,
    "service": EnumField(ServiceEnum),
    "cron_expression": fields.String,
    "active": fields.Boolean,
    "next_run": fields.String,
    "scheduler_id": fields.String,
    "histories": fields.List(fields.Nested(job_history_fields)),
}

# Parser for jobs
job_parser = reqparse.RequestParser()
job_parser.add_argument("name", type=str, help="Name of the job", required=True)
job_parser.add_argument("args", type=dict, help="Arguments for the function")
job_parser.add_argument(
    "cron_expression",
    type=str,
    help='Cron expression (e.g., "* * * * *")',
    required=True,
)
job_parser.add_argument(
    "service",
    type=str,
    help="Service to trigger",
    default=ServiceEnum.TRADING_ASSISTANT,
)
job_parser.add_argument("url", type=str, help="Api url to trigger", required=True)
job_parser.add_argument("active", type=bool, help="status of the job", default=True)
