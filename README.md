# Job Management API

A Python-based RESTful API for managing scheduled jobs using Flask, Flask-RESTful, Flask-CORS, and APScheduler.

## Features

- Create, update, delete, and retrieve scheduled jobs.
- Pause and resume jobs.
- Supports cron-based scheduling.
- Provides job details, including next run time and status.

## Requirements

- Python `>=3.12,<4.0`

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd job-management
   ```

2. Install dependencies:
   ```bash
   pip install poetry
   poetry install
   ```

## Usage

1. Start the API server:
   ```bash
   python main.py
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
