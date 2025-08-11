"""
Startup checks for the application.
"""
import sys

from sqlalchemy import text

from src.common.db import get_db_session
from src.log.handler import logger


def check_database_connection() -> None:
    """
    Check database connection at application startup.
    Exits the application if the database is not accessible.
    """
    try:
        logger.info("Checking database connection...")
        with get_db_session() as session:
            result = session.execute(text("SELECT 1"))
            result.fetchone()
        logger.info("Database connection successful")
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        logger.error("Application will exit due to database connection failure")
        sys.exit(1)


def perform_startup_checks() -> None:
    """
    Perform all startup checks.
    """
    logger.info("Performing startup checks...")
    check_database_connection()
    logger.info("All startup checks passed")
