from pydantic import BaseModel


class GitHubCrawlerSettings(BaseModel):
    keywords: list[str]
    proxies: list[str]
    type: str
