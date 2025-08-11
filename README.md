# Job Management API

A Python-based RESTful API for managing scheduled jobs using Flask, Flask-RESTful, Flask-CORS, and APScheduler.

## Features

- Create, update, delete, and retrieve scheduled jobs.
- Pause and resume jobs.
- Supports cron-based scheduling.
- Provides job details, including next run time and status.
- Health check endpoint for monitoring application status.

## API Endpoints

### Health Check
- `GET /health-check` - Simple liveness check (returns 200 when server is running)

### Jobs
- `GET /api/v1/jobs` - List all jobs
- `POST /api/v1/jobs` - Create a new job
- `GET /api/v1/jobs/{job_id}` - Get job details
- `PUT /api/v1/jobs/{job_id}` - Update a job
- `DELETE /api/v1/jobs/{job_id}` - Delete a job
- `POST /api/v1/jobs/{job_id}/{action}` - Control job (pause/resume)

## Requirements

- Python `>=3.12,<4.0`
- uv package manager

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd job-management
   ```

2. Install dependencies:
   ```bash
   pip install uv
   uv sync
   ```

## Usage

1. Start the API server:
   ```bash
   uv run python main.py
   ```

2. Access the API at `http://localhost:6699`.

## Deployment

1. Using docker
    ```bash
    docker build -t job-management .
    docker run -p 6699:6699 --name job-management-app job-management
    ```

## License

This project is licensed under the MIT License.
