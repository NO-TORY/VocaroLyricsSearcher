import requests, regex, html

from typing import Optional, Any
from .exc import SongNotFound

def search(*song: Any, artist: Optional[str] = ""):
    response = requests.get("https://www.google.com/search?q={}+site%3Avocaro.wikidot.com".format(str(*song) + artist))
    s = regex.findall(r"http://vocaro.wikidot.com/.*", html.unescape(response.text))
    try:
        d = s[0][0:s[0].index("&")]
    except:
        raise SongNotFound()

    if all([k == "http://vocaro.wikidot.com" or k == "http://vocaro.wikidot.com/" for k in s]):
        raise SongNotFound()

    return d

def get_lyrics(*song: Any, indents: Optional[int] = 1, artist: Optional[str] = ""):
    song_url = search(*song, artist=artist)

    lyrics = requests.get(song_url).text
    lyrics = html.unescape(lyrics)

    d = regex.findall(r"<td>.*", lyrics)
    s = str("\n"*indents).join(d)
    s = regex.sub(r"(<td>)|(</td>)", "", s)
    s = s.replace("<span class=\"rt\">", "(")
    s = s.replace("</span></span>", ")")
    s = s.replace("<span class=\"ruby\">", "")
    s = regex.sub(r"(<a class.*)|(<a href.*)", "", s)
    return {
        "vocaloid": regex.sub(r"(<a href=\".*\">)|(</a>)|(<td>)|(</td>)", "", d[3]),
        "original_url": regex.sub(r"(target.*)", "", d[0].split("href=")[1].replace("\"", "")),
        "lyrics": s.lstrip().rstrip()
    }
