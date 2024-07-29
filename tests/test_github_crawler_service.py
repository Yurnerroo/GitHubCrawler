import httpx
import pytest
from urllib.parse import quote_plus

import respx
from starlette.exceptions import HTTPException

from services.http_service import send_get_request

pytestmark = pytest.mark.asyncio


@respx.mock
async def test_send_request_success(github_crawler_service):
    keywords = github_crawler_service.crawler_settings.keywords
    type_ = github_crawler_service.crawler_settings.type

    url = f"https://github.com/search/?q={quote_plus(",".join(keywords))}&type={quote_plus(type_)}"
    request = respx.get(url).mock(return_value=httpx.Response(200, json={}))

    response = await send_get_request(
        url=url,
        proxy={"http://": "http://localhost:8080"},
        headers=github_crawler_service.headers,
    )
    assert response.status_code == 200
    assert request.called


@respx.mock
async def test_send_request_failure(github_crawler_service):
    keywords = github_crawler_service.crawler_settings.keywords
    type_ = github_crawler_service.crawler_settings.type

    url = f"https://github.com/search/?q={quote_plus(",".join(keywords))}&type={quote_plus(type_)}"
    request = respx.get(url).mock(return_value=httpx.Response(404, json={}))

    with pytest.raises(HTTPException):
        await send_get_request(
            url=url,
            proxy={"http://": "http://localhost:8080"},
            headers=github_crawler_service.headers,
        )
    assert request.called


async def test_parse_html_repositories(github_crawler_service):
    html_text = """
    <html>
        <body>
            <div class="Box-sc-g0xbh4-0 bBwPjs search-title">
                <a href="/author/repo">Text</a>
            </div>
        </body>
    </html>
    """
    expected_result = [{"url": "https://github.com/author/repo"}]
    result = github_crawler_service.parse_html(html_text)

    assert result == expected_result


async def test_parse_html_issues(github_crawler_service):
    github_crawler_service.crawler_settings.type = "issues"
    html_text = """
    <html>
        <body>
            <div class="Box-sc-g0xbh4-0 bBwPjs search-title">
                <a href="/author/repo/issues/1">Issue</a>
            </div>
        </body>
    </html>
    """
    expected_result = [{"url": "https://github.com/author/repo/issues/1"}]
    result = github_crawler_service.parse_html(html_text)
    assert result == expected_result


async def test_parse_html_wikis(github_crawler_service):
    github_crawler_service.crawler_settings.type = "wikis"
    html_text = """
    <html>
        <body>
            <div class="Box-sc-g0xbh4-0 bBwPjs search-title">
                <a href="/author/repo/wiki">Wiki</a>
            </div>
        </body>
    </html>
    """
    expected_result = [{"url": "https://github.com/author/repo/wiki"}]
    result = github_crawler_service.parse_html(html_text)
    assert result == expected_result


@respx.mock
async def test_start_crawler(github_crawler_service):
    keywords = github_crawler_service.crawler_settings.keywords
    type_ = github_crawler_service.crawler_settings.type

    url = f"https://github.com/search/?q={quote_plus(",".join(keywords))}&type={quote_plus(type_)}"
    html_text = """
    <html>
        <body>
            <div class="Box-sc-g0xbh4-0 bBwPjs search-title">
                <a href="/author/repo">Text</a>
            </div>
        </body>
    </html>
    """
    request = respx.get(url).mock(return_value=httpx.Response(200, text=html_text))

    await github_crawler_service.crawling_job()
    expected_result = [{"url": "https://github.com/author/repo"}]
    assert github_crawler_service.last_crawled_results == expected_result
    assert request.called
