import asyncio
from random import choice

from bs4 import BeautifulSoup

from exceptions.crawler_exceptions import ParsingException
from schema.github_crawler_schema import GitHubCrawlerSettings
from services.http_service import send_get_request
from settings import settings


class GitHubCrawlerService:
    """
    Service for crawling GitHub search results based on specified keywords and types.

    Attributes:
        crawler_settings (GitHubCrawlerSettings): Settings for the GitHub crawler.
        headers (dict): HTTP headers to be used in the request.
        last_crawled_results (list[dict]): Class variable to store the results of the last crawl.
    """
    last_crawled_results = []

    def __init__(self, crawler_settings: GitHubCrawlerSettings):
        self.crawler_settings = crawler_settings
        self.headers = {
            "Accept": "text/html",
        }

    @staticmethod
    def parse_html(html_text: str) -> list[dict]:
        """
        Parse the HTML response to extract URLs based on the specified criteria.

        Args:
            html_text (str): HTML content to be parsed.

        Returns:
            list[dict]: A list of dictionaries containing the extracted URLs.
        """
        soup = BeautifulSoup(html_text, "html.parser")
        tag = "div"
        class_suffix = "search-title"

        searched_results = []

        for element in soup.find_all(tag, class_=class_suffix):
            a_tag = element.find("a")
            if a_tag:
                href_ending = a_tag.get("href")
                href = f"https://github.com{href_ending}"
                searched_results.append({"url": href})

        return searched_results

    async def crawling_job(self) -> None:
        """
        Perform the crawling job with a random proxy and save the parsed HTML response.
        """
        # pick random proxy
        proxy = {"http://": "http://" + choice(self.crawler_settings.proxies)}
        params = {
            "q": ",".join(self.crawler_settings.keywords),
            "type": self.crawler_settings.type,
        }

        response_text = (
            await send_get_request(
                url=settings.GITHUB_API_URL,
                proxy=proxy,
                params=params,
                headers=self.headers,
            )
        ).text

        try:
            GitHubCrawlerService.last_crawled_results = self.parse_html(
                html_text=response_text
            )
        except Exception as e:
            raise ParsingException(message=f"HTML response processing failed: {e}")

    def start_crawler(self) -> None:
        """
        Clear results and start the crawling job as an asynchronous task.
        """
        GitHubCrawlerService.last_crawled_results = []
        asyncio.create_task(self.crawling_job())
