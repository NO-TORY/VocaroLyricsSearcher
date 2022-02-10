import re
import aiohttp
import asyncio

from bs4 import BeautifulSoup
from collections import namedtuple     
from fake_useragent import UserAgent   
from typing import Optional, Union, Any

ResultSet = namedtuple("ResultSet", "lyrics original_url vocaloid artist title")

def SearchMusic(song: Union[str, Any], artist: Optional[str] = "", /):
    r"""| Awaitable |
    Fetch the url from [vocaro.wikidot.com](http://vocaro.wikidot.com).
    var song: str | Any
    var artist: Optional[str] | None = ""
    rtype: Any
    return: str
    """    

    return asyncio.get_event_loop().run_until_complete(asyncSearchMusic(song, artist))

def GetMusic(song: Union[str, Any], artist: Optional[str] = "", indents: Optional[int] = 1, /):
    r"""| Callable |
    Fetch the lyrics from [vocaro.wikidot.com](http://vocaro.wikidot.com)
    var song: str | Any
    var artist: Optional[str] | None = ""
    var indents: Optional[int] | None = 1
    rtype: ResultSet
    return: lyrics, original_url, vocaloid, artist, title 
    """

    return asyncio.get_event_loop().run_until_complete(asyncGetMusic(song, artist, indents))

async def asyncSearchMusic(song: Union[str, Any], artist: Optional[str] = "", /):
    r""" | Awaitable |
    Fetch the url from [vocaro.wikidot.com](http://vocaro.wikidot.com)
    var song: str | Any
    var artist: Optional[str] | None = ""
    rtype: str
    return: str
    """

    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.google.com/search?q={}+site%3Avocaro.wikidot.com".format(song + artist), proxy=None, headers={"User-Agent": UserAgent().random}) as response:
            link_list = re.findall(r"http://vocaro.wikidot.com/.*", await response.text("utf-8"))
            try:
                d = link_list[0][0:link_list[0].index("&")]
            except:
                raise TypeError

            if all([link == "http://vocaro.wikidot.com" or link == "http://vocaro.wikidot.com/" for link in link_list]):
                raise TypeError

            await session.close()
        return str(d)

async def asyncGetMusic(song: Union[str, Any], artist: Optional[str] = "", indents: Optional[int] = 1, /):
    r""" | Callable |
    Fetch the lyrics from [vocaro.wikidot.com](http://vocaro.wikidot.com)
    var song: str | Any
    var artist: Optional[str] | None = ""
    var indents: Optional[int] | None = 1
    rtype: Lyrics
    return: lyrics, original_url, vocaloid, artist, title 
    """
    song_url = await asyncSearchMusic(song, artist)

    async with aiohttp.ClientSession() as session:
        async with session.get(song_url, headers={"User-Agent": UserAgent().random, "content-type": "text/html; charset=utf-8"}, proxy=None) as response:
            lyrics = await response.text("utf-8")

            soup = BeautifulSoup(lyrics, "html5lib")
            
            _lyrics = soup.find_all("td")
            _lyrics_group = []

            for _lyric in _lyrics:
                _lyrics_group.append(_lyric.get_text(strip=True))

            _temp_lyrics = "\n".join(_lyrics_group).splitlines()

            _artist = _temp_lyrics[2]
            _vocaloid = _temp_lyrics[4]

            for _ in range(5):
                del _temp_lyrics[0]

            _original_url = (re.findall(r"<td>.*", lyrics)[0].split("href=")[1].split(" ")[0][1:-1])
            _lyrics = str("\n"*indents).join(_temp_lyrics)
            _title = soup.find(attrs={"id": "page-title"}).get_text(strip=True)

    await session.close()
    return ResultSet(
        _lyrics,
        _original_url,
        _vocaloid,
        _artist,
        _title
    )
