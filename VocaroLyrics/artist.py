import re
import html
import aiohttp
import asyncio

from typing import Any
from bs4 import BeautifulSoup
from collections import namedtuple
from fake_useragent import UserAgent

ResultSet = namedtuple("ResultSet", "name description songs albums")

async def asyncGetArtist(artist: Any, /):
    r"""| async def |
    Fetch the artist from [vocaro.wikidot.com](http://vocaro.wikidot.com) 
    var artist: Any
    """

    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.google.com/search?q={}+site%3Avocaro.wikidot.com".format(artist), headers={"User-Agent": UserAgent().random}, proxy=None) as response:
            _raw = html.unescape(await response.text("utf-8"))
            soup = BeautifulSoup(_raw, "html5lib")
            _artist = soup.find_all(href=True)
            _links = "\n".join(list(map(str, list(_artist))))
            _links = re.findall(r"http://vocaro.wikidot.com.*", _links)[0]
            _artist = _links[0:_links.index("&")]

        async with session.get(_artist, headers={"User-Agent": UserAgent().random}, proxy=None) as response:
            _raw = html.unescape(await response.text())

            soup = BeautifulSoup(_raw, "html5lib")

        await session.close()
        _content = soup.find(attrs={"id": "page-content"})

        _content_descriptions = _content.find_all("p")
        
        descriptions = []
        albums = []
        songs = []

        is_description = True

        for content in _content_descriptions:
            if content.get_text().endswith("/앨범"):
                is_description = False
                albums.append(content.get_text().replace("/앨범", ""))

            elif not is_description:
                songs.append(content.get_text())
            
            if is_description:
                descriptions.append(content.get_text())

        await session.close()
        return ResultSet(
            soup.find(attrs={"id": "page-title"}).get_text(strip=True),
            "\n".join(descriptions),
            songs,
            albums
        )

def GetArtist(artist: Any, /):
    r"""| def |
    Fetch the artist from [vocaro.wikidot.com](http://vocaro.wikidot.com) 
    var artist: Any
    """

    return asyncio.get_event_loop().run_until_complete(asyncGetArtist(artist))
