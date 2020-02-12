import os

from cache import cache
from fastapi import HTTPException
import httpx

API_KEY = os.environ["GIPHY_API_KEY"]

# Also consider translate:
# http://api.giphy.com/v1/gifs/translate?s={search_text}&api_key={API_KEY}"


async def search(search_text):
    url = (
        f"http://api.giphy.com/v1/gifs/search?q={search_text}&limit=1&api_key={API_KEY}"
    )
    gif_match = await cache.get(url)
    if gif_match is None:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://api.giphy.com/v1/gifs/search?q={search_text}&limit=1&api_key={API_KEY}"
            )
        data = response.json()["data"]
        if len(data) > 0:
            gif_match = data[0]["images"]["original"]["url"]
            await cache.set(url, gif_match)
        else:
            raise HTTPException(
                status_code=400, detail="The search query had no results"
            )
    return gif_match
