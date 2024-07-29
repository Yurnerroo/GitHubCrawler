import asyncio
from random import choice
from urllib.parse import quote_plus

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
        url (str): Constructed URL for the GitHub search query.
        last_crawled_results (list[dict]): Class variable to store the results of the last crawl.
    """
    last_crawled_results = []

    def __init__(self, crawler_settings: GitHubCrawlerSettings):
        self.crawler_settings = crawler_settings
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }
        self.url = (
            f"{settings.GITHUB_API_URL}"
            f"?q={quote_plus(",".join(crawler_settings.keywords))}"
            f"&type={quote_plus(crawler_settings.type)}"
        )

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

        response_text = (await send_get_request(
            url=self.url,
            proxy=proxy,
            headers=self.headers,
        )).text

        try:
            GitHubCrawlerService.last_crawled_results = self.parse_html(html_text=response_text)
        except Exception as e:
            raise ParsingException(message=f"HTML response processing failed: {e}")

    def start_crawler(self) -> None:
        """
        Start the crawling job as an asynchronous task.
        """
        asyncio.create_task(self.crawling_job())
