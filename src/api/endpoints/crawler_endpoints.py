from fastapi import APIRouter

from schema.github_crawler_schema import GitHubCrawlerSettings

from services.github_crawler_service import GitHubCrawlerService

router = APIRouter()


@router.post("/github_crawler", response_model=dict)
async def invoke_github_crawler(settings: GitHubCrawlerSettings):
    """
    Invoke GitHub crawler to find URLs of chosen type.

    :param settings:
    keywords - list of keywords for search request.
    proxies - list of proxies to get randomly picked from.
    type - type of values for crawler.
    :return: status of the crawling job.
    """
    crawler = GitHubCrawlerService(settings)
    crawler.start_crawler()
    return {"status": "Crawling started."}


@router.get("/github_crawler/results", response_model=dict | list[dict])
async def get_crawled_results() -> dict | list[dict]:
    """
    Get the results of the crawled URLs.

    :return: list of parsed GitHub URLs.
    """
    results = GitHubCrawlerService.last_crawled_results

    if results is not []:
        return results
    return {"status": "No results available."}
