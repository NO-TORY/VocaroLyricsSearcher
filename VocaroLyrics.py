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

def search(**kwargs: Any):
    """보카로 가사위키 링크를 가져옵니다.\n\n
    var song: str | Any
    var artist: Optional[str] | None = ""
    ```python
    import VocaroLyrics

    print(VocaroLyrics.search(song="소실"))
    """
    song: Union[str, Any] = kwargs["song"]
    artist: Optional[str] = kwargs.get("artist") if kwargs.get("artist") != None else ""

    response = requests.get("https://www.google.com/search?q={}+site%3Avocaro.wikidot.com".format(song + artist))
    s = regex.findall(r"http://vocaro.wikidot.com/.*", html.unescape(response.text))
    try:
        d = s[0][0:s[0].index("&")]
    except:
        raise TypeError

    if all([k == "http://vocaro.wikidot.com" or k == "http://vocaro.wikidot.com/" for k in s]):
        raise TypeError

    return d

def get_lyrics(**kwargs: Any):
    """보카로 가사위키에서 가사를 가져옵니다.\n\n
    var song: str | Any
    var artist: Optional[str] | None = ""
    var indents: Optional[int] | None = 1
    ```python
    import VocaroLyrics

    print(VocaroLyrics.get_lyrics(song="animal", artist="deco*27", indents=2))
    """
    song: Union[str, Any] = kwargs["song"]
    indents: Optional[int] = kwargs.get("indents") if kwargs.get("indents") != None else 1
    artist: Optional[str] = kwargs.get("artist") if kwargs.get("artist") != None else ""

    song_url = search(song=song, artist=artist)

    lyrics = requests.get(song_url).text
    lyrics = html.unescape(lyrics)

    html_replacements = ("<span style=\"white-space: pre-wrap;\">---", "<span class=\"ruby\">", "---<span>")

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
