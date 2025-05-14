from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from src.common.scheduler import Scheduler
from src.configs.setting import get_settings
from src.exceptions.handler import register_error_handlers
from src.routers.api.v1.job.job import Job
from src.routers.api.v1.job.job_control import JobControl
from src.routers.api.v1.job.job_list import JobList

settings = get_settings()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
api = Api(app)

# Register error handlers
register_error_handlers(app)

# Register the routes
api_v1 = "/api/v1/"

api.add_resource(JobList, f"{api_v1}/jobs")
api.add_resource(Job, f"{api_v1}jobs/<string:job_id>")
api.add_resource(JobControl, f"{api_v1}jobs/<string:job_id>/<string:action>")

if __name__ == "__main__":
    try:
        app.run(
            host=settings.app_host,
            port=settings.app_port,
            debug=settings.debug,
            use_reloader=settings.debug,
        )
    finally:
        # Properly shut down the scheduler when the app is terminated
        scheduler = Scheduler()
        scheduler.shutdown()
