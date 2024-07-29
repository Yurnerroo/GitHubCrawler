import pytest

from schema.github_crawler_schema import GitHubCrawlerSettings
from services.github_crawler_service import GitHubCrawlerService


@pytest.fixture
def github_crawler_settings():
    return GitHubCrawlerSettings(
        keywords=["python", "django"],
        proxies=["http://localhost:8080"],
        type="repositories",
    )


@pytest.fixture
def github_crawler_service(github_crawler_settings):
    return GitHubCrawlerService(github_crawler_settings)
