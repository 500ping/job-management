from datetime import datetime
from typing import Any, Dict

from flask_restful import Resource


class HealthCheck(Resource):
    def get(self) -> Dict[str, Any]:
        """
        Simple health check endpoint that verifies the server is running.

        Returns:
            Dict containing basic status information
        """
        health_status = {
            "status": "ok",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "job-management",
            "version": "0.1.0",
        }

        return health_status, 200
