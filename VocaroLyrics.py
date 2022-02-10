import aiohttp
import re
import asyncio
from collections import namedtuple
from bs4 import BeautifulSoup
from typing import Optional, Union, Any
from fake_useragent import UserAgent

ResultSet = namedtuple("ResultSet", "lyrics original_url vocaloid artist title")

__all__ = (
    "asyncSearch",
    "asyncGet",
    "Search",
    "Get"
)

def Search(**kwargs: Any):
    """보카로 가사위키 링크를 가져옵니다.\n\n
    var song: str | Any
    var artist: Optional[str] | None = ""
    rtype: Any
    return: 보카로 가사 위키 URL
    ```python
    import VocaroLyrics

    print(VocaroLyrics.Search(song="소실"))
    """    

    return asyncio.get_event_loop().run_until_complete(asyncSearch(**kwargs))

def Get(song: Union[str, Any], artist: Optional[str] = "", indents: Optional[int] = 1):
    """보카로 가사위키에서 가사를 가져옵니다.\n\n
    var song: str | Any
    var artist: Optional[str] | None = ""
    var indents: Optional[int] | None = 1
    var session: Optional[Session] | None = None
    rtype: Lyrics
    return: lyrics, original_url, vocaloid, artist, title 
    ```python
    import VocaroLyrics

    print(VocaroLyrics.GetLyrics("animal", "deco*27"))
    """

    return asyncio.get_event_loop().run_until_complete(asyncGet(song, artist, indents))

async def asyncSearch(**kwargs: Any):
    """보카로 가사위키 링크를 가져옵니다.\n\n
    var session: Optional[Session] | None = None
    var song: str | Any
    var artist: Optional[str] | None = ""
    rtype: Any
    return: 보카로 가사 위키 URL
    ```python
    import VocaroLyrics, asyncio

    async def main():
    \treturn await VocaroLyrics.asyncSearch(song="animal", artist="deco*27")

    print(asyncio.run(main()))

    """
    song: Union[str, Any] = kwargs["song"]
    artist: Optional[str] = kwargs.get("artist") if kwargs.get("artist") != None else ""

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
        return d
                

async def asyncGet(song: Union[str, Any], artist: Optional[str] = "", indents: Optional[int] = 1):
    """보카로 가사위키에서 가사를 가져옵니다.\n\n
    var song: str | Any
    var artist: Optional[str] | None = ""
    var indents: Optional[int] | None = 1
    var session: Optional[Session] | None = None
    rtype: Lyrics
    return: lyrics, original_url, vocaloid, artist, title 
    ```python
    import VocaroLyrics, asyncio

    async def main():
        return await VocaroLyrics.asyncGetLyrics("animal", "deco*27")

    print(asyncio.run(main()))
    """
    song_url = await asyncSearch(song=song, artist=artist)

    async with aiohttp.ClientSession(trust_env=True) as session:
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

            _original_url = (re.findall(r"<td>.*", lyrics)[0].split("href=")[1].split(" ")[0].replace("\"", ""))
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
