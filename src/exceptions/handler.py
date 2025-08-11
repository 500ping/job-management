from flask import jsonify

from src.exceptions.api_exception import BaseAPIException
from src.log.handler import logger


def register_error_handlers(app):
    """Register error handlers with the Flask app"""

    @app.errorhandler(BaseAPIException)
    def handle_api_exception(error):
        logger.error(f"API Exception: {error.message}", exc_info=True)
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(404)
    def handle_not_found(error):
        logger.error(f"Not Found: {str(error)}", exc_info=True)
        response = jsonify({"status": 404, "message": "Resource not found"})
        response.status_code = 404
        return response

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        logger.error(f"Unexpected error: {str(error)}", exc_info=True)
        response = jsonify({"status": 500, "message": "An unexpected error occurred"})
        response.status_code = 500
        return response
