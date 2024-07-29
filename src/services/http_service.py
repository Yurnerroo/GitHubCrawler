import httpx
from starlette.exceptions import HTTPException


async def send_get_request(url: str, proxy: dict, headers: dict) -> httpx.Response:
    async with httpx.AsyncClient(proxy=proxy) as client:
        response = await client.get(url, headers=headers)

        if response.status_code == 200:
            return response
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Request failed.\nDetail: {response.text}",
        )
