import requests, regex, html, sys

from typing import (
    Any,
    Union,
    Optional,
)
from collections import namedtuple

if sys.version_info.major < 3:
    import future_annotations
    future_annotations.register()

del sys

Lyrics = namedtuple("Lyrics", "lyrics original_url vocaloid")

__all__ = (
    "search",
    "get_lyrics",
)

def search(session: Optional[requests.Session] = None, **kwargs: Any):
    """보카로 가사위키 링크를 가져옵니다.\n\n
    var session: Optional[Session] | None = None
    var song: str | Any
    var artist: Optional[str] | None = ""
    rtype: Any
    return: 보카로 가사 위키 URL
    ```python
    import VocaroLyrics, requests

    session = requests.Session()

    print(VocaroLyrics.search(session, song="소실"))
    """
    song: Union[str, Any] = kwargs["song"]
    artist: Optional[str] = kwargs.get("artist") if kwargs.get("artist") != None else ""

    if session:
        response = session.get("https://www.google.com/search?q={}+site%3Avocaro.wikidot.com".format(song + artist))
    else:
        response = requests.get("https://www.google.com/search?q={}+site%3Avocaro.wikidot.com".format(song + artist))
    s = regex.findall(r"http://vocaro.wikidot.com/.*", html.unescape(response.text))
    try:
        d = s[0][0:s[0].index("&")]
    except:
        raise TypeError

    if all([k == "http://vocaro.wikidot.com" or k == "http://vocaro.wikidot.com/" for k in s]):
        raise TypeError

    return d

def get_lyrics(session: Optional[requests.Session] = None, **kwargs: Any):
    """보카로 가사위키에서 가사를 가져옵니다.\n\n
    var session: Optional[Session] | None = None
    var song: str | Any
    var artist: Optional[str] | None = ""
    var indents: Optional[int] | None = 1
    rtype: Lyrics (namedtuple)
    return: lyrics, original_url, vocaloid
    ```python
    import VocaroLyrics, requests

    session = requests.Session()

    print(VocaroLyrics.get_lyrics(session, song="animal", artist="deco*27", indents=2).lyrics)
    """
    song: Union[str, Any] = kwargs["song"]
    indents: Optional[int] = kwargs.get("indents") if kwargs.get("indents") != None else 1
    artist: Optional[str] = kwargs.get("artist") if kwargs.get("artist") != None else ""

    song_url = search(session, song=song, artist=artist)

    if session:
        lyrics = session.get(song_url).text
    else:
        lyrics = requests.get(song_url).text
    lyrics = html.unescape(lyrics)

    html_replacements = ("<span style=\"white-space: pre-wrap;\">---", "<span class=\"ruby\">", "---</span>")

    d = regex.findall(r"<td>.*", lyrics)
    s = str("\n"*indents).join(d)
    s = regex.sub(r"(<td>)|(</td>)", "", s)
    s = s.replace("<span class=\"rt\">", "(")
    s = s.replace("</span></span>", ")")
    for r in html_replacements:
        s = s.replace(r, "")
    s = regex.sub(r"(<a class.*)|(<a href.*)", "", s)
    
    return Lyrics(
        s.lstrip().rstrip(),
        regex.sub(r"(target.*)", "", d[0].split("href=")[1].replace("\"", "")), 
        regex.sub(r"(<a href=\".*\">)|(</a>)|(<td>)|(</td>)", "", d[3])
    )   
