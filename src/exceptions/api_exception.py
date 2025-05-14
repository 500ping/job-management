# src/exceptions/custom_exceptions.py
class BaseAPIException(Exception):
    """Base exception for all API errors"""

    status_code = 500
    message = "An unexpected error occurred"

    def __init__(self, message=None, status_code=None, payload=None):
        self.message = message or self.message
        self.status_code = status_code or self.status_code
        self.payload = payload
        super().__init__(self.message)

    def to_dict(self):
        error_dict = dict(self.payload or ())
        error_dict["message"] = self.message
        error_dict["status"] = self.status_code
        return error_dict


class ResourceNotFoundException(BaseAPIException):
    status_code = 404
    message = "Resource not found"


class ValidationException(BaseAPIException):
    status_code = 400
    message = "Validation error"


class JobSchedulerException(BaseAPIException):
    status_code = 500
    message = "Job scheduler error"
