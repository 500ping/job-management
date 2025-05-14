# Job Management API

A Python-based RESTful API for managing scheduled jobs using Flask, Flask-RESTful, Flask-CORS, and APScheduler.

## Features

- Create, update, delete, and retrieve scheduled jobs.
- Pause and resume jobs.
- Supports cron-based scheduling.
- Provides job details, including next run time and status.

## Requirements

- Python `>=3.12,<4.0`
- Dependencies:
  - Flask `>=3.1.0,<4.0.0`
  - Flask-RESTful `>=0.3.10,<0.4.0`
  - Flask-CORS `>=5.0.1,<6.0.0`
  - APScheduler `>=3.11.0,<4.0.0`
  - Requests `>=2.32.3,<3.0.0`

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

## License

This project is licensed under the MIT License.
```

Replace `<repository-url>` with the actual URL of your repository. You can further customize this README as needed.
