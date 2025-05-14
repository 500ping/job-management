import json
from typing import Any, Dict, Optional, Union

import requests

from src.common.db import get_db_session
from src.common.scheduler import Scheduler
from src.enums.job_enum import JobEnum
from src.log.handler import logger
from src.models.job import Job
from src.models.job_history import JobHistory

custom_scheduler = Scheduler()
scheduler = custom_scheduler.get_scheduler()


def main_job(
    job_id: int,
    scheduler_id: str,
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    body: Optional[Union[Dict[str, Any], str]] = None,
    params: Optional[Dict[str, Any]] = None,
) -> None:
    with get_db_session() as session:
        try:
            logger.info(f"Triggering job {job_id}")

            # Make the API call
            call_api(url=url, method=method, headers=headers, body=body, params=params)

            # API call successful, save success status to history
            job_history = JobHistory(
                job_id=job_id, status=JobEnum.SUCCESS, error_message=None
            )
            session.add(job_history)

            # Update the job's next run time
            schedule_job = scheduler.get_job(scheduler_id)
            session.query(Job).filter(Job.id == job_id).update(
                {"next_run": schedule_job.next_run_time}
            )

            session.commit()
            logger.info(f"Job {job_id} completed successfully")
        except Exception as e:
            # API call failed, save failure status with error message
            error_message = str(e)
            job_history = JobHistory(
                job_id=job_id, status=JobEnum.FAILURE, error_message=error_message
            )
            session.add(job_history)
            session.commit()

            logger.error(f"Job {job_id} failed: {error_message}")


def call_api(
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    body: Optional[Union[Dict[str, Any], str]] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
) -> requests.Response:
    """
    Make an API request using the requests library.

    Args:
        url: The URL to make the request to.
        method: HTTP method like GET, POST, PUT, DELETE, etc. Defaults to GET.
        headers: Optional dictionary of HTTP headers to send with the request.
        body: Optional dictionary or string to send in the request body.
        params: Optional dictionary of URL parameters to append to the URL.
        timeout: Request timeout in seconds. Defaults to 30.

    Returns:
        requests.Response: The response from the API.

    Raises:
        requests.RequestException: If the request fails.
    """
    method = method.upper()

    if headers is None:
        headers = {}

    # Set default Content-Type for requests with a body
    if body and "Content-Type" not in headers:
        headers["Content-Type"] = "application/json"

    request_data = {}

    if isinstance(body, dict):
        request_data["json"] = body
    elif isinstance(body, str):
        # Try to parse as JSON, otherwise send as raw data
        try:
            request_data["json"] = json.loads(body)
        except json.JSONDecodeError:
            request_data["data"] = body
    elif body is not None:
        request_data["data"] = body

    logger.debug(f"Making {method} request to {url}")

    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            timeout=timeout,
            **request_data,
        )

        logger.debug(f"Response status code: {response.status_code}")

        # Raise an exception for 4XX/5XX responses
        response.raise_for_status()

        return response

    except requests.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        raise
