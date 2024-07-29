# GitHub Crawler

This project implements a GitHub crawler that searches for repositories, issues, or wikis based on provided keywords and returns the URLs. It uses FastAPI for the API, BeautifulSoup for HTML parsing, and Poetry for dependency management.

## Technology Stack

- **Python 3.12**
- **FastAPI**
- **Requests**
- **BeautifulSoup**
- **Poetry**

## Installation

### Prerequisites

- Python 3.12
- Poetry (for dependency management)

### Setup

1. **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Set up poetry environment and install dependencies:**

    ```bash
    poetry shell
    poetry install
    ```

3. **Set up environment variables:**

    Create a `.env` file in the root directory of the project and add the following environment variables:

    ```env
    PROJECT_NAME=GitHub Crawler
    ALLOW_ORIGINS=["*"]
    APP_HOST=0.0.0.0
    APP_PORT=8000
    APP_RELOAD=False
    API_V1_STR=/api/v1
    GITHUB_API_URL=https://github.com/
    ```

## Running the Project
    
Run locally:
```shell
python src/main.py
```

## API Usage
### POST "/api/v1/crawler/github_crawler"
Endpoint that starts asynchronous crawling job.

**Request Body**

keywords (list of strings): A list of keywords for the search request.

proxies (list of strings): A list of proxies to randomly pick from.

type (string): The type of values for the crawler (repositories, issues, or wikis).

Example request:
```json
{
  "keywords": ["python", "django"],
  "proxies": ["http://localhost:8080"],
  "type": "repositories"
}
```
Example response:
```json
{
   "status": "Crawling started."
}
```

### GET "/api/v1/crawler/results"
Endpoint for retrieving crawled results.

Example response:
```json
[
  {
    "url": "https://github.com/author/repo"
  },
  {
    "url": "https://github.com/author/another-repo"
  },
  ...
]
```

## Running tests
Run test coverage:
```shell
poetry run pytest --cov=services --cov-report=term-missing tests/
```
